"""Compare merge sort, insertion sort, and Python's Timsort."""

import random
import timeit
# Callable is a type hint that represents a callable object, such as a function or method. It allows you to specify the
# expected signature of the callable, including the types of its arguments and return value.
from collections.abc import Callable


def insertion_sort(values: list[int]) -> list[int]:
    """Return a sorted copy using insertion sort."""
    # Create a copy of the input list to avoid modifying the original list.
    result = values.copy()
    # Iterate over the indices of the list starting from the second element (index 1) to the last element.
    for index in range(1, len(result)):
        # Store the current value to be inserted into the sorted portion of the list.
        current = result[index]
        # Initialize a variable to track the position where the current value should be inserted.
        position = index - 1
        # Use a while loop until result[position] is less than or equal to current or position is less than 0.
        while position >= 0 and result[position] > current:
            # Shift the element at position to the right to make room for the current value.
            result[position + 1] = result[position]
            # Decrement the position to continue checking the previous elements in the sorted portion of the list.
            position -= 1
        # Insert the current value into its correct position in the sorted portion of the list.
        result[position + 1] = current
    return result


def merge_sort(values: list[int]) -> list[int]:
    """Return a sorted copy using recursive merge sort."""
    # If the input list has one or zero elements, it is already sorted, so return a copy of it.
    if len(values) <= 1:
        return values.copy()

    # Split the input list into two halves for recursive sorting.
    middle = len(values) // 2
    # Recursively sort the left half of the list.
    left = merge_sort(values[:middle])
    # Recursively sort the right half of the list.
    right = merge_sort(values[middle:])
    # Create an empty list to hold the merged and sorted result of the two halves.
    merged: list[int] = []
    # Initialize indices for iterating through the left and right halves of the list.
    left_index = right_index = 0

    # Use a while loop until the end of either the left or right half is reached.
    while left_index < len(left) and right_index < len(right):
        # if the current element in the left half is less than or equal to the current element in the right half.
        if left[left_index] <= right[right_index]:
            # Append the current element from the left half to the merged list.
            merged.append(left[left_index])
            # Increment the index for the left half to move to the next element.
            left_index += 1
        else:
            # Append the current element from the right half to the merged list.
            merged.append(right[right_index])
            # Increment the index for the right half to move to the next element.
            right_index += 1

    # After the while loop, one of the halves may still have remaining elements.
    # Append any remaining elements from the left and right halves to the merged list.
    return merged + left[left_index:] + right[right_index:]


def benchmark(
    algorithm: Callable[[list[int]], list[int]],
    values: list[int],
    repetitions: int = 3,
) -> float:
    """Return the best execution time for one input set."""
    # timeit.Timer is a class that provides a way to measure the execution time of small code snippets. It allows you
    # specify a callable (function) and the number of times to execute it, and it returns the total time taken for those
    # executions.
    timer = timeit.Timer(lambda: algorithm(values))
    # The repeat method of the Timer class runs the specified code multiple times and returns a list of execution times.
    # number=1 means that each repetition will execute code only once, and repeat=repetitions specifies how many times
    return min(timer.repeat(repeat=repetitions, number=1))


def main() -> None:
    """Measure algorithms on random, sorted, and reversed data."""
    # Set the seed for the random number generator. By setting a specific seed value (in this case, 42),
    random.seed(42)
    # Define a dictionary that maps algorithm names to their corresponding sorting functions.
    algorithms = {
        "Insertion sort": insertion_sort,
        "Merge sort": merge_sort,
        "Timsort (sorted)": sorted,
    }
    # Define a list of dataset sizes to test the sorting algorithms on. Represent the number of elements in the datasets
    sizes = (100, 1_000, 5_000)

    # Print the header for the output table, including the dataset name, size, and algorithm names.
    print(f"{'Data set':<12} {'Size':>6} " + " ".join(
        f"{name:>20}" for name in algorithms
    ))
    # Iterate over each dataset size to generate random, sorted, and reversed datasets for benchmarking.
    for size in sizes:
        # Generate a list of random integers between 0 and size (inclusive) with the specified size.
        random_values = [random.randint(0, size) for _ in range(size)]
        # Create a dictionary that maps dataset names to their corresponding datasets (random, sorted, and reversed).
        datasets = {
            "random": random_values,
            "sorted": sorted(random_values),
            "reversed": sorted(random_values, reverse=True),
        }
        # Iterate over each dataset and benchmark the sorting algorithms.
        for data_name, values in datasets.items():
            # Measure the execution time of each sorting algorithm on the current dataset and format the results.
            timings = [
                f"{benchmark(algorithm, values):.6f}s"
                for algorithm in algorithms.values()
            ]
            # Print the dataset name, size, and execution times for each sorting algorithm in a formatted manner.
            print(f"{data_name:<12} {size:>6} " + " ".join(
                f"{timing:>20}" for timing in timings
            ))


# The following code is executed when the script is run directly (not imported as a module).
if __name__ == "__main__":
    main()

"""
Data set       Size       Insertion sort           Merge sort     Timsort (sorted)
random          100            0.000165s            0.000145s            0.000005s
sorted          100            0.000009s            0.000099s            0.000001s
reversed        100            0.000317s            0.000111s            0.000002s
random         1000            0.021169s            0.002011s            0.000095s
sorted         1000            0.000106s            0.001283s            0.000008s
reversed       1000            0.041370s            0.001441s            0.000014s
random         5000            0.573972s            0.011670s            0.000759s
sorted         5000            0.000554s            0.007316s            0.000039s
reversed       5000            1.110556s            0.008386s            0.000098s

The results show that Timsort (Python's built-in sorted function) consistently outperforms both insertion sort and merge
sort across all dataset sizes and types. Insertion sort performs well on small datasets but becomes inefficient on
larger datasets, especially with reversed data. Merge sort maintains a more consistent performance but is still slower
than Timsort. Overall, Timsort is the most efficient sorting algorithm among the three tested.
"""
