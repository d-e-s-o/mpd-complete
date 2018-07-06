#!/usr/bin/env python

#/***************************************************************************
# *   Copyright (C) 2015,2018 Daniel Mueller (deso@posteo.net)              *
# *                                                                         *
# *   This program is free software: you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation, either version 3 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU General Public License for more details.                          *
# *                                                                         *
# *   You should have received a copy of the GNU General Public License     *
# *   along with this program.  If not, see <http://www.gnu.org/licenses/>. *
# ***************************************************************************/

"""This script offers help in providing tab completion functionality for mpd/mpc."""

from argparse import (
  ArgumentParser,
)
from mpd import (
  MPDClient as MpdClient,
)
from os.path import (
  join,
)
from sys import (
  argv as sysargv,
  exit,
)


def trail(path):
  """Ensure the path has a trailing separator."""
  return join(path, "")


def setupArgumentParser():
  """Create and initialize an argument parser, ready for use."""
  parser = ArgumentParser()
  parser.add_argument(
    "socket", action="store", metavar="socket",
    help="Socket to use for connecting to MPD.",
  )
  return parser


def main(argv):
  """The main function queries and prints the elements contained in the MPD database."""
  def retrieveValue(element):
    """Retrieve the value of an element as managed by MPD."""
    assert len(element) == 1, element
    assert "directory" in element or "file" in element or "playlist" in element, element
    value, = element.values()

    if "directory" in element:
      return trail(value)

    return value

  parser = setupArgumentParser()
  ns = parser.parse_args(argv[1:])

  client = MpdClient()
  client.connect(ns.socket, 0)
  try:
    # Retrieve a list of all elements in the MPD database. Each item is
    # a dictionary describing the type of element (directory, file,
    # playlist, whatnot) and the value. We are only interested in the
    # value.
    for element in map(retrieveValue, client.listall()):
      print("%s" % element)
  finally:
    client.disconnect()


if __name__ == "__main__":
  exit(main(sysargv))
