"""
Dashboard Web — Lotes Lei do Bem (MCTI)
Backend Flask com API de scraping
"""

import json
import re
import time
from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Cache em memória
_cache = {
    "data": None,
    "timestamp": 0,
    "ttl": 3600  # 1 hora
}

MCTI_URL = "https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/lei-do-bem/paginas/lotes"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "identity",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}


def classify_document(url, context_text=""):
    """Classifica o tipo de documento baseado na URL e contexto."""
    url_lower = url.lower()
    ctx = context_text.lower()

    if "manual" in url_lower or "manual" in ctx:
        return "Manual"
    if "recurso" in url_lower or "recurso" in ctx:
        return "Recurso Administrativo"
    if "contestac" in url_lower or "contestac" in ctx:
        return "Contestação"
    if "retifica" in url_lower or "retifica" in ctx:
        return "Retificação"
    if "parecer" in url_lower or "parecer" in ctx:
        return "Parecer Técnico"
    if "conjunto" in url_lower or "publicacoes-anteriores" in url_lower or "publicac" in url_lower:
        return "Consolidado"
    return "Outro"


def extract_year(url):
    """Extrai o ano-base da URL."""
    # Padrão: ab-2023, ab-2022, ano-base-2021, etc.
    match = re.search(r'(?:ab|ano-base)[-_]?(20\d{2})', url.lower())
    if match:
        return match.group(1)

    # Padrão: /2017/, /2018/, etc. no path
    match = re.search(r'/(\d{4})/', url)
    if match:
        year = match.group(1)
        if 2006 <= int(year) <= 2030:
            return year

    # Padrão: anteriores2023, anteriores_2022
    match = re.search(r'anteriores[_]?(20\d{2})', url.lower())
    if match:
        return match.group(1)

    # Padrão no nome: 2019.zip, 2018-1.zip
    match = re.search(r'(20\d{2})(?:[-_]?\d)?\.(?:zip|pdf|7z)', url.lower())
    if match:
        return match.group(1)

    return "N/A"


def extract_lot_number(url):
    """Extrai o número do lote da URL."""
    # Padrão: 11-lote, 10-lote, 9-lote
    match = re.search(r'(\d+)[oa]?[-_]lote', url.lower())
    if match:
        return int(match.group(1))

    # Padrão: lote-contestacao, publicacao-lei-do-bem-N-lote
    match = re.search(r'bem[-_](\d+)[-_]lote', url.lower())
    if match:
        return int(match.group(1))

    # Padrão: N-lote-do-parecer
    match = re.search(r'(\d+)[-_]lote[-_]', url.lower())
    if match:
        return int(match.group(1))

    return None


def get_file_format(url):
    """Retorna o formato do arquivo."""
    url_lower = url.lower()
    if url_lower.endswith('.pdf'):
        return "PDF"
    if url_lower.endswith('.zip'):
        return "ZIP"
    if url_lower.endswith('.7z'):
        return "7Z"
    return "Outro"


def generate_friendly_name(url, doc_type, year, lot_number):
    """Gera um nome amigável para o documento."""
    fmt = get_file_format(url)

    if doc_type == "Manual":
        if "contestac" in url.lower():
            return "Manual do Usuário — Contestação"
        if "recurso" in url.lower():
            return "Manual do Usuário — Recurso Administrativo"
        return "Manual do Usuário"

    if doc_type == "Consolidado":
        if "conjunto" in url.lower():
            return f"Conjunto dos Lotes — Ano-Base {year} ({fmt})"
        return f"Publicações Anteriores — Ano-Base {year} ({fmt})"

    lot_str = f"{lot_number}º Lote" if lot_number else "Lote"
    return f"{lot_str} — {doc_type} — Ano-Base {year} ({fmt})"


def scrape_lotes():
    """Faz scraping da página de lotes do MCTI."""
    now = time.time()

    # Verifica cache
    if _cache["data"] and (now - _cache["timestamp"]) < _cache["ttl"]:
        return _cache["data"]

    resp = requests.get(MCTI_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Encontrar todos os links relevantes de Lei do Bem
    lotes = []
    seen_urls = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]

        # Filtrar apenas links de Lei do Bem com arquivos
        if not any(ext in href.lower() for ext in ['.pdf', '.zip', '.7z']):
            continue

        if "lei-do-bem" not in href.lower() and "lei_do_bem" not in href.lower():
            continue

        # Evitar duplicatas
        if href in seen_urls:
            continue
        seen_urls.add(href)

        # Capturar contexto (texto ao redor do link)
        parent = a_tag.parent
        context_text = ""
        if parent:
            # Subir até encontrar um bloco com texto significativo
            for ancestor in a_tag.parents:
                text = ancestor.get_text(separator=" ", strip=True)
                if len(text) > 20:
                    context_text = text[:500]
                    break

        year = extract_year(href)
        doc_type = classify_document(href, context_text)
        lot_number = extract_lot_number(href)
        file_format = get_file_format(href)
        friendly_name = generate_friendly_name(href, doc_type, year, lot_number)

        # Extrair nome do arquivo da URL
        filename = href.split("/")[-1]

        lotes.append({
            "id": len(lotes) + 1,
            "name": friendly_name,
            "filename": filename,
            "url": href,
            "year": year,
            "type": doc_type,
            "format": file_format,
            "lot_number": lot_number,
            "is_legacy": "antigo.mctic.gov.br" in href,
        })

    # Ordenar por ano (desc) e depois por número do lote (desc)
    lotes.sort(key=lambda x: (
        x["year"] if x["year"] != "N/A" else "0000",
        x["lot_number"] or 0
    ), reverse=True)

    # Recalcular IDs após ordenação
    for i, lote in enumerate(lotes):
        lote["id"] = i + 1

    # Calcular estatísticas
    stats = {
        "total": len(lotes),
        "by_year": {},
        "by_type": {},
        "by_format": {},
        "years": sorted(set(l["year"] for l in lotes if l["year"] != "N/A"), reverse=True),
        "types": sorted(set(l["type"] for l in lotes)),
    }

    for lote in lotes:
        y = lote["year"]
        t = lote["type"]
        f = lote["format"]
        stats["by_year"][y] = stats["by_year"].get(y, 0) + 1
        stats["by_type"][t] = stats["by_type"].get(t, 0) + 1
        stats["by_format"][f] = stats["by_format"].get(f, 0) + 1

    result = {
        "lotes": lotes,
        "stats": stats,
        "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_url": MCTI_URL,
    }

    # Atualizar cache
    _cache["data"] = result
    _cache["timestamp"] = now

    return result


# ── Rotas ──────────────────────────────────────────────

@app.route("/")
def index():
    try:
        data = scrape_lotes()
    except Exception:
        data = None
    return render_template("index.html", initial_data=json.dumps(data, ensure_ascii=False) if data else "null")


@app.route("/api/lotes")
def api_lotes():
    try:
        data = scrape_lotes()
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": f"Erro ao acessar o site do MCTI: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@app.route("/api/refresh")
def api_refresh():
    """Força re-scraping limpando o cache."""
    _cache["data"] = None
    _cache["timestamp"] = 0
    try:
        data = scrape_lotes()
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": f"Erro ao acessar o site do MCTI: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
