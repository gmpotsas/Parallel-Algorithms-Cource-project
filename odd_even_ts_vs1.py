from threading import Thread, Lock
import time
import logging

class OddEvenTransSort:
    def __init__(self, arr):
        self.arr = arr.copy()
        self.N = len(arr)
        self.lock = Lock()

        # Configure logging
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        self.logger = logging.getLogger()
        
        # To store the logs for visualization purposes
        self.logs = []

    def compare(self, index, phase):
        if index + 1 < self.N and self.arr[index] > self.arr[index + 1]:
            with self.lock:
                self.arr[index], self.arr[index + 1] = self.arr[index + 1], self.arr[index]
                self.logger.debug(f"Phase {phase}, Thread {index // 2}: swapping {self.arr[index]} and {self.arr[index + 1]}")
                self.logs.append((index // 2, index, index + 1, True))
        else:
            self.logger.debug(f"Phase {phase}, Thread {index // 2}: comparing {self.arr[index]} and {self.arr[index + 1]} - no swap")
            self.logs.append((index // 2, index, index + 1, False))

    def create_threads(self, start_index, phase):
        threads = []
        for i in range(start_index, self.N - 1, 2):
            thread = Thread(target=self.compare, args=(i, phase))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def odd_even_sort_parallel(self):
        for i in range(1, self.N + 1):
            if i % 2 == 1:  # Odd phase
                self.logger.debug(f"Odd phase {i}")
                self.create_threads(0, i)
            else:  # Even phase
                self.logger.debug(f"Even phase {i}")
                self.create_threads(1, i)
        return self.arr

    def odd_even_sort_sequential(self):
        arr = self.arr.copy()
        n = self.N
        is_sorted = False
        while not is_sorted:
            is_sorted = True
            for phase in range(2):
                start = phase % 2
                for i in range(start, n - 1, 2):
                    if arr[i] > arr[i + 1]:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]
                        is_sorted = False
        return arr

def compare_sorts(arr):
    sorter = OddEvenTransSort(arr)
    start_time = time.time()
    parallel_result = sorter.odd_even_sort_parallel()
    parallel_time = time.time() - start_time

    sorter = OddEvenTransSort(arr)  # Reinitialize to reset any state
    start_time = time.time()
    sequential_result = sorter.odd_even_sort_sequential()
    sequential_time = time.time() - start_time

    print("Original array: ", arr)
    print("Sequential sort result: ", sequential_result)
    print("Parallel sort result: ", parallel_result)
    print("Results match: ", sequential_result == parallel_result)
    print(f"Sequential sort time: {sequential_time:.6f} seconds")
    print(f"Parallel sort time: {parallel_time:.6f} seconds")


def get_user_input():
    arr = []
    print("Enter values to add to the array. Type 'done' to finish.")
    while True:
        user_input = input("Enter a value (or 'done' to finish): ")
        if user_input.lower() == 'done':
            break
        try:
            value = float(user_input)
            arr.append(value)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    return arr

# Example usage
user_array = get_user_input()
compare_sorts(user_array)


