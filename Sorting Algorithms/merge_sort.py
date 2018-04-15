# Merge Sort

def mergeSort(array):
  if len(array) < 2:
    return array

  middle = len(array)/2
  left_sub_array = array[:middle]
  right_sub_array = array[middle:]

  left_sub_array = mergeSort(left_sub_array)
  right_sub_array = mergeSort(right_sub_array)

  return merge(left_sub_array, right_sub_array)

def merge(left_array, right_array):
  left_last = len(left_array) - 1
  right_last = len(right_array) - 1

  left_index = 0
  right_index = 0

  merged_array = []

  while left_index <= left_last and right_index <= right_last:
    if left_array[left_index] <= right_array[right_index]:
      merged_array.append(left_array[left_index])
      left_index += 1
    else:
      merged_array.append(right_array[right_index])
      right_index += 1

  while left_index <= left_last:
    merged_array.append(left_array[left_index])
    left_index += 1

  while right_index <= right_last:
    merged_array.append(right_array[right_index])
    right_index += 1

  return merged_array
