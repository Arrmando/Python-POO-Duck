#!/usr/bin/env bash
set -euo pipefail

BASE="http://localhost:8000"
cd "$(dirname "$0")"

run() {
    printf '%s\n' "$1"
    eval "$2"
    echo
}

run \
"> curl $BASE/insumo | jq" \
"curl -s $BASE/insumo | jq"

run \
"> curl -X POST $BASE/insumo \\
    -H 'Content-Type: application/json' \\
    -d @post_ingrediente.json | jq" \
"curl -s -X POST $BASE/insumo -H 'Content-Type: application/json' -d @post_ingrediente.json | jq"

run \
"> curl -X POST $BASE/insumo \\
    -H 'Content-Type: application/json' \\
    -d @post_homem_hora.json | jq" \
"curl -s -X POST $BASE/insumo -H 'Content-Type: application/json' -d @post_homem_hora.json | jq"

run \
"> curl $BASE/insumo | jq" \
"curl -s $BASE/insumo | jq"

run \
"> curl -X POST $BASE/insumo \\
    -H 'Content-Type: application/json' \\
    -d @post_tipo_invalido.json | jq" \
"curl -s -X POST $BASE/insumo -H 'Content-Type: application/json' -d @post_tipo_invalido.json | jq"

run \
"> curl -X POST $BASE/insumo \\
    -H 'Content-Type: application/json' \\
    -d @post_quantidade_invalida.json | jq" \
"curl -s -X POST $BASE/insumo -H 'Content-Type: application/json' -d @post_quantidade_invalida.json | jq"
