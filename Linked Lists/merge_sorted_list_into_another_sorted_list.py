# Merge two sorted linked lists in a sorted manner.

'''
Sample Commands:
Repl.it: https://repl.it/@Ishitva/MergeSortedLinkedLists

l1 = LinkedList()
l1.addBatch([1,3,5,7,9, 11, 23])
l2 = LinkedList()
l2.addBatch([4,6,8,10,11,11,13,14,15,16,17,24])
mergeLists(l1,l2)
l1.printLinkedList()

Result:
1 --> 3 --> 4 --> 5 --> 6 --> 7 --> 8 --> 9 --> 10 --> 11 --> 11 --> 11 --> 13 --> 14 --> 15 --> 16 --> 17 --> 23 --> 24

l1 = LinkedList()
l1.addBatch([1,2,3,4,5])
l2 = LinkedList()
l2.addBatch([6,7,8,9,10])
mergeLists(l1,l2)
l1.printLinkedList()

Result:
1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7 --> 8 --> 9 --> 10

l1 = LinkedList()
l1.addBatch([6,7,8,9,10])
l2 = LinkedList()
l2.addBatch([6,7,8,9,10])
mergeLists(l1,l2)
l1.printLinkedList()

Result:
6 --> 6 --> 7 --> 7 --> 8 --> 8 --> 9 --> 9 --> 10 --> 10

l1 = LinkedList()
l1.addBatch([6,7,8,9,10])
l2 = LinkedList()
l2.addBatch([1,2,3,4,5])
mergeLists(l1,l2)
l1.printLinkedList()

Result:
1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7 --> 8 --> 9 --> 10

l1 = LinkedList()
l1.addBatch([6,7,8,9,10])
l2 = LinkedList()
l2.addBatch([1])
mergeLists(l1,l2)
l1.printLinkedList()

Result:
1 --> 6 --> 7 --> 8 --> 9 --> 10

l1 = LinkedList()
l1.addBatch([6,7,8,9,10])
l2 = LinkedList()
l2.addBatch([11])
mergeLists(l1,l2)
l1.printLinkedList()

Result:
6 --> 7 --> 8 --> 9 --> 10 --> 11
'''

NODE_SEPARATOR = ' --> '

checkLessThan = lambda x, y: x < y
checkGreaterThan = lambda x, y: x > y


def mergeLists(list1, list2):
  prev_l1 = list1._head
  l1_ref = list1._head.next
  l2_ref = list2._head.next
  while l1_ref and l2_ref:
    if l2_ref.data <= l1_ref.data:
      # Get the last node in list2 whose data is less than l1_ref.data
      l2_span_end = getSpanEndNode(l2_ref, checkLessThan, l1_ref.data)
      prev_l1.next = l2_ref
      l2_ref = l2_span_end.next
      l2_span_end.next = l1_ref
      prev_l1 = l2_span_end
    elif l2_ref.data > l1_ref.data:
      # Get the last node in list1 whose data is less than l2_ref.data
      l1_span_end = getSpanEndNode(l1_ref, checkLessThan, l2_ref.data)
      if not l1_span_end.next:
        # Append l2 onwards here
        l1_span_end.next = l2_ref
        break
      else:
        # Get the last node in list2 whose data is less than l1_span_end.next.data
        l2_span_end = getSpanEndNode(l2_ref, checkLessThan,
                                     l1_span_end.next.data)
        l1_ref = l1_span_end.next
        prev_l1 = l2_span_end
        l1_span_end.next = l2_ref
        l2_ref = l2_span_end.next
        prev_l1.next = l1_ref


def getSpanEndNode(current_node, getComparison, data):
  while current_node.next:
    if getComparison(current_node.next.data, data):
      current_node = current_node.next
    else:
      break
  return current_node


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
