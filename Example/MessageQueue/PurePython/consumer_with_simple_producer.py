import multiprocessing
import time


def consumer(q):
    while True:
        item = q.get()
        if item is None:  # Exit condition
            break
        print(f"Consumed: {item}")
        time.sleep(2)  # Simulate work


if __name__ == "__main__":
    q = multiprocessing.Queue()
    consumer_process = multiprocessing.Process(target=consumer, args=(q,))
    consumer_process.start()

    # Producer code can be integrated here or run separately
    for i in range(10):
        item = f"message {i}"
        q.put(item)
        print(f"Produced: {item}")
        time.sleep(1)  # Simulate work

    # Stop the consumer
    q.put(None)
    consumer_process.join()
