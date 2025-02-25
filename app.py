import multiprocessing
# import queue
import time


class Manager:
    def __init__(self):
        self.worker_queues = {}  # Worker name -> queue
        self.llm_queue = multiprocessing.Queue()
        self.input_queue = multiprocessing.Queue()

    def register_worker(self, worker_name, queue):
        self.worker_queues[worker_name] = queue

    def get_llm_response(self, prompt):
        self.llm_queue.put(prompt)
        return self.llm_queue.get()

    def process_job(self, job):
        llm_prompt = (
            f"Given the job '{job}', which workers are needed?"
            f"(Choose from: file_worker, database_worker, none)")
        required_worker = self.get_llm_response(llm_prompt)

        if required_worker == "file_worker":
            self.worker_queues["file_worker"].put(f"Create file: {job}")
            result = self.worker_queues["file_worker"].get()
        elif required_worker == "database_worker":
            self.worker_queues["database_worker"].put(f"Process DB: {job}")
            result = self.worker_queues["database_worker"].get()
        else:
            result = f"No worker needed for: {job}"

        self.input_queue.put(result)  # Send result back to input worker


def input_worker(manage, shutdown_event):
    while not shutdown_event.is_set():  # Check for shutdown signal before input
        try:
            job = input("Enter job (or 'exit' to quit): ")
            if job.lower() == "exit":
                print(10 * 1)
                break  # Exit the loop if the user types "exit"
            manager.process_job(job)
            result = manager.input_queue.get()
            print(f"Result: {result}")
        except EOFError:
            break  # Exit loop if EOFError occurs


def file_worker(queue):
    while True:
        job = queue.get()
        print(f"File worker processing: {job}")
        time.sleep(1)  # Simulate work
        queue.put("File operation complete")


def database_worker(queue):
    while True:
        job = queue.get()
        print(f"Database worker processing: {job}")
        time.sleep(1)  # Simulate work
        queue.put("Database operation complete")


def llm_worker(queue):
    while True:
        prompt = queue.get()
        print(f"LLM received prompt: {prompt}")
        # Mock LLM response - replace with actual LLM API call
        if "file" in prompt.lower():
            response = "file_worker"
        elif "db" in prompt.lower() or "database" in prompt.lower():
            response = "database_worker"
        else:
            response = "none"
        queue.put(response)


if __name__ == "__main__":
    manager = Manager()

    file_queue = multiprocessing.Queue()
    db_queue = multiprocessing.Queue()

    manager.register_worker("file_worker", file_queue)
    manager.register_worker("database_worker", db_queue)

    shutdown_event = multiprocessing.Event()  # Create shutdown event

    processes = [
        multiprocessing.Process(target=input_worker, args=(manager, shutdown_event)),
        multiprocessing.Process(target=file_worker, args=(file_queue,)),
        multiprocessing.Process(target=database_worker, args=(db_queue,)),
        multiprocessing.Process(target=llm_worker, args=(manager.llm_queue,))
    ]

    for p in processes:
        p.start()

    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:  # Handle CTRL+C
        print("Shutting down...")
        shutdown_event.set()  # Signal workers to exit
        for p in processes:
            p.join()
