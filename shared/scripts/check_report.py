#!/usr/bin/env -S uv run --with pypdf
import os
import sys

from pypdf import PdfReader


def check_report(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo '{pdf_path}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        appendix_start_page = None

        for i, page in enumerate(reader.pages):
            text = page.extract_text().lower()
            if "apêndice" in text or "appendix" in text or "diagramas uml" in text:
                appendix_start_page = i + 1
                break

        content_pages = appendix_start_page - 1 if appendix_start_page else total_pages

        if not (4 <= content_pages <= 8):
            print(
                f"Erro: O relatório possui {content_pages} páginas de conteúdo, mas o esperado é entre 4 e 8.",
                file=sys.stderr,
            )
            sys.exit(1)

        sys.exit(0)

    except Exception as e:
        print(f"Erro ao processar o relatório: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <caminho_do_pdf>", file=sys.stderr)
        sys.exit(1)

    check_report(sys.argv[1])
