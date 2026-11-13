import threading
import time

# Dados
N = 5
garfos = [threading.Lock() for _ in range(N)]

# >> evita bagunça das mensagens no terminal <<
trava_print = threading.Lock()

def mostrar(filosofo, mensagem):
    with trava_print:
        print(f"Filósofo {filosofo + 1}: {mensagem}", flush=True)

def garfos_filosofo(p):
    esquerdo = (p - 1) % N
    direito = p
    return esquerdo, direito

# --------------------------
# V1: INGENUA (com deadlock)
# --------------------------

barreira = threading.Barrier(N) # serve pra reproduzir de forma previsível e garante o ciclo

def filosofo_ingenuo(p):
    mostrar(p, "pensando")
    time.sleep(0.1)

    mostrar(p, "com fome")

    esquerdo, direito = garfos_filosofo(p)

    garfos[esquerdo].acquire()
    mostrar(p, f"pegou garfo {esquerdo}")

    # Espera todos pegarem o primeiro garfo
    barreira.wait()

    mostrar(p, f"esperando garfo {direito}")
    garfos[direito].acquire()

    mostrar(p, "comendo")
    time.sleep(0.1)

    garfos[direito].release()
    garfos[esquerdo].release()

def executar_ingenuo():
    threads = []

    for p in range(N):
        thread = threading.Thread(
            target=filosofo_ingenuo,
            args=(p,),
            daemon=True
        )
        threads.append(thread)
        thread.start()

    time.sleep(1)

    if any(t.is_alive() for t in threads):
        print("\nDEADLOCK DETECTADO!")
        print("Os filósofos estão aguardando garfos.")

# --------------
# V2: CORRIGIDA
# --------------

# Controle pra garantir que os pedidos sejam atendidos na ordem
condicao = threading.Condition()
proxima_senha = 0
senha_atual = 0

def pegar_garfos(p):
    global proxima_senha, senha_atual

    with condicao:
        minha_senha = proxima_senha
        proxima_senha += 1

        while minha_senha != senha_atual:
            condicao.wait()

    esquerdo, direito = garfos_filosofo(p)

    # Hierarquia: MENOR índice primeiro
    primeiro = min(esquerdo, direito)
    segundo = max(esquerdo, direito)

    garfos[primeiro].acquire()
    garfos[segundo].acquire()

    # Libera o próximo pedido da fila
    with condicao:
        senha_atual += 1
        condicao.notify_all()

    return primeiro, segundo

def filosofo_corrigido(p):
    for rodada in range(3):
        mostrar(p, "pensando")
        time.sleep(0.05)

        mostrar(p, "com fome")

        primeiro, segundo = pegar_garfos(p)

        try:
            mostrar(p, "comendo")
            time.sleep(0.1)
        finally:
            garfos[segundo].release()
            garfos[primeiro].release()

    mostrar(p, "terminou suas 3 refeições")

def executar_corrigido():
    threads = []

    for p in range(N):
        thread = threading.Thread(
            target=filosofo_corrigido,
            args=(p,)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\nTodos os filósofos terminaram de comer e pensar! :)")

# PRINCIPAL

print("JANTAR DOS FILÓSOFOS")
print("1 - Versão ingênua")
print("2 - Versão corrigida")

opcao = input("Escolha uma opção: ")

if opcao == "1":
    executar_ingenuo()
elif opcao == "2":
    executar_corrigido()
else:
    print("Opção inválida")