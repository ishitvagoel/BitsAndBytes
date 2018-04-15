# Selection Sort

def selectionSort(test_list, asc= True):
  """Implementation of Selection Sort.

  Call eg: selectionSort([1, 5, 7, 2, 0, -1], True)

  Args:
    test_list: The list which we need to sort.
    asc: Flag to indicate order of sorting.

  Returns:
    List sorted in ascending order.
    eg: [-1, 0 , 1, 2, 5, 7]
  """
  list_length = len(test_list)
  for outer_index in xrange(list_length-1):
    min_index = outer_index
    for inner_index in xrange(outer_index + 1, list_length):
      if asc:
        replace = test_list[min_index] > test_list[inner_index]
      else:
        replace =  test_list[min_index] < test_list[inner_index]
      if replace:
        test_list[min_index], test_list[inner_index] = test_list[inner_index], test_list[min_index]

  return test_list
