# Merge two sorted linked lists in a sorted manner.

'''
Repl.it: https://repl.it/@Ishitva/MergeSortedLinkedListsSimplified

Sample Commands:

l1 = LinkedList()
l1.addBatch([1,3,5,7,9, 11, 23])
l2 = LinkedList()
l2.addBatch([4,6,8,10,11,11,13,14,15,16,17,24])
mergeLists(l1,l2).printLinkedList()

Result:
1 --> 3 --> 4 --> 5 --> 6 --> 7 --> 8 --> 9 --> 10 --> 11 --> 11 --> 11 --> 13 --> 14 --> 15 --> 16 --> 17 --> 23 --> 24

l1 = LinkedList()
l1.addBatch([1,2,3,4,5])
l2 = LinkedList()
l2.addBatch([6,7,8,9,10])
mergeLists(l1,l2).printLinkedList()

Result:
1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7 --> 8 --> 9 --> 10

l1 = LinkedList()
l1.addBatch([6,7,8,9,10])
l2 = LinkedList()
l2.addBatch([6,7,8,9,10])
mergeLists(l1,l2).printLinkedList()

Result:
6 --> 6 --> 7 --> 7 --> 8 --> 8 --> 9 --> 9 --> 10 --> 10

l1 = LinkedList()
l1.addBatch([6,7,8,9,10])
l2 = LinkedList()
l2.addBatch([1,2,3,4,5])
mergeLists(l1,l2).printLinkedList()

Result:
1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7 --> 8 --> 9 --> 10

l1 = LinkedList()
l1.addBatch([6,7,8,9,10])
l2 = LinkedList()
l2.addBatch([1])
mergeLists(l1,l2).printLinkedList()

Result:
1 --> 6 --> 7 --> 8 --> 9 --> 10

l1 = LinkedList()
l1.addBatch([6,7,8,9,10])
l2 = LinkedList()
l2.addBatch([11])
mergeLists(l1,l2).printLinkedList()

Result:
6 --> 7 --> 8 --> 9 --> 10 --> 11
'''

NODE_SEPARATOR = ' --> '

def mergeLists(list1, list2):
  list1_current = list1._head.next
  list2_current = list2._head.next
  sorted_list = LinkedList()
  temp = sorted_list._head

  while list1_current and list2_current:
    if list1_current.data <= list2_current.data:
      temp.next = list1_current
      list1_current = list1_current.next
    else:
      temp.next = list2_current
      list2_current = list2_current.next
    temp = temp.next
  if list1_current:
    temp.next = list1_current
  if list2_current:
    temp.next = list2_current

  return sorted_list

class LinkedList:
  def __init__(self):
    self._head = Node(-100000, None)
    self._size = 0

  def addBatch(self, data_list):
    for data in data_list:
      self.addNodeAtEnd(data)

  def addNodeAtEnd(self, data):
    new_node = Node(data, None)
    self._size += 1
    if not self._head.next:
      self._head.next = new_node
      return
    current_node = self._head.next
    while current_node.next:
      current_node = current_node.next
    current_node.next = new_node

  def printLinkedList(self):
    current_node = self._head.next
    data_list = []
    while current_node:
      data_list.append(current_node.data)
      current_node = current_node.next

    print NODE_SEPARATOR.join(str(data) for data in data_list)


class Node:
  def __init__(self, data, next_node):
    self._data = data
    self._next = next_node

  @property
  def data(self):
    return self._data

  @data.setter
  def data(self, data):
    self._data = data

  @property
  def next(self):
    return self._next

  @next.setter
  def next(self, next_node):
    self._next = next_node
