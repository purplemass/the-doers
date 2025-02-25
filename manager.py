import multiprocessing

from workers.input_worker import InputWorker
from workers.db_worker import DatabaseWorker
from workers.file_worker import FileWorker
from llm.llm_client import LLMClient


class Manager:
    def __init__(self):
        self.task_queue = multiprocessing.Queue()
        self.results_queue = multiprocessing.Queue()
        self.llm_client = LLMClient()

    def start_input_worker(self):
        input_worker = InputWorker(self.task_queue)
        input_worker.start()

    def process_tasks(self):
        while True:
            task = self.task_queue.get()  # Blocking call
            print(f"Manager received task: {task}")

            # Use LLM to decide which worker(s) to spawn
            decision = self.llm_client.decide(task)
            print(f"LLM Decision: {decision}")

            if decision == "database":
                worker = DatabaseWorker(task, self.results_queue)
            elif decision == "file":
                worker = FileWorker(task, self.results_queue)
            else:
                print(f"No worker available for task: {task}")
                continue

            worker.start()


if __name__ == "__main__":
    manager = Manager()
    manager.start_input_worker()
    manager.process_tasks()
