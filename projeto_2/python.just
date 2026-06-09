_sys_python := if os_family() == "windows" { "python" } else { "python3" }
python      := if os_family() == "windows" { ".venv\\Scripts\\python.exe" } else { ".venv/bin/python" }
run         := if os_family() == "windows" { ".venv\\Scripts\\" } else { ".venv/bin/" }

[private, unix]
setup-venv:
    #!/usr/bin/env sh
    [ -d .venv ] && exit 0
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install --group dev -e .

[private, windows]
setup-venv:
    #!/usr/bin/env pwsh
    if (Test-Path .venv) { exit 0 }
    python -m venv .venv
    .venv\Scripts\pip install --upgrade pip
    .venv\Scripts\pip install --group dev -e .

# Gera os artefatos de distribuição
build: setup-venv
    {{python}} -m build

# Formata o código e documentacao
format: setup-venv
    {{run}}ruff format .
    {{run}}ruff check --fix .
    {{run}}mdformat .

# Verifica problemas de estilo e qualidade
lint: setup-venv
    {{run}}ruff check .

# Executa os testes (aceita argumentos extras do pytest)
test *args: setup-venv
    {{run}}pytest {{args}}

# Remove artefatos de build e cache
clean:
    {{_sys_python}} -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) if p.is_dir() else p.unlink(missing_ok=True) for p in [pathlib.Path(x) for x in ['dist', '.pytest_cache', '.ruff_cache', '.coverage']]]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"
