# Comandos para gerenciamento de relatórios usando LaTeX puro (Modular).

[private]
default:
    @just --list report

# Gera o relatório da Parte 2 em PDF
parte-2:
    docker run --rm \
        -v $(pwd):/workdir \
        -w /workdir/docs/relatorio-parte-2 \
        ghcr.io/xu-cheng/texlive-debian:latest \
        lualatex -interaction=nonstopmode _main.tex
    docker run --rm \
        -v $(pwd):/workdir \
        -w /workdir/docs/relatorio-parte-2 \
        ghcr.io/xu-cheng/texlive-debian:latest \
        lualatex -interaction=nonstopmode _main.tex
    cp docs/relatorio-parte-2/_main.pdf ./relatorio-parte-2.pdf

# Gera o relatório final em PDF
final:
    docker run --rm \
        -v $(pwd):/workdir \
        -w /workdir/docs/relatorio-final \
        ghcr.io/xu-cheng/texlive-debian:latest \
        latexmk -pdf -interaction=nonstopmode main.tex
    cp docs/relatorio-final/main.pdf ./relatorio-final.pdf

# Limpa arquivos auxiliares do LaTeX
clean:
    cd docs/relatorio-parte-2 && rm -f *.aux *.log *.out *.toc *.pdf
    cd docs/relatorio-final && rm -f *.aux *.log *.out *.toc *.pdf *.fdb_latexmk *.fls

# Valida a quantidade de páginas do relatório
check file:
    ../shared/scripts/check_report.py {{ file }}
