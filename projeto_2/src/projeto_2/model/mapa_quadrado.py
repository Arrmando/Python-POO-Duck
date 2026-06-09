from .celula import Celula
from .bomba import Bomba
from typing import List


class MapaQuadrado:
    def __init__(self, colunas: int, linhas: int):
        self._colunas = colunas
        self._linhas = linhas
        self._mapa: List[List[Celula]] = self._gerar_mapa()

    def _gerar_mapa(self) -> List[List[Celula]]:
        """Gera uma matriz de células escondidas (status=True)."""
        mapa = []
        for y in range(self._linhas):
            linha = []
            for x in range(self._colunas):
                address = y * self._colunas + x
                linha.append(Celula(address=address, status=True))
            mapa.append(linha)
        return mapa

    @property
    def mapa(self) -> List[List[Celula]]:
        return self._mapa

    @property
    def colunas(self) -> int:
        return self._colunas

    @property
    def linhas(self) -> int:
        return self._linhas

    def obter_celula(self, x: int, y: int) -> Celula | None:
        if 0 <= x < self._colunas and 0 <= y < self._linhas:
            return self._mapa[y][x]
        return None

    def contar_bombas_vizinhas(self):
        """
        Calcula a quantidade de bombas vizinhas para cada célula do mapa.
        """
        for y in range(self._linhas):
            for x in range(self._colunas):
                celula = self.obter_celula(x, y)
                if celula:
                    bombas = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            
                            vizinha = self.obter_celula(x + dx, y + dy)
                            if vizinha and vizinha.obter_entidade(Bomba):
                                bombas += 1
                    
                    celula.valor = bombas

    def revelar(self, x: int, y: int) -> bool:
        """
        Revela a célula na posição [x, y].
        Se o valor da célula for 0, revela recursivamente as vizinhas.
        Retorna True se a célula revelada contiver uma bomba.
        """
        celula = self.obter_celula(x, y)
        
        if not celula or not celula.status:
            return False
            
        celula.cavar() # Define status como False
        
        # Se encontrou uma bomba, retorna True imediatamente
        if celula.obter_entidade(Bomba):
            return True
            
        # Se for uma célula vazia (valor 0), revela vizinhos recursivamente
        if celula.valor == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    self.revelar(x + dx, y + dy)
        
        return False
