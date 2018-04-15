# Quick Sort

import random

def quickSort(array, beginning, end):
  """Implementation of Quick Sort.

  Call eg: quickSort([1, 5, 7, 2, 0, -1], 0, 5)

  Args:
    array: The list which we need to sort.
    beginning: The starting index of the list in recursive call.
    end: The end index of the list in recursive call.

  Returns:
    List sorted in ascending order.
    eg: [-1, 0 , 1, 2, 5, 7]
  """
  if beginning > end:
    return array
  partition_index = partition(array, beginning, end)
  quickSort(array, beginning, partition_index - 1)
  quickSort(array, partition_index + 1, end)
  return array

def partition(array, beginning, end):
  """Utility method to perform Randomized Partitioning of a list.

  Call eg: partition([1, 5, 7, 2, 0, -1], 0, 5)

  Args:
    array: The list which we need to partition.
    beginning: The starting index of the list in recursive call.
    end: The end index of the list in recursive call.

  Returns:
    Index of the partition ie. the final position of the chosen pivot.
  """
  random_int = random.randint(beginning, end)
  array[end], array[random_int] = array[random_int], array[end]
  pivot = array[end]
  partition_index = beginning
  for offset in range(end - beginning):
    if array[beginning + offset] <= pivot:
      array[beginning + offset], array[partition_index] = array[partition_index], array[beginning + offset]
      partition_index += 1
  array[end], array[partition_index] = array[partition_index], array[end]
  return partition_index
