broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/1'

task_routes = {
    'tasks.cpu_tasks.*': {'queue': 'cpu_queue'},
    'tasks.io_tasks.*': {'queue': 'io_queue'},
}