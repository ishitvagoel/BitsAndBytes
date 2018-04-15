# Insertion Sort

def InsertionSort(array):
  for i in range(1, len(array)):
    k = i
    for j in range(i-1, -1, -1):
      if array[k] < array[j]:
        array[k], array[j] = array[j], array[k]
        k = j

  return array
