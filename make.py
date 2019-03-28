#!/usr/bin/env python3
"""
Program to build CentOS vagrant box and add to vagrant boxes
"""

import subprocess

def build(name):
    """ Build virtualbox vagrant box image """
    try:
        subprocess.run(["packer", "build", "-force", name])
        return True
    except subprocess.CalledProcessError as err:
        print('Error:', err)
        return False

def add(name):
    """ Add vagrant box image to vagrant """
    try:
        subprocess.run(["vagrant", "box", "add", "--force", "--name=" + name,
                        "packer_cent7_virtualbox.box"])
        return True
    except subprocess.CalledProcessError as err:
        print('Error:', err)
        return False

def main():
    """ Main function """
    if build("vbox.json"):
        add("CentOS")

if __name__ == "__main__":
    main()
