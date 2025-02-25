import multiprocessing


class InputWorker(multiprocessing.Process):
    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue

    def run(self):
        while True:
            task = input("Enter a task: ")
            self.task_queue.put(task)
            print(f"Task '{task}' sent to manager")
