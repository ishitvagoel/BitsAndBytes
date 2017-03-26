#!/usr/bin/env python

import sys

def UserPermission(function):
  """Decorator to ask user permission before executing a function.

    Args:
      function: The function object to decorate.

    Returns:
      Wrapper function.
  """

  def Wrapper(*args):

    allow = raw_input("Allow to proceed the execution (y/n)?")
    if allow == 'y' or allow == 'Y':
      function(*args)
      print ("Method " + function.__name__ +
             " executed with %s arguments" % (len(args)))
    else:
      print "Method execution denied by the user."
    return

  return Wrapper


@UserPermission
def main(*args):
  print args


if __name__ == '__main__':
  main(sys.argv[1:])
