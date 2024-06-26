from threading import Thread
import time

class OddEvenTransSort:
    def __init__(self, arr):
        self.arr = arr.copy()
        self.N = len(arr)
        self.MAX_THREAD = int((self.N + 1) / 2)
        self.tmp = 0

    def compare(self):
        index = self.tmp
        self.tmp += 2
        if index + 1 < self.N and self.arr[index] > self.arr[index + 1]:
            self.arr[index], self.arr[index + 1] = self.arr[index + 1], self.arr[index]

    def create_threads(self):
        threads = [None] * self.MAX_THREAD

        for index in range(self.MAX_THREAD):
            threads[index] = Thread(target=self.compare)
            threads[index].start()

        for index in range(self.MAX_THREAD):
            threads[index].join()

    def odd_even_sort_parallel(self):
        for i in range(1, self.N + 1):
            if i % 2 == 1:  # Odd step
                self.tmp = 0
            else:  # Even step
                self.tmp = 1
            self.create_threads()
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