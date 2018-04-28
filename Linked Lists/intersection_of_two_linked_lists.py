# Find node of intersection of two merging linked lists.

'''
Sample Commands:

l1 = LinkedList()

l1.addBatch([1,2,3,4,5,6])

l2 = LinkedList()

l2.addBatch([1,2])

# Set node having value 4 as the intersection point.
l2._head.next.next = l1._head.next.next.next

findIntersection(l1,l2)

Result: 4
'''

NODE_SEPARATOR = ' --> '

def findIntersection(list1, list2):
  length_difference = 0
  list_refs = {
    'list1': list1._head,
    'list2': list2._head
  }
  list1_length = 0
  list2_length = 0
  current_node = list_refs['list1']
  while current_node:
    list1_length += 1
    current_node = current_node.next

  current_node = list_refs['list2']
  while current_node:
    list2_length += 1
    current_node = current_node.next

  longer_list_key = ''
  if list1_length > list2_length:
    length_difference = list1_length - list2_length
    longer_list_key = 'list1'
  else:
    length_difference = list2_length - list1_length
    longer_list_key = 'list2'

  for adjusting_step in range(length_difference):
    list_refs[longer_list_key] = list_refs[longer_list_key].next

  while list_refs['list1'] != list_refs['list2']:
    list_refs['list1'] = list_refs['list1'].next
    list_refs['list2'] = list_refs['list2'].next

  return list_refs['list2'].data

class LinkedList:
  def __init__(self):
    self._head = None
    self._size = 0

  def addBatch(self, data_list):
    for data in data_list:
      self.addNodeAtEnd(data)

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

