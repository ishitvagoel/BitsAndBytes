# Reverse blocks of K nodes in a given Linked List.

'''
Repl.it: https://repl.it/@Ishitva/ReverseNodesInBlocksOfK

Sample Commands:

l = LinkedList()
l.addBatch([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
reverseInBlocks(l, 4)
l.printLinkedList()

Result:
4 --> 3 --> 2 --> 1 --> 8 --> 7 --> 6 --> 5 --> 12 --> 11 --> 10 --> 9 --> 15 --> 14 --> 13

l = LinkedList()
l.addBatch([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
reverseInBlocks(l, 3)
l.printLinkedList()

Result:
3 --> 2 --> 1 --> 6 --> 5 --> 4 --> 9 --> 8 --> 7 --> 12 --> 11 --> 10 --> 15 --> 14 --> 13

l = LinkedList()
l.addBatch([1,2,3])
reverseInBlocks(l, 10)
l.printLinkedList()

Result:
3 --> 2 --> 1
'''

NODE_SEPARATOR = ' --> '

def reverseInBlocks(list1, k):
  current_node = list1._head.next
  prev_node = list1._head
  prev_end_node = list1._head
  temp = None
  while current_node:
    node_in_block = 0
    while node_in_block < k and current_node:
      temp = current_node.next
      current_node.next = prev_node
      prev_node = current_node
      current_node = temp
      node_in_block += 1
    prev_end_node.next.next = current_node
    temp = prev_end_node.next
    prev_end_node.next = prev_node
    prev_end_node = temp

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
