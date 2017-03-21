#!/usr/bin/env python

import os
import sys

ROOT_DIR = '.'  # The directory to start from. Present directory in this case.
TRAVERSAL_BOOLEAN_MAP = {
  'topdown': True,
  'bottomup': False
}

def PrintFileStructure():
  """Prints the file structure in the present directory."""

  try:
    for dir_name, sub_dir_list, file_list in os.walk(
        ROOT_DIR, topdown=TRAVERSAL_BOOLEAN_MAP[sys.argv[1]]):
      print 'Found Directory: %s' % (dir_name)
      for file_name in file_list:
        print '\t%s' % (file_name)
  except IndexError as e.:
    print 'Traversal order not specified. Error: %s' % (e)


def main():
  PrintFileStructure()


if __name__ == '__main__':
  main()



