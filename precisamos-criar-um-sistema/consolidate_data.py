import json

# Load all data sources
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos.json') as f:
    sim_data = json.load(f)

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_bids_config.json') as f:
    bids_data = json.load(f)

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_assembleias.json') as f:
    asm_data = json.load(f)

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_crm.json') as f:
    crm_data = json.load(f)

# Build consolidated groups array
groups = []
for seg_key, seg_info in sim_data.items():
    segment_label = seg_info['label']
    for gid, gdata in seg_info['groups'].items():
        sp = gdata.get('salesPlan', {})
        inst = gdata.get('installment', {})

        # Find bid config for this group
        # Group names have formats like "002010", "A950", "SE18", "MT001", "BM008"
        group_name = gdata.get('name', '')
        group_num = str(gdata.get('group', ''))

        # Bid config uses zero-padded 6-digit group number
        bid_key = group_num.zfill(6)
        bid_configs = bids_data.get(bid_key, [])

        # Also try the group name with zero padding
        if not bid_configs:
            bid_key2 = group_name.zfill(6) if group_name.isdigit() else group_name
            bid_configs = bids_data.get(bid_key2, [])

        # Parse bid modalities
        bids = {}
        for bc in bid_configs:
            mod = bc.get('st_modalidade', '')
            enabled = bc.get('sn_habilitada') == 'S'
            bids[mod] = {
                'enabled': enabled,
                'name': bc.get('nm_modalidade', ''),
                'oferta': bc.get('st_oferta', ''),
                'lance_embutido_max': bc.get('pe_lance_embutido_max', 0),
                'parcelas_embutido_max': bc.get('qt_pc_lance_embutido_max', 0),
                'regra': bc.get('regra_lance', '')
            }

        # Find category from extractions
        category = None
        ext_type = 'properties' if seg_key == 'property-segment' else 'vehicles' if seg_key == 'vehicle-segment' else None
        if ext_type and ext_type in crm_data.get('extractions', {}):
            exts = crm_data['extractions'][ext_type]
            if exts:
                latest_key = sorted(exts.keys())[-1]
                ext = exts[latest_key]
                first = ext.get('extractionFirstNumber', {}).get('extraction', {})
                for cat_letter, cat_data in first.items():
                    if group_num in [str(g) for g in cat_data.get('groups', [])]:
                        category = cat_letter
                        break

        group = {
            'id': gid,
            'group': gdata.get('group'),
            'name': group_name,
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
            'category': category,
        }
        groups.append(group)

# Sort by segment then by credit amount
groups.sort(key=lambda g: (g['segment'], g['amount']))

# Build calendar data (simplified)
calendar = {}
for pid, assemblies in asm_data.get('calendar', {}).items():
    calendar[pid] = []
    for asm in assemblies:
        calendar[pid].append({
            'date': asm.get('dt_assembleia', ''),
            'time': asm.get('hr_assembleia', ''),
            'groups': asm.get('grupos', [])
        })

# Build assembly history summary
assembly_history = {
    'imoveis': {'months': len(asm_data.get('imoveis_assemblies', []))},
    'veiculos': {'months': len(asm_data.get('veiculos_assemblies', []))}
}

# Build the consolidated JS
output = {
    'groups': groups,
    'calendar': calendar,
    'assemblyHistory': assembly_history,
    'stats': {
        'totalGroups': len(groups),
        'bySegment': {},
        'totalBidsConfig': len(bids_data),
    }
}

# Count by segment
for g in groups:
    seg = g['segment']
    if seg not in output['stats']['bySegment']:
        output['stats']['bySegment'][seg] = 0
    output['stats']['bySegment'][seg] += 1

# Write as JS module
js_content = f"// Dados consolidados do sistema ADEMICON\n"
js_content += f"// Gerado em: 2026-02-24\n"
js_content += f"// Total de grupos: {len(groups)}\n\n"
js_content += f"const DADOS = {json.dumps(output, ensure_ascii=False, indent=2)};\n"

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados.js', 'w') as f:
    f.write(js_content)

print(f"=== CONSOLIDATION COMPLETE ===")
print(f"Total groups: {len(groups)}")
print(f"By segment: {output['stats']['bySegment']}")
print(f"Groups with bids: {sum(1 for g in groups if g['bids'])}")
print(f"Groups with category: {sum(1 for g in groups if g['category'])}")
print(f"Calendar products: {list(calendar.keys())}")
print(f"File: dados.js ({len(js_content)} chars)")

# Show a sample group
print(f"\n=== SAMPLE GROUP ===")
print(json.dumps(groups[0], indent=2, ensure_ascii=False)[:800])
