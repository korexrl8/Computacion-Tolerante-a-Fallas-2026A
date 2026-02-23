from threads_example import run_threads
from process_example import run_processes
import asyncio
from async_example import run_async

def main():
    print(">> THREADS")
    run_threads()

    print(">> PROCESSES")
    run_processes()

    print(">> ASYNCIO")
    asyncio.run(run_async())

if __name__ == "__main__":
    main()