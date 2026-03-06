import json
import re

# Load all data sources
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos.json') as f:
    sim_data = json.load(f)

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_bids_config.json') as f:
    bids_data = json.load(f)

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_assembleias.json') as f:
    asm_data = json.load(f)

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_crm.json') as f:
    crm_data = json.load(f)

# ==========================================
# Step 1: Build groups from SIMULATOR (full data)
# ==========================================
groups_by_id = {}

for seg_key, seg_info in sim_data.items():
    segment_label = seg_info['label']
    for gid, gdata in seg_info['groups'].items():
        sp = gdata.get('salesPlan', {})
        inst = gdata.get('installment', {})

        group_num = str(gdata.get('group', ''))
        bid_key = group_num.zfill(6)
        bid_configs = bids_data.get(bid_key, [])

        bids = {}
        for bc in bid_configs:
            mod = bc.get('st_modalidade', '')
            bids[mod] = {
                'enabled': bc.get('sn_habilitada') == 'S',
                'name': bc.get('nm_modalidade', ''),
                'oferta': bc.get('st_oferta', ''),
                'lance_embutido_max': bc.get('pe_lance_embutido_max', 0),
                'parcelas_embutido_max': bc.get('qt_pc_lance_embutido_max', 0),
                'regra': bc.get('regra_lance', '')
            }

        groups_by_id[group_num] = {
            'id': gid,
            'group': gdata.get('group'),
            'name': gdata.get('name', ''),
            'segment': segment_label,
            'segmentKey': seg_key,
            'productId': sp.get('productId', ''),
            'amount': gdata.get('amount', 0),
            'status': gdata.get('groupStatus', ''),
            'active': gdata.get('active', False),
            'participantsTotal': gdata.get('participantsTotal', 0),
            'participantsRemaining': gdata.get('participantsRemaining', 0),
            'correctionIndex': gdata.get('groupCorrectionIndex', ''),
            'administrationFee': gdata.get('administrationFee', 0),
            'administrationFeePerYear': gdata.get('administrationFeePerYear', 0),
            'insuranceFee': gdata.get('insuranceFee', 0),
            'reserveFundFee': gdata.get('reserveFundFee', 0),
            'installment': {
                'value': inst.get('value', 0),
                'reducedValue': inst.get('reducedValue', 0),
                'monthsRemaining': inst.get('monthsRemaining', 0),
                'monthsTotal': inst.get('monthsTotal', 0),
                'finalReducedMonth': inst.get('finalReducedMonth', 0),
                'finalReducedValue': inst.get('finalReducedValue', 0),
            },
            'salesPlan': {
                'name': sp.get('salesPlanName', ''),
                'isDiluted': sp.get('isDiluted', False),
                'isHole': sp.get('isHole', False),
            },
            'bids': bids,
            'category': None,
            'hasFullData': True,
        }

# ==========================================
# Step 2: Add groups from CRM Extractions (missing from simulator)
# ==========================================

segment_map = {
    'properties': {'label': 'Imoveis', 'key': 'property-segment', 'productId': '101'},
    'vehicles': {'label': 'Veiculos', 'key': 'vehicle-segment', 'productId': '102'},
}

