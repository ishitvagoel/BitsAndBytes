#Template Linked List.
#TODO 1: Add methods to remove nodes.
#TODO 2: Add Exception handing.

NODE_SEPARATOR = ' --> '

class LinkedList:
  def __init__(self):
    self._head = None
    self._size = 0

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

  def addNodeAtBeg(self, data):
    new_node = Node(data, None)
    self._size += 1
    if not self._head:
      self._head = new_node
      return
    new_node.next = self._head
    self._head = new_node

  def addNodeAtPos(self, data, pos):
    if pos < 1 or pos > self._size + 1:
      print "Invalid position"
      return
    elif pos == 1:
      self.addNodeAtBeg(data)
      return
    elif pos == (self._size + 1):
      self.addNodeAtEnd(data)
      return
    new_node = Node(data, None)
    self._size += 1
    current_node = self._head
    current_pos = 1
    while current_pos < pos - 1:
      current_node = current_node.next
      current_pos += 1
    new_node.next = current_node.next
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

