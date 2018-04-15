# Selection Sort

def selectionSort(test_list, asc= True):

  n = len(test_list)
  for i in xrange(n-1):
    min_index = i
    for j in xrange(i + 1, n):

      if asc:
        replace = test_list[min_index] > test_list[j]
      else:
        replace =  test_list[min_index] < test_list[j]

      if replace:
        test_list[min_index], test_list[j] = test_list[j], test_list[min_index]

  return test_list
