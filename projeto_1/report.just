# Comandos para gerenciamento de relatórios usando LaTeX puro (Modular).

[private]
default:
    @just --list report

# Gera o relatório da Parte 2 em PDF
parte-2:
    cd docs/relatorio-parte-2 && pdflatex -interaction=nonstopmode _main.tex && pdflatex -interaction=nonstopmode _main.tex
    cp docs/relatorio-parte-2/_main.pdf ./relatorio-parte-2.pdf

# Limpa arquivos auxiliares do LaTeX
clean:
    cd docs/relatorio-parte-2 && rm -f *.aux *.log *.out *.toc *.pdf
