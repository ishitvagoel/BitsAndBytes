#!/usr/bin/env python

import sys

USER_PERMISSIONS_MAP = {
  'admin': ['admin'],
  'developer': ['dev', 'test'],
  'tester': ['test']
}

ACTION_FUNCTION_NAMES_MAP = {
  'manage': 'ManageUsers',
  'modifydb': 'ModifyDatabase',
  'testdb': 'ReadDatabase'
}


def AccessRequired(permission):
  """Function to return a decorator

    Args:
      permission: String representing permission to check for.

    Returns:
      AccessChecker: Decorator function.
  """

  def AccessChecker(function):

    def Wrapper(*args, **kwargs):

      if permission in GetUserPermissions(sys.argv[1]):
        return function(*args, **kwargs)

      raise Exception("Permission Denied.")

    return Wrapper

  return AccessChecker


def GetUserPermissions(user):
  """Gets user permissions

    Args:
     user: name of the user

    Returns:
     List of permissions for the user.
  """
  return USER_PERMISSIONS_MAP[user]


@AccessRequired('admin')
def ManageUsers():
  print "Managed Users successfully"


@AccessRequired('dev')
def ModifyDatabase():
  print "Modified Database successfully"


@AccessRequired('test')
def ReadDatabase():
  print "Read Database successfully"


def main():
  globals()[ACTION_FUNCTION_NAMES_MAP[sys.argv[2]]]()


if __name__ == '__main__':
  main()
