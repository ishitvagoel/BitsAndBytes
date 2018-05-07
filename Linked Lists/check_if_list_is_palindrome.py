# Check if a Linked List is palindrome or not.

'''
Repl.it: https://repl.it/@Ishitva/CheckIfListIsPalindrome

Sample Commands:

l = LinkedList()
l.addBatch([1])
a = checkPalindrome(l._head.next,l._head.next)
a[0] # Contains final truth value

Result:
True

l = LinkedList()
l.addBatch([1,2,1,2,1])
a = checkPalindrome(l._head.next,l._head.next)
a[0] # Contains final truth value

Result:
True

l = LinkedList()
l.addBatch([1,2,2,2,2])
a = checkPalindrome(l._head.next,l._head.next)
a[0] # Contains final truth value

Result:
False
'''

NODE_SEPARATOR = ' --> '

def checkPalindrome(slow_ref, fast_ref):
  truth = True
  comparison_node = None
  if fast_ref.next and fast_ref.next.next:
    truth, comparison_node = checkPalindrome(slow_ref.next, fast_ref.next.next)
  else: # Last recursive call
    comparison_node = slow_ref.next
    if not fast_ref.next: # True only when number of nodes is odd.
      comparison_node = slow_ref
  truth = truth and (slow_ref.data == comparison_node.data)
  return truth, comparison_node.next


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