for ext_type, seg_info in segment_map.items():
    exts = crm_data.get('extractions', {}).get(ext_type, {})
    if not exts:
        continue

    latest_key = sorted(exts.keys())[-1]
    ext = exts[latest_key]
    extraction = ext.get('extractionFirstNumber', {}).get('extraction', {})

    for cat_letter, cat_data in extraction.items():
        cat_groups = cat_data.get('groups', [])
        for g_num in cat_groups:
            g_str = str(g_num)
            if g_str in groups_by_id:
                # Already have from simulator, just set category
                groups_by_id[g_str]['category'] = cat_letter
            else:
                # New group from CRM - add with limited data
                bid_key = g_str.zfill(6)
                bid_configs = bids_data.get(bid_key, [])

                bids = {}
                for bc in bid_configs:
                    mod = bc.get('st_modalidade', '')
                    bids[mod] = {
                        'enabled': bc.get('sn_habilitada') == 'S',
                        'name': bc.get('nm_modalidade', ''),
                        'oferta': bc.get('st_oferta', ''),
                        'lance_embutido_max': bc.get('pe_lance_embutido_max', 0),
                        'parcelas_embutido_max': bc.get('qt_pc_lance_embutido_max', 0),
                        'regra': bc.get('regra_lance', '')
                    }

                # Determine name (zero-padded 6 digits for imoveis, Axxx for veiculos)
                name = bid_key  # e.g. "001010"

                groups_by_id[g_str] = {
                    'id': g_str,
                    'group': int(g_str) if g_str.isdigit() else g_str,
                    'name': name,
                    'segment': seg_info['label'],
                    'segmentKey': seg_info['key'],
                    'productId': seg_info['productId'],
                    'amount': 0,
                    'status': 'active',
                    'active': True,
                    'participantsTotal': 0,
                    'participantsRemaining': 0,
                    'correctionIndex': '',
                    'administrationFee': 0,
                    'administrationFeePerYear': 0,
                    'insuranceFee': 0,
                    'reserveFundFee': 0,
                    'installment': {
                        'value': 0,
                        'reducedValue': 0,
                        'monthsRemaining': 0,
                        'monthsTotal': 0,
                        'finalReducedMonth': 0,
                        'finalReducedValue': 0,
                    },
                    'salesPlan': {
                        'name': '',
                        'isDiluted': False,
                        'isHole': False,
                    },
                    'bids': bids,
                    'category': cat_letter,
                    'hasFullData': False,
                }

# ==========================================
# Step 3: Build calendar with proper parsing
# ==========================================
calendar = {}
for pid, assemblies in asm_data.get('calendar', {}).items():
    calendar[pid] = []
    for a in assemblies:
        # Parse grupos - it's a string like "[000530, 000540, ...]"
        grupos_raw = a.get('grupos', '')
        if isinstance(grupos_raw, str):
            # Remove brackets and split
            clean = grupos_raw.strip('[] ')
            if clean:
                parsed_groups = [g.strip() for g in clean.split(',') if g.strip()]
            else:
                parsed_groups = []
        elif isinstance(grupos_raw, list):
            parsed_groups = [str(g) for g in grupos_raw]
        else:
            parsed_groups = []

        calendar[pid].append({
            'date': a.get('dt_assembleia', ''),
            'time': a.get('hr_assembleia', ''),
            'groups': parsed_groups
        })

# ==========================================
# Step 4: Build final output
# ==========================================
groups = sorted(groups_by_id.values(), key=lambda g: (g['segment'], -g['amount'] if g['amount'] else 0, g['name']))

stats = {
    'totalGroups': len(groups),
    'withFullData': sum(1 for g in groups if g.get('hasFullData')),
    'withoutFullData': sum(1 for g in groups if not g.get('hasFullData')),
    'bySegment': {},
    'bySegmentFull': {},
}

for g in groups:
    seg = g['segment']
    stats['bySegment'][seg] = stats['bySegment'].get(seg, 0) + 1
    if g.get('hasFullData'):
        stats['bySegmentFull'][seg] = stats['bySegmentFull'].get(seg, 0) + 1

output = {
    'groups': groups,
    'calendar': calendar,
    'stats': stats,
}

# Write JS
js_content = "// Dados consolidados do sistema ADEMICON v2\n"
js_content += f"// Gerado em: 2026-02-24\n"
js_content += f"// Total de grupos: {len(groups)} ({stats['withFullData']} completos + {stats['withoutFullData']} parciais)\n\n"
js_content += f"const DADOS = {json.dumps(output, ensure_ascii=False)};\n"

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados.js', 'w') as f:
    f.write(js_content)

print(f"=== CONSOLIDATION v2 COMPLETE ===")
print(f"Total groups: {len(groups)}")
print(f"With full data: {stats['withFullData']}")
print(f"Without full data (cotas esgotadas): {stats['withoutFullData']}")
print(f"\nBy segment:")
for seg in sorted(stats['bySegment'].keys()):
    total = stats['bySegment'][seg]
    full = stats['bySegmentFull'].get(seg, 0)
    print(f"  {seg}: {total} total ({full} completos, {total - full} parciais)")
print(f"\nCalendar:")
for pid, asm_list in calendar.items():
    total_groups = set()
    for a in asm_list:
        total_groups.update(a['groups'])
    print(f"  Produto {pid}: {len(asm_list)} assembleias, {len(total_groups)} grupos")
print(f"\nFile size: {len(js_content)} chars")
