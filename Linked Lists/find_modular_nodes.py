# Find last modular node from beginning and end whose pos % k = 0

'''
Repl.it: https://repl.it/@Ishitva/FindModularNodes

Sample Commands:
l = LinkedList([1,2,5,111,234,51,1])
modularNodeFromBeg(l,3)

Result:
'At position 6, the node with data 51'

'''

NODE_SEPARATOR = ' --> '

def modularNodeFromBeg(list_arg, k):
  pos = 0
  current_node = list_arg._head.next
  modular_node = None
  modular_node_pos = None
  if k <= 0:
    return
  while current_node:
    pos += 1
    if pos % k == 0:
      modular_node = current_node
      modular_node_pos = pos
    current_node = current_node.next
  if modular_node:
    return 'At position {}, the node with data {}'.format(modular_node_pos,modular_node.data)
  return 'Not found'

def modularNodeFromEnd(list_arg, k):
  pass

class LinkedList:
  def __init__(self, nodes):
    self._head = Node(-100000, None)
    self._size = 0
    self.addBatch(nodes)

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
