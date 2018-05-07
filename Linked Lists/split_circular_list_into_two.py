# Split a circular linked list into two equal parts.
# In case of odd nodes let list1 have the extra node.

'''
Repl.it: https://repl.it/@Ishitva/SplitCircularListIntoTwo

Sample Commands:

list1 = LinkedList()
list1.addBatch([1,2,3,4,5,6,7,8,9,10,11])
# Make list1 circular by making 11th node point to first node.
list1._head.next.next.next.next.next.next.next.next.next.next.next.next = list1._head.next

result = splitCircularList(list1)
result[0].printLinkedList() # 1 --> 2 --> 3 --> 4 --> 5 --> 6
result[1].printLinkedList() # 7 --> 8 --> 9 --> 10 --> 11
'''

import math

NODE_SEPARATOR = ' --> '

def splitCircularList(orig_list):
  current_node = orig_list._head.next
  list_length = 1
  while current_node.next != orig_list._head.next:
    current_node = current_node.next
    list_length += 1

  current_node.next = None
  current_node = orig_list._head.next
  node_number = 1
  while node_number < math.ceil(list_length / 2.0):
    current_node = current_node.next
    node_number += 1

  list2 = LinkedList()
  list2._head.next = current_node.next
  current_node.next = None
  return orig_list, list2


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
