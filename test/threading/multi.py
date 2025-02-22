import multiprocessing
import time

def task_1():
    print("Task 1 started")
    time.sleep(3)
    print("Task 1 finished")

def task_2():
    print("Task 2 started")
    time.sleep(2)
    print("Task 2 finished")

# Create processes
p1 = multiprocessing.Process(target=task_1)
p2 = multiprocessing.Process(target=task_2)

# Start processes
p1.start()
p2.start()

# Wait for processes to finish
p1.join()
p2.join()

print("All tasks completed")
