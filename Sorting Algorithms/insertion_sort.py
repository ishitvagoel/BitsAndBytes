# Insertion Sort

def insertionSort(array):
  """Implementation of Insertion Sort.

  Call eg: insertionSort([1, 5, 7, 2, 0, -1])

  Args:
    array: The list which we need to sort.

  Returns:
    List sorted in ascending order.
    eg: [-1, 0 , 1, 2, 5, 7]
  """
  for outer_index in range(1, len(array)):
    last_position = outer_index
    for inner_index in range(outer_index - 1, -1, -1):
      if array[last_position] < array[inner_index]:
        array[last_position], array[inner_index] = array[inner_index], array[last_position]
        last_position = inner_index

  return array
