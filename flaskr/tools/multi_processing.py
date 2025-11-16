from multiprocessing import Pool, cpu_count, current_process
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import random

def threaded_worker(task):
    """Worker running inside a thread"""
    process_name = current_process().name
    thread_name = threading.current_thread().name
    print(f"[Process: {process_name}, Thread: {thread_name}] Processing task {task}")
    time.sleep(random.uniform(0.5, 1.5))  # simulate work
    return f"Task {task} done by {thread_name} in {process_name}"

def process_worker(task_batch):
    """Each process handles a batch of tasks using threads"""
    results = []
    with ThreadPoolExecutor(max_workers=2) as executor:  # 2 threads per process
        future_to_task = {executor.submit(threaded_worker, t): t for t in task_batch}
        for future in as_completed(future_to_task):
            results.append(future.result())
    return results

if __name__ == "__main__":
    max_processes = cpu_count()
    print(f"Running up to {max_processes} processes, each with 2 threads:\n")

    # Simulate a large number of tasks (50 tasks)
    tasks = range(50)

    # Function to batch tasks
    def batched(iterable, n):
        it = iter(iterable)
        while True:
            batch = []
            try:
                for _ in range(n):
                    batch.append(next(it))
            except StopIteration:
                if batch:
                    yield batch
                break
            yield batch

    # Run process pool
    with Pool(processes=max_processes) as pool:
        for batch_result in pool.imap_unordered(process_worker, batched(tasks, 2), chunksize=1):
            for r in batch_result:
                print(r)
    print("All tasks completed.")
