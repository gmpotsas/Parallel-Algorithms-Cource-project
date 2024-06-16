import threading

class OddEvenTranspositionSort:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.lock = threading.Lock()

    def sort(self):
        threads = []
        for phase in range(self.n):
            # Create a thread for each phase
            if phase % 2 == 0:
                thread = threading.Thread(target=self.even_phase)
            else:
                thread = threading.Thread(target=self.odd_phase)
            threads.append(thread)
            thread.start()

            # Ensure that the current phase completes before starting the next one
            for t in threads:
                t.join()
            threads.clear()  # Clear the threads list for the next phase

    def even_phase(self):
        for i in range(0, self.n - 1, 2):
            self.compare_and_swap(i, i + 1)

    def odd_phase(self):
        for i in range(1, self.n - 1, 2):
            self.compare_and_swap(i, i + 1)

    def compare_and_swap(self, i, j):
        with self.lock:
            if self.arr[i] > self.arr[j]:
                self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

    def get_sorted_array(self):
        return self.arr

# Example usage
if __name__ == "__main__":
    array = [5, 3, 2, 8, 1, 4]
    sorter = OddEvenTranspositionSort(array)
    sorter.sort()
    print("Sorted array:", sorter.get_sorted_array())
