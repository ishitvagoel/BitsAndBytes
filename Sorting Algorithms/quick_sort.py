# Quick Sort

import random

def quickSort(array, beginning, end):
  if beginning > end:
    return array
  partition_index = partition(array, beginning, end)
  quickSort(array, beginning, partition_index - 1)
  quickSort(array, partition_index + 1, end)
  return array

def partition(array, beginning, end):
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
