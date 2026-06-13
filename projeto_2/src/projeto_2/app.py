from projeto_2.view.janela import JanelaView
from projeto_2.controller.tela_controller import TelaController


def run():
    largura, altura = 800, 600
    janela = JanelaView(largura, altura)
    controller = TelaController(largura, altura)
    controller.run(janela)


if __name__ == "__main__":
    run()
