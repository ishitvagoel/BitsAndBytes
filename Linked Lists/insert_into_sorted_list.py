#Template Linked List

'''
Sample Commands:

l = LinkedList()
l.addNodeInSortedList(0)
l.addNodeInSortedList(-1)
l.addNodeInSortedList(1)
l.printLinkedList()

Result:
-1 --> 0 --> 1
'''

NODE_SEPARATOR = ' --> '

class LinkedList:
  def __init__(self):
    self._head = None
    self._size = 0

  def addNodeInSortedList(self, data):
    new_node = Node(data, None)
    self._size += 1

    if not self._head:
      self._head = new_node
      return
    current_node = self._head
    prev_node = self._head

    while current_node:
      if data > current_node.data:
        prev_node = current_node
        current_node = current_node.next
        continue
      break

    if prev_node == self._head and current_node == self._head:
      new_node.next = self._head
      self._head = new_node
      return
    new_node.next = prev_node.next
    prev_node.next = new_node

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

