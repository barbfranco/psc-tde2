"""Experimento de contador concorrente com e sem semáforo binário"""

import threading
import time

threads = 8
incrementos = 200_000
repeticoes = 3


def executar(protegido: bool) -> tuple[int, float]:
    """Executa incrementos concorrentes e retorna o contador e o tempo"""
    contador = 0
    semaforo = threading.Semaphore(1)

    def tarefa() -> None:
        nonlocal contador

        for i in range(incrementos):
            if protegido:
                with semaforo:
                    contador += 1
            else:
                valor_anterior = contador

                # Cede a CPU pra tornar a janela de corrida observável
                if i % 1000 == 0:
                    time.sleep(0)

                contador = valor_anterior + 1

    inicio = time.perf_counter()

    workers = [
        threading.Thread(target=tarefa)
        for _ in range(threads)
    ]

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()

    duracao = time.perf_counter() - inicio
    return contador, duracao


def main() -> None:
    """Executa três medições para cada versão do contador"""
    esperado = threads * incrementos

    print(f"threads: {threads} | incrementos/thread: {incrementos}")
    print("Versao | Rodada | Esperado | Obtido | Tempo(s)")

    for protegido in (False, True):
        versao = "com semaforo" if protegido else "sem semaforo"

        for rodada in range(1, repeticoes + 1):
            obtido, tempo_s = executar(protegido)
            print(
                f"{versao} | {rodada} | {esperado} | "
                f"{obtido} | {tempo_s:.4f}"
            )


if __name__ == "__main__":
    main()
