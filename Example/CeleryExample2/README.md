# Celery setup for Mix of CPU intensive tasks and I/O intensive tasks

- [Concurrency — Celery 5.4.0 documentation](https://docs.celeryq.dev/en/stable/userguide/concurrency/index.html)
- [Python Celery vs Python RQ for Distributed Tasks Processing | by Lal Zada | Python in Plain English](https://python.plainenglish.io/python-celery-vs-python-rq-for-distributed-tasks-processing-20041c346e6)
  - [Scale up Messaging Queue with Python Celery (Processes vs Threads) — Part 1 | by Lal Zada | Python in Plain English](https://python.plainenglish.io/scale-up-messaging-queue-with-python-celery-processes-vs-threads-402533be269e)
  - [Handling I/O Bound Tasks with Python Celery using Processes vs Threads Pool — Part 2 | by Lal Zada | Python in Plain English](https://python.plainenglish.io/handling-i-o-bound-tasks-with-python-celery-using-processes-vs-threads-pool-126a4875600d)

## Setup and Run

### Using Docker (Recommended)

The easiest way to run this example is using Docker Compose:

```bash
# Start Redis and Celery workers
docker-compose up -d

# Run the main script to submit tasks
docker-compose exec celery-cpu-worker python main.py
```

### Manual Setup (macOS)

1. Install Redis:

```bash
brew install redis
```

2. Start Redis:

```bash
brew services start redis
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Run the workers:

```bash
# Run in separate terminals or use the run_workers.sh script
./run_workers.sh
```

5. Run the main application:

```bash
python main.py
```

## Project Structure

- `celery_app.py`: Celery application configuration
- `celery_config.py`: Defines Redis connection and task routing
- `tasks/`: Contains task definitions
  - `cpu_tasks.py`: CPU-bound tasks using prefork pool
  - `io_tasks.py`: I/O-bound tasks using eventlet pool
- `main.py`: Client code to submit tasks
- `run_workers.sh`: Shell script to start workers locally
- `docker-compose.yml`: Docker configuration with Redis and workers

---

Using Docker (recommended):

```bash
./run_with_docker.sh
```

Manual setup on macOS:

```bash
# Install Redis
brew install redis

# Start Redis
brew services start redis

# Install Python dependencies
pip install -r requirements.txt

# Start the workers
./run_workers.sh

# Run the tasks
python main.py

# Check task status
python check_tasks.py
```

---

```bash
$ docker compose exec celery-cpu-worker python main.py
$ docker compose exec celery-cpu-worker python check_tasks.py
Tasks submitted...
CPU Task ID: 55d4d84e-5e25-417d-a2ea-2841196f84cb
IO Task ID: 101bd268-94e7-47eb-9547-70600dbfc85c

Time elapsed: 0.0s
CPU task status: PENDING
IO task status: PENDING

Time elapsed: 2.0s
CPU task status: DONE
IO task status: DONE

All tasks completed!
CPU task result: 21081849486.439312
IO task result length: 1256 characters
```
