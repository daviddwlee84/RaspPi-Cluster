from tasks.cpu_tasks import heavy_computation
from tasks.io_tasks import download_page
import time

# Submit tasks and get their AsyncResult objects
cpu_task = heavy_computation.delay(10_000_000)
io_task = download_page.delay('https://example.com')

print("Tasks submitted...")
print(f"CPU Task ID: {cpu_task.id}")
print(f"IO Task ID: {io_task.id}")

# Wait and check results
max_wait = 30  # seconds
start_time = time.time()

while time.time() - start_time < max_wait:
    cpu_ready = cpu_task.ready()
    io_ready = io_task.ready()
    
    print(f"\nTime elapsed: {time.time() - start_time:.1f}s")
    print(f"CPU task status: {'DONE' if cpu_ready else 'PENDING'}")
    print(f"IO task status: {'DONE' if io_ready else 'PENDING'}")
    
    if cpu_ready and io_ready:
        print("\nAll tasks completed!")
        
        # Safe result retrieval with error handling
        try:
            cpu_result = cpu_task.result
            print(f"CPU task result: {cpu_result}")
        except Exception as e:
            print(f"Error getting CPU result: {e}")
            
        try:
            io_result = io_task.result
            if isinstance(io_result, str):
                print(f"IO task result length: {len(io_result)} characters")
            else:
                print(f"IO task result type: {type(io_result)}")
        except Exception as e:
            print(f"Error getting IO result: {e}")
        
        break
        
    time.sleep(2)
else:
    print("\nTimeout waiting for tasks to complete")
    print(f"CPU task ready: {cpu_task.ready()}")
    print(f"IO task ready: {io_task.ready()}") 