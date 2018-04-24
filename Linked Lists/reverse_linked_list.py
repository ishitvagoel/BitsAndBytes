# Reverse a linked list

'''
Sample Commands:

l = LinkedList()
l.addBatch([1,2,3,4,5,6,7,8,9,10])

l.printLinkedList()
# 1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7 --> 8 --> 9 --> 10

l.reverseList()
l.printLinkedList()
# 10 --> 9 --> 8 --> 7 --> 6 --> 5 --> 4 --> 3 --> 2 --> 1

'''

NODE_SEPARATOR = ' --> '

class LinkedList:
  def __init__(self):
    self._head = None
    self._size = 0

  def addBatch(self, data_list):
    for data in data_list:
      self.addNodeAtEnd(data)

  def reverseList(self):
    current_node = self._head
    temp = None
    next_node = current_node.next

    while current_node:
      current_node.next = temp
      temp = current_node
      if next_node:
        current_node = next_node
        next_node = current_node.next
      else:
        self._head = current_node
        break

  def addNodeAtEnd(self, data):
    new_node = Node(data, None)
    self._size += 1
    if not self._head:
      self._head = new_node
      return
    current_node = self._head
    while current_node.next:
      current_node = current_node.next
    current_node.next = new_node

  def printLinkedList(self):
    current_node = self._head
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

