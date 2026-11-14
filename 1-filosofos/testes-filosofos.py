# Testes do Jantar dos Filosofos (Parte 1)
# Roda o filosofos.py em um subprocesso, escolhe a opcao do menu
# e confere a saida do terminal.
#
# Execucao (na raiz do repositorio):
#   python 1-filosofos/testes-filosofos.py

from pathlib import Path
import subprocess
import sys
import threading
import unicodedata

SCRIPT = Path(__file__).with_name("filosofos.py")
N = 5
REFEICOES = 3
RODADAS_CORRIGIDA = 10


def normalizar(texto):
    # tira acentos e deixa minusculo, pra comparar sem problema de encoding
    texto = unicodedata.normalize("NFKD", texto)
    return texto.encode("ascii", "ignore").decode("ascii").lower()


def executar(opcao):
    processo = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=f"{opcao}\n",
        text=True,
        encoding="utf-8",
        capture_output=True,
        timeout=15,
        check=True,
    )
    return normalizar(processo.stdout)


# ---------------------------------
# Teste 1: impasse na versao ingenua
# ---------------------------------
def testar_ingenua():
    saida = executar(1)

    assert "deadlock detectado" in saida
    # todos pegaram o primeiro garfo e ficaram esperando o segundo
    assert saida.count("pegou garfo") == N
    assert saida.count("esperando garfo") == N
    # ninguem conseguiu comer
    assert "comendo" not in saida

    print("[OK] Ingenua: 5 filosofos com 1 garfo, 5 esperando o segundo, deadlock detectado")


# ---------------------------------------------
# Teste 2: progresso e inanicao na versao corrigida
# ---------------------------------------------
def analisar_corrigida(saida):
    refeicoes = [0] * N
    maior_diferenca = 0

    for linha in saida.splitlines():
        if not linha.startswith("filosofo ") or ": comendo" not in linha:
            continue
        p = int(linha.split()[1].rstrip(":")) - 1
        refeicoes[p] += 1
        # diferenca entre quem comeu mais e quem comeu menos ate esse momento
        diferenca = max(refeicoes) - min(refeicoes)
        maior_diferenca = max(maior_diferenca, diferenca)

    return refeicoes, maior_diferenca


def testar_corrigida():
    diferencas = []

    for rodada in range(1, RODADAS_CORRIGIDA + 1):
        saida = executar(2)

        for p in range(1, N + 1):
            assert saida.count(f"filosofo {p}: comendo") == REFEICOES, f"filosofo {p} nao comeu 3 vezes"
            assert f"filosofo {p}: terminou suas 3 refeicoes" in saida, f"filosofo {p} nao terminou"
        assert "todos os filosofos terminaram" in saida
        assert "deadlock" not in saida

        refeicoes, maior_diferenca = analisar_corrigida(saida)
        diferencas.append(maior_diferenca)
        print(f"[OK] Corrigida rodada {rodada}/{RODADAS_CORRIGIDA}: refeicoes={refeicoes} "
              f"maior diferenca durante a execucao={maior_diferenca}")

    return diferencas


# -----------------------------------
# Teste 3: exclusao mutua do garfo (Lock)
# -----------------------------------
def testar_exclusao_mutua():
    garfo = threading.Lock()
    conseguiu = []

    garfo.acquire()  # um filosofo esta com o garfo

    def outro_filosofo():
        # tenta pegar sem esperar: tem que falhar enquanto o garfo esta ocupado
        conseguiu.append(garfo.acquire(blocking=False))

    t = threading.Thread(target=outro_filosofo)
    t.start()
    t.join()
    assert conseguiu == [False]

    garfo.release()  # devolveu o garfo
    assert garfo.acquire(blocking=False) is True
    garfo.release()

    print("[OK] Exclusao mutua: o Lock so deixa um filosofo segurar o garfo por vez")


if __name__ == "__main__":
    print("TESTES - JANTAR DOS FILOSOFOS\n")
    testar_exclusao_mutua()
    testar_ingenua()
    diferencas = testar_corrigida()

    print("\nRESUMO")
    print(f"Rodadas da versao corrigida: {RODADAS_CORRIGIDA}")
    print(f"Refeicoes conferidas: {RODADAS_CORRIGIDA * N * REFEICOES}")
    print(f"Maior diferenca de refeicoes entre filosofos (pior rodada): {max(diferencas)}")
    print("Deadlock na corrigida: 0 | Filosofo sem comer: 0")
    print("Testes concluidos.")
