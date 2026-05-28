import json
from pathlib import Path
from typing import Any

from src.projeto_1.dominio.base import Insumo
from src.projeto_1.dominio.homem_hora import HomemHora
from src.projeto_1.dominio.ingrediente import Ingrediente
from src.projeto_1.persistencia.base import Repositorio


class RepositorioInsumo(Repositorio):
    """Repositório concreto para gerenciar os insumos, implementando os métodos
    definidos na classe abstrata Repositorio"""

    def __init__(self) -> None:
        # inicializa o dicionario vazio que funcionara como o banco de dados
        # a chave do dicionário será o ID do insumo e o valor será o objeto Insumo
        # correspondente
        self._dados: dict[Any, Insumo] = {}
        self._proximo_id = 1  # contador para gerar IDs únicos para os insumos

    def save(self, entity: Insumo) -> None:
        """Salva um insumo no repositório, usando o ID do insumo como chave no
        dicionário"""
        ## Se o usuário tentar passar um objeto que JÁ tem ID, o programa barra
        if entity.id is not None:
            raise ValueError(
                "Não é possível salvar um insumo com ID já definido,"
                "ele já é gerado pelo repositório."
            )

        # Define o ID gerado no objeto
        entity._definir_id_persistencia(self._proximo_id)

        self._dados[self._proximo_id] = entity
        self._proximo_id += 1  # incrementa o contador para o próximo ID

    def update(self, entity: Insumo) -> None:
        """Atualiza um insumo existente no repositório, verificando se o ID do insumo
        existe no dicionário"""
        if entity.id is None:
            raise ValueError("Não é possível atualizar um insumo sem ID.")
        if entity.id not in self._dados:
            raise ValueError(f"Não existe um insumo com ID {entity.id} para atualizar.")
        self._dados[entity.id] = entity

    def get(self, id: Any) -> Insumo | None:
        """Recupera um insumo pelo ID. Retorna None se não existir."""
        return self._dados.get(id)

    def list(self) -> list[Insumo]:
        """Retorna uma lista com todos os insumos no repositório"""
        return list(self._dados.values())

    def delete(self, id: int) -> None:
        """Remove um insumo do repositório pelo ID, lançando um erro se o ID
        não existir"""
        if id not in self._dados:
            raise ValueError(f"Não existe um insumo com ID {id} para remover.")
        del self._dados[id]


class RepositorioInsumoDB(RepositorioInsumo):
    """Implementação de RepositorioInsumo com persistência em arquivo JSON."""

    def __init__(self, path: Path) -> None:
        super().__init__()
        self._path = Path(path)
        # Se o arquivo não existir, inicializa um JSON vazio estruturado
        if not self._path.exists():
            self._salvar_arquivo({"proximo_id": 1, "dados": {}})

    def _ler_arquivo(self) -> dict:
        """Método auxiliar para ler o arquivo JSON e carregar o estado atual."""
        with open(self._path, encoding="utf-8") as f:
            return json.load(f)

    def _salvar_arquivo(self, estado: dict) -> None:
        """Método auxiliar para descarregar o estado atual no arquivo JSON."""
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(estado, f, indent=4, ensure_ascii=False)

    def _carregar_dados_em_memoria(self) -> None:
        """Lê o arquivo JSON e reconstrói os objetos de domínio na memória RAM

        da classe pai (self._dados e self._proximo_id).
        """
        estado = self._ler_arquivo()
        self._proximo_id = estado["proximo_id"]
        self._dados = {}

        for id_str, dados_insumo in estado["dados"].items():
            id_int = int(id_str)

            # POLIMORFISMO: Identifica se é HomemHora ou Ingrediente pelos
            # atributos presentes
            if "unidade" in dados_insumo:
                entity = Ingrediente(
                    nome=dados_insumo["nome"],
                    unidade=dados_insumo["unidade"],
                    quantidade=dados_insumo["quantidade"],
                    preco_base=dados_insumo["preco_base"],
                    id=id_int,
                )
            else:
                entity = HomemHora(
                    nome=dados_insumo["nome"],
                    quantidade=dados_insumo["quantidade"],
                    preco_base=dados_insumo["preco_base"],
                    id=id_int,
                )
            self._dados[id_int] = entity

    def _salvar_dados_do_modelo(self) -> None:
        """Pega o dicionário de objetos da memória RAM e exporta no formato

        bruto para o arquivo JSON.
        """
        dados_json = {}
        for id_int, entity in self._dados.items():
            # Estrutura base de qualquer Insumo
            info = {
                "nome": entity.nome,
                "quantidade": entity.quantidade,
                "preco_base": entity.preco_base,
            }
            # Se for Ingrediente, adicionamos o campo específico 'unidade'
            if hasattr(entity, "unidade"):
                info["unidade"] = entity.unidade

            dados_json[str(id_int)] = info

        estado = {"proximo_id": self._proximo_id, "dados": dados_json}
        self._salvar_arquivo(estado)

    # ──────────────────────────────────────────────────────────────────────────
    # SOBREESCRITA DOS MÉTODOS CRUD
    # Sincronizam a memória RAM com o arquivo JSON em cada operação
    # ──────────────────────────────────────────────────────────────────────────

    def save(self, entity: Insumo) -> None:
        self._carregar_dados_em_memoria()
        super().save(entity)  # Executa a lógica de validação e incremento do pai
        self._salvar_dados_do_modelo()

    def update(self, entity: Insumo) -> None:
        self._carregar_dados_em_memoria()
        super().update(entity)  # Executa as validações do pai
        self._salvar_dados_do_modelo()

    def get(self, id: Any) -> Insumo | None:
        self._carregar_dados_em_memoria()
        return super().get(id)

    def list(self) -> list[Insumo]:
        self._carregar_dados_em_memoria()
        return super().list()

    def delete(self, id: int) -> None:
        self._carregar_dados_em_memoria()
        super().delete(id)
        self._salvar_dados_do_modelo()
