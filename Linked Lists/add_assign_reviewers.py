# Circular Linked List to add and assign code reviewers.

'''
Sample Commands:

r = ReviewersList()
r.add_reviewer('Sachin Tendulkar')
r.get_current_reviewer_name()
r.add_reviewer('Micheal Schumacher')
r.add_reviewer('Nadia Comaneci')
r.add_reviewer('Sergei Bubka')
r.get_next_reviewer().name
    '''

class ReviewersList:
  def __init__(self):
    self.head = None
    self.size = 0
    self.current_reviewer = None

  def add_reviewer(self, name):
    new_reviewer = Reviewer(name, None)
    if not self.current_reviewer:
      new_reviewer.set_next(new_reviewer)
      self.head = new_reviewer
      self.current_reviewer = new_reviewer
    else:
      new_reviewer.set_next(self.current_reviewer.get_next())
      self.current_reviewer.set_next(new_reviewer)
    self.size += 1

  def get_next_reviewer(self):
    self.current_reviewer = self.current_reviewer.get_next()
    return self.current_reviewer

  def get_current_reviewer_name(self):
    return self.current_reviewer.name

class Reviewer:
  def __init__(self, name, next_reviewer):
    self.name = name
    self.next_reviewer = next_reviewer

  def set_next(self, next_reviewer_node):
    self.next_reviewer = next_reviewer_node

  def get_next(self):
    return self.next_reviewer

