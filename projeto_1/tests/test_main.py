from projeto_1.main import hello


def test_hello_default():
    assert hello() == "Olá, mundo!"


def test_hello_custom():
    assert hello("Pedro") == "Olá, Pedro!"
