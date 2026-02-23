import threading
from utils import print_start_end

def thread_task(name):
    print_start_end(name)

def run_threads():
    threads = []
    for i in range(5):
        t = threading.Thread(target=thread_task, args=(f"Hilo-{i+1}",))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    print("=== Ejecutando con Threads ===")
    run_threads()