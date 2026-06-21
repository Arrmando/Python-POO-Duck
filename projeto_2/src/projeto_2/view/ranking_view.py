import pygame

from projeto_2.persistencia.ranking_db import RepositorioRankingJSON


class GameRankingView:
    def __init__(self, screen, largura: int, altura: int):
        self.screen = screen
        self.largura = largura
        self.altura = altura

        # lê o arquivo "ranking.json" que fica na raiz do projeto
        self.repo = RepositorioRankingJSON()

        # Definição de Cores
        self.COR_FUNDO = (40, 40, 40)  # Cinza escuro
        self.COR_TEXTO = (255, 255, 255)  # Branco
        self.COR_DESTAQUE = (76, 175, 80)  # Verde igual ao botão "MÉDIO" do seu print
        self.COR_LINHA = (100, 100, 100)  # Cinza claro para as linhas

        # Configuração das Fontes
        self.fonte_titulo = pygame.font.SysFont("Arial", 40, bold=True)
        self.fonte_subtitulo = pygame.font.SysFont("Arial", 24, italic=True)
        self.fonte_dados = pygame.font.SysFont("Arial", 28)

    def desenhar(self, dificuldade_atual: str = "Médio"):
        """Desenha a tela de ranking puxando os dados reais do JSON."""
        # 1. Limpa a tela com o fundo escuro
        self.screen.fill(self.COR_FUNDO)

        # 2. Desenha o Título principal e a dificuldade
        texto_titulo = self.fonte_titulo.render(
            "RECORDES - TOP 10", True, self.COR_DESTAQUE
        )
        texto_sub = self.fonte_subtitulo.render(
            f"Dificuldade: {dificuldade_atual.upper()}", True, self.COR_TEXTO
        )

        self.screen.blit(
            texto_titulo, (self.largura // 2 - texto_titulo.get_width() // 2, 40)
        )
        self.screen.blit(
            texto_sub, (self.largura // 2 - texto_sub.get_width() // 2, 90)
        )

        # 3. Busca os 10 melhores tempos do seu arquivo JSON
        melhores = self.repo.listar_melhores(dificuldade_atual)

        posicao_y = 160

        if not melhores:
            texto_vazio = self.fonte_dados.render(
                "Nenhum recorde nesta dificuldade!", True, self.COR_LINHA
            )
            self.screen.blit(
                texto_vazio,
                (self.largura // 2 - texto_vazio.get_width() // 2, posicao_y + 50),
            )
        else:
            # 4. Loop para desenhar as linhas do placar (Apenas a posição e o tempo)
            for indice, registro in enumerate(melhores, start=1):
                tempo = registro["tempo_segundos"]

                # Formata a string (Ex: "1º Lugar .................... 14s")
                linha_texto = (
                    f"{indice}º Lugar .................................... {tempo}s"
                )

                texto_renderizado = self.fonte_dados.render(
                    linha_texto, True, self.COR_TEXTO
                )
                self.screen.blit(
                    texto_renderizado,
                    (self.largura // 2 - texto_renderizado.get_width() // 2, posicao_y),
                )

                posicao_y += 40  # Dá espaço para a próxima linha

        # 5. Instrução de rodapé para voltar ao jogo
        texto_voltar = self.fonte_subtitulo.render(
            "Pressione [ESC] para voltar ao menu", True, self.COR_LINHA
        )
        self.screen.blit(
            texto_voltar,
            (self.largura // 2 - texto_voltar.get_width() // 2, self.altura - 60),
        )
