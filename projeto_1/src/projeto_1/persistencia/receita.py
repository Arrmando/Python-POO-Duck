import json
from pathlib import Path
from typing import Any

from src.projeto_1.dominio.receita import ItemReceita, Receita
from src.projeto_1.persistencia.base import Repositorio
from src.projeto_1.persistencia.insumo import RepositorioInsumo


class RepositorioReceita(Repositorio):
    """Implementação concreta de Repositorio para entidades Receita em memória com
    ID incremental."""

    def __init__(self) -> None:
        self._dados: dict[int, Receita] = {}
        self._proximo_id = 1

    def save(self, entity: Receita) -> None:
        """Salva uma nova receita gerando um ID incremental automaticamente."""
        if entity.id is not None:
            raise ValueError(
                "Não é possível salvar uma receita com ID já definido, "
                "ele já é gerado pelo repositório."
            )

        # Injeta o ID incremental diretamente no atributo privado da Receita
        setattr(entity, "_id", self._proximo_id)

        self._dados[self._proximo_id] = entity
        self._proximo_id += 1

    def update(self, entity: Receita) -> None:
        """Atualiza uma receita existente."""
        if entity.id is None:
            raise ValueError("Não é possível atualizar uma receita sem ID.")
        if entity.id not in self._dados:
            raise ValueError(
                f"Não existe uma receita com ID {entity.id} para atualizar."
            )
        self._dados[entity.id] = entity

    def get(self, id: Any) -> Receita | None:
        """Recupera uma receita pelo ID. Retorna None se não existir."""
        return self._dados.get(id)

    def list(self) -> list[Receita]:
        """Retorna uma lista com todas as receitas armazenadas."""
        return list(self._dados.values())

    def delete(self, id: int) -> None:
        """Remove uma receita pelo ID."""
        if id not in self._dados:
            raise ValueError(f"Não existe uma receita com ID {id} para remover.")
        del self._dados[id]


class RepositorioReceitaDB(RepositorioReceita):
    """Implementação de RepositorioReceita com persistência em arquivo JSON."""

    def __init__(self, path: Path, repo_insumo: RepositorioInsumo) -> None:
        super().__init__()
        self._path = Path(path)
        self._repo_insumo = repo_insumo

        # Se o arquivo não existir, inicializa a estrutura básica do JSON
        if not self._path.exists():
            self._salvar_arquivo({"proximo_id": 1, "dados": {}})

    def _ler_arquivo(self) -> dict:
        with open(self._path, encoding="utf-8") as f:
            return json.load(f)

    def _salvar_arquivo(self, estado: dict) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(estado, f, indent=4, ensure_ascii=False)

    def _carregar_dados_em_memoria(self) -> None:
        """Lê o arquivo JSON e reconstrói as Receitas e seus respectivos

        ItemReceita na memória RAM, buscando os Insumos pelo ID.
        """
        estado = self._ler_arquivo()
        self._proximo_id = estado["proximo_id"]
        self._dados = {}

        for id_str, dados_receita in estado["dados"].items():
            id_int = int(id_str)

            # 1. Reconstrói a estrutura básica da Receita
            receita = Receita(
                id=id_int,
                nome=dados_receita["nome"],
                instrucoes=dados_receita["instrucoes"],
            )

            # 2. Reconstrói a lista de itens agregados
            for item_dados in dados_receita["itens"]:
                insumo_id = item_dados["insumo_id"]
                coeficiente = item_dados["coeficiente"]

                # Busca o Insumo atualizado no repositório dele (Relacionamento!)
                insumo_real = self._repo_insumo.get(insumo_id)
                if insumo_real is not None:
                    item_receita = ItemReceita(
                        insumo=insumo_real, coeficiente=coeficiente
                    )
                    receita.adicionar_item(item_receita)

            self._dados[id_int] = receita

    def _salvar_dados_do_modelo(self) -> None:
        """Exporta as Receitas da memória RAM para o formato estruturado do JSON,

        salvando apenas as referências (IDs) dos Insumos.
        """
        dados_json = {}
        for id_int, receita in self._dados.items():
            # Transforma a lista de objetos ItemReceita em dados brutos (dicionários)
            lista_itens_json = []
            for item in receita.itens:
                lista_itens_json.append(
                    {
                        "insumo_id": item.insumo.id,  # Salva apenas a referência do ID
                        "coeficiente": item.coeficiente,
                    }
                )

            dados_json[str(id_int)] = {
                "nome": receita.nome,
                "instrucoes": receita.instrucoes,
                "itens": lista_itens_json,
            }

        estado = {"proximo_id": self._proximo_id, "dados": dados_json}
        self._salvar_arquivo(estado)

    # ──────────────────────────────────────────────────────────────────────────
    # REESCRITA DOS MÉTODOS CRUD (Sincronização com o JSON)
    # ──────────────────────────────────────────────────────────────────────────

    def save(self, entity: Receita) -> None:
        self._carregar_dados_em_memoria()
        super().save(entity)  # Executa a clonagem segura/adultos consentidos do pai
        self._salvar_dados_do_modelo()

    def update(self, entity: Receita) -> None:
        self._carregar_dados_em_memoria()
        super().update(entity)
        self._salvar_dados_do_modelo()

    def get(self, id: Any) -> Receita | None:
        self._carregar_dados_em_memoria()
        return super().get(id)

    def list(self) -> list[Receita]:
        self._carregar_dados_em_memoria()
        return super().list()

    def delete(self, id: int) -> None:
        self._carregar_dados_em_memoria()
        super().delete(id)
        self._salvar_dados_do_modelo()
