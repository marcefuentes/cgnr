""" This module contains a function that returns
 a sorted list of all the folders in a given directory. """

import os


def list_of_folders(path):
    """Returns a sorted list of all the folders in a given directory."""

    folders = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            folders.append(item_path)
    folders.sort()
    return folders
