import multiprocessing
from utils import print_start_end

def process_task(name):
    print_start_end(name)

def run_processes():
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=process_task, args=(f"Proceso-{i+1}",))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    print("=== Ejecutando con Processes ===")
    run_processes()