import multiprocessing


class BaseWorker(multiprocessing.Process):
    def __init__(self, task, results_queue):
        super().__init__()
        self.task = task
        self.results_queue = results_queue

    def run(self):
        result = self.execute_task(self.task)
        self.results_queue.put(result)

    def execute_task(self, task):
        raise NotImplementedError("Subclasses must implement this method")
