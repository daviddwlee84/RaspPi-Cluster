from tasks.cpu_tasks import heavy_computation
from tasks.io_tasks import download_page

heavy_computation.delay(10_000_000)     # Sent to CPU worker
download_page.delay('https://example.com')  # Sent to IO worker