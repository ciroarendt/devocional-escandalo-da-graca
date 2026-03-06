#!/usr/bin/env python3
"""
MCTI Lei do Bem — Scraper de Lotes
Captura PDFs e ZIPs de pareceres técnicos, contestações e recursos
da página de Lotes do Ministério da Ciência e Tecnologia.

Fonte: https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/lei-do-bem/paginas/lotes
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path


URL_LOTES = "https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/lei-do-bem/paginas/lotes"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "identity",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# Regex para extrair ano-base da URL
ANO_BASE_PATTERNS = [
    r"ab[_-]?(\d{4})",            # ab-2023, ab2023, ab_2023
    r"ano[_-]?base[_-]?(\d{4})",  # ano-base-2023
    r"AB(\d{4})",                  # AB2023
    r"(\d{4})[_-]1?\.zip",        # 2018-1.zip
    r"anteriores[_-]?(\d{4})",    # anteriores2023
    r"anteriores_(\d{4})",        # anteriores_2022
    r"adm[_-](\d{4})",            # adm-2021
    r"/ano-base-(\d{4})/",        # /ano-base-2016/
    r"de[_-]?(\d{4})\.zip",       # de2019.zip, de-2019.zip
    r"de(\d{4})",                  # conjuntodoslotesdoanobasede2019
]


def fetch_page(url):
    """Faz request da página com headers de browser."""
    print(f"  Acessando {url} ...")
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        print(f"  Página carregada ({len(html):,} bytes)")
        return html
    except urllib.error.HTTPError as e:
        print(f"  ERRO HTTP {e.code}: {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"  ERRO de conexão: {e.reason}")
        sys.exit(1)


def extract_links(html):
    """Extrai todos os links de PDF e ZIP relacionados à Lei do Bem."""
    # Busca todos os anchors com href contendo .pdf ou .zip
    pattern = r'<a[^>]*href="([^"]*\.(?:pdf|zip)[^"]*)"[^>]*>(.*?)</a>'
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)

    links = []
    seen = set()

    for href, text_html in matches:
        # Filtra apenas links da Lei do Bem
        if "lei-do-bem" not in href.lower() and "lei_do_bem" not in href.lower():
            continue

        # Remove duplicatas
        if href in seen:
            continue
        seen.add(href)

        text = re.sub(r"<[^>]+>", "", text_html).strip()
        ext = "pdf" if ".pdf" in href.lower() else "zip"
        filename = href.split("/")[-1]
        ano_base = detect_ano_base(href)
        tipo = classify_tipo(href, filename)

        links.append({
            "url": href,
            "filename": filename,
            "text": text if text else filename,
            "tipo_arquivo": ext.upper(),
            "ano_base": ano_base,
            "tipo": tipo,
        })

    # Ordena por ano_base (desc) e depois por filename
    links.sort(key=lambda x: (x["ano_base"] or "0000", x["filename"]), reverse=True)
    return links


def detect_ano_base(url):
    """Detecta o ano-base a partir da URL."""
    for pattern in ANO_BASE_PATTERNS:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            ano = match.group(1)
            if 2006 <= int(ano) <= 2030:
                return ano
    return None


def classify_tipo(url, filename):
    """Classifica o tipo do documento."""
    lower = (url + filename).lower()
    if "manual" in lower:
        return "Manual"
    if "recurso" in lower or "recurso-adm" in lower:
        return "Recurso Administrativo"
    if "contestacao" in lower or "contestacão" in lower:
        return "Contestação"
    if "retifica" in lower:
        return "Retificação"
    if "conjunto" in lower or "anteriores" in lower:
        return "Publicações Anteriores (consolidado)"
    if "parecer" in lower:
        return "Parecer Técnico"
    return "Outro"


def format_size(size_bytes):
    """Formata bytes em formato legível."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def download_file(url, dest_path):
    """Baixa um arquivo com progresso."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            total = resp.headers.get("Content-Length")
            total = int(total) if total else None

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            downloaded = 0
            block_size = 8192

            with open(dest_path, "wb") as f:
                while True:
                    chunk = resp.read(block_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total:
                        pct = downloaded / total * 100
                        bar_len = 30
                        filled = int(bar_len * downloaded / total)
                        bar = "█" * filled + "░" * (bar_len - filled)
                        sys.stdout.write(
                            f"\r    [{bar}] {pct:5.1f}% "
                            f"({format_size(downloaded)}/{format_size(total)})"
                        )
                    else:
                        sys.stdout.write(f"\r    Baixando... {format_size(downloaded)}")
                    sys.stdout.flush()

            print()  # Nova linha após progresso
            return downloaded

    except urllib.error.HTTPError as e:
        print(f"\n    ERRO HTTP {e.code}: {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"\n    ERRO de conexão: {e.reason}")
        return None
    except Exception as e:
        print(f"\n    ERRO: {e}")
        return None


def print_table(links):
    """Imprime tabela formatada dos links encontrados."""
    print(f"\n{'#':>3}  {'Ano':>4}  {'Tipo':<8}  {'Categoria':<32}  {'Arquivo'}")
    print("─" * 120)

    for i, link in enumerate(links, 1):
        ano = link["ano_base"] or "  ? "
        tipo = link["tipo_arquivo"]
        cat = link["tipo"][:32]
        name = link["filename"][:60]
        print(f"{i:3d}  {ano:>4}  {tipo:<8}  {cat:<32}  {name}")

    print("─" * 120)
    print(f"Total: {len(links)} arquivos")

    # Resumo por ano
    anos = {}
    for link in links:
        ano = link["ano_base"] or "Sem ano"
        anos[ano] = anos.get(ano, 0) + 1

    print("\nResumo por ano-base:")
    for ano in sorted(anos.keys(), reverse=True):
        print(f"  {ano}: {anos[ano]} arquivo(s)")


def save_report(links, output_dir, results=None):
    """Salva relatório JSON."""
    report = {
        "fonte": URL_LOTES,
        "data_extracao": datetime.now().isoformat(),
        "total_arquivos": len(links),
        "arquivos": links,
    }

    if results:
        report["downloads"] = {
            "sucesso": sum(1 for r in results if r["status"] == "ok"),
            "erro": sum(1 for r in results if r["status"] == "erro"),
            "detalhes": results,
        }

    report_path = os.path.join(output_dir, "relatorio.json")
    os.makedirs(output_dir, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nRelatório salvo em: {report_path}")
    return report_path


def run_scraper(args):
    """Fluxo principal do scraper."""
    print("=" * 60)
    print("  MCTI Lei do Bem — Scraper de Lotes")
    print("=" * 60)

    # 1. Fetch da página
    print("\n[1/4] Acessando página do MCTI...")
    html = fetch_page(URL_LOTES)

    # 2. Extração de links
    print("\n[2/4] Extraindo links de arquivos...")
    links = extract_links(html)
    print(f"  Encontrados {len(links)} arquivos (PDFs + ZIPs)")

    # 3. Filtro por ano-base
    if args.ano:
        links = [l for l in links if l["ano_base"] == args.ano]
        print(f"  Filtrado para ano-base {args.ano}: {len(links)} arquivo(s)")

    if not links:
        print("\n  Nenhum arquivo encontrado com os filtros aplicados.")
        return

    # Mostra tabela
    print_table(links)

    # Se --list, apenas lista e salva relatório
    if args.list:
        save_report(links, args.output)
        return

    # 4. Download dos arquivos
    print(f"\n[3/4] Baixando {len(links)} arquivos para '{args.output}/'...")
    print(f"  (Ctrl+C para cancelar)\n")

    results = []
    success = 0
    errors = 0

    for i, link in enumerate(links, 1):
        ano = link["ano_base"] or "outros"
        subdir = "manuais" if link["tipo"] == "Manual" else ano
        dest_dir = os.path.join(args.output, subdir)
        dest_path = os.path.join(dest_dir, link["filename"])

        print(f"  [{i}/{len(links)}] {link['filename']}")

        if os.path.exists(dest_path) and not args.force:
            size = os.path.getsize(dest_path)
            print(f"    Já existe ({format_size(size)}), pulando. Use --force para rebaixar.")
            results.append({"arquivo": link["filename"], "status": "existente", "tamanho": size})
            success += 1
            continue

        size = download_file(link["url"], dest_path)

        if size is not None:
            results.append({"arquivo": link["filename"], "status": "ok", "tamanho": size})
            success += 1
        else:
            results.append({"arquivo": link["filename"], "status": "erro"})
            errors += 1

        # Pausa entre downloads para não sobrecarregar o servidor
        if i < len(links):
            time.sleep(1)

    # 5. Relatório
    print(f"\n[4/4] Gerando relatório...")
    save_report(links, args.output, results)

    print(f"\n{'=' * 60}")
    print(f"  Concluído!")
    print(f"  Downloads: {success} sucesso, {errors} erro(s)")
    print(f"  Pasta: {os.path.abspath(args.output)}/")
    print(f"{'=' * 60}")


def main():
    parser = argparse.ArgumentParser(
        description="MCTI Lei do Bem — Scraper de Lotes de Pareceres Técnicos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 scraper.py --list                 # Lista todos os arquivos disponíveis
  python3 scraper.py --ano 2023             # Baixa apenas ano-base 2023
  python3 scraper.py --ano 2023 --list      # Lista apenas ano-base 2023
  python3 scraper.py                        # Baixa TODOS os arquivos
  python3 scraper.py --output meus_dados    # Salva em pasta personalizada
  python3 scraper.py --force                # Rebaixa arquivos existentes
        """,
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="Apenas lista os arquivos sem baixar",
    )
    parser.add_argument(
        "--ano", "-a",
        type=str,
        help="Filtra por ano-base (ex: 2023, 2022)",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="downloads",
        help="Pasta de destino dos downloads (default: downloads/)",
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Força re-download de arquivos existentes",
    )

    args = parser.parse_args()

    try:
        run_scraper(args)
    except KeyboardInterrupt:
        print("\n\nDownload cancelado pelo usuário.")
        sys.exit(0)


if __name__ == "__main__":
    main()
