# Detect cycle and find the beginning node of the cycle in a Linked List

'''
#Sample Commands:

l = LinkedList()
l.addNodeAtEnd(1)
l.addNodeAtEnd(2)
l.addNodeAtEnd(3)
l.addNodeAtEnd(4)
l.addNodeAtEnd(5)

# Create a cycle:

l._head.next.next.next.next = l._head.next.next
l.isListCyclic()

# Returns: 'Cycle begins at node 3'
'''

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

  def isListCyclic(self):
    slow_ref = self._head
    fast_ref = self._head
    isCyclic = False
    while fast_ref.next and fast_ref.next.next:
      fast_ref = fast_ref.next.next
      slow_ref = slow_ref.next
      if slow_ref == fast_ref:
        isCyclic = True
        break
    if isCyclic:
      slow_ref = self._head
      pos = 1
      while slow_ref != fast_ref:
        slow_ref = slow_ref.next
        fast_ref = fast_ref.next
        pos += 1
      return 'Cycle begins at node {}'.format(pos)
    return 'LinkedList is acyclic.'

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
