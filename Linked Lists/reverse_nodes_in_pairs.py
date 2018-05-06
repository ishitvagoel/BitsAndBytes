# Reverse the nodes of a Linked List in pairs.

'''
Repl.it: https://repl.it/@Ishitva/ReverseNodesInPairs

Sample Commands:

l = LinkedList()
l.addBatch([1,2,3,4,5,6,7])
reversePairs(l)
l.printLinkedList()

Result:
2 --> 1 --> 4 --> 3 --> 6 --> 5 --> 7
'''

NODE_SEPARATOR = ' --> '

def reversePairs(original_list):
  prev_node = original_list._head
  current_node = prev_node.next
  while current_node and current_node.next:
    if current_node.next:
      temp = current_node.next
      prev_node.next = temp
      current_node.next = temp.next
      temp.next = current_node
      prev_node = current_node
      current_node = current_node.next

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
