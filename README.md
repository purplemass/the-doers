# The Doers project

## Pre-requisites

### Prompts for LLMS

1. Can you give me some guidelines on how to best start a new project in Python? Please include things like tools to use, which version of Python, project structure etc

2. I'd like to build an application in Python that has this structure:

- it has one manager and many workers
- the manager's job is to spawn workers when needed
- it is only possible to communicate with the application (or manager) using a worker - this is called the input worker
- a job is given to the manager via the input worker
- the input worker has a prompt in Terminal - a task or job is given via this prompt
- other workers can have various tasks like database worker (reads and write to the DB), file worker (has access to the file system and can make/edit/delete files) etc
- a worker is only needed if the job requires it - this decision is made by the manager
- we'd like to use an LLM like Gemini/ChatGPT for the decision making tasks that the manage has to undertake
