# Bubble Sort

def bubbleSort(input_list):
  n = len(input_list)
  isSorted = False
  for i in xrange(n - 1):
    if not isSorted:
      isSorted = True
      for j in xrange(n - i - 1):
        if input_list[j] > input_list[j + 1]:
          isSorted = False
          input_list[j], input_list[j + 1] = input_list[j + 1], input_list[j]
    else:
      break
  return input_list
