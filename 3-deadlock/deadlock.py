import threading
import time

def deadlock():
    lock_a = threading.Lock()
    lock_b = threading.Lock()

    def tarefa(nome, primeiro, segundo, primeiroLock, segundoLock):
        primeiro.acquire()
        print(f"{nome}: adquiriu {primeiroLock}", flush=True)
        
        time.sleep(0.05)
        print(f"{nome}: aguardando {segundoLock}", flush=True)
        
        segundo.acquire()
        print(f"{nome}: adquiriu {segundoLock}", flush=True)

        print(f"{nome}: concluiu", flush=True)
        
        segundo.release()
        primeiro.release()

    t1 = threading.Thread(target=tarefa, args=("T1", lock_a, lock_b, "A", "B"), daemon=True)
    t2 = threading.Thread(target=tarefa, args=("T2", lock_b, lock_a, "B", "A"), daemon=True)

    t1.start()
    t2.start()
    t1.join(timeout=5)
    t2.join(timeout=5)

    if t1.is_alive() and t2.is_alive():
        print("DEADLOCK OBSERVADO: T1 e T2 permanecem bloqueadas")

def correcao_deadlock():
    lock_a = threading.Lock()
    lock_b = threading.Lock()

    def tarefa(nome):
        lock_a.acquire()
        print(f"{nome}: adquiriu Lock A", flush=True)
        
        time.sleep(0.05)
            
        lock_b.acquire()
        print(f"{nome}: adquiriu Lock B", flush=True)

        print(f"{nome}: concluiu", flush=True)
        
        lock_b.release()
        lock_a.release()

    t1 = threading.Thread(target=tarefa, args=("T1",), daemon=True)
    t2 = threading.Thread(target=tarefa, args=("T2",), daemon=True)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("CORREÇÃO: T1 e T2 foram concluídas sem deadlock")

def main():
    while True:
        print("\nMenu Teste Deadlock:")
        print("1 - Demonstrar deadlock")
        print("2 - Demonstrar correção do deadlock")
        print("3 - Sair")
        opcao = int(input("Escolha uma opção: "))
        print("\n")
        
        if opcao == 1:
            deadlock()
        elif opcao == 2:
            correcao_deadlock()
        elif opcao == 3:
            print("Saindo...")
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
 main()
