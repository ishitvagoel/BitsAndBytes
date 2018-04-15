# Bubble Sort

def bubbleSort(input_list):
  """Implementation of Bubble Sort.

  Call eg: bubbleSort([1, 5, 7, 2, 0, -1])

  Args:
    input_list: The list which we need to sort.

  Returns:
    List sorted in ascending order.
    eg: [-1, 0 , 1, 2, 5, 7]
  """
  list_length = len(input_list)
  isSorted = False
  for outer_index in xrange(list_length - 1):
    if not isSorted:
      isSorted = True
      for inner_index in xrange(list_length - outer_index - 1):
        if input_list[inner_index] > input_list[inner_index + 1]:
          isSorted = False
          input_list[inner_index], input_list[inner_index + 1] = input_list[inner_index + 1], input_list[inner_index]
    else:
      break
  return input_list
