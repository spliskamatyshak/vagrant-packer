#!/usr/bin/env python
"""
Program to build CentOS vagrant box and add to vagrant boxes
"""

import subprocess

def build(name):
    """ Build virtualbox vagrant box image """
    try:
        subprocess.run(["packer", "build", "-force", name])
    except subprocess.CalledProcessError as err:
        print('Error:', err)

def add(name):
    """ Add vagrant box image to vagrant """
    try:
        subprocess.run(["vagrant", "box", "add", "--force", "--name=" + name,
                        "packer_cent7_virtualbox.box"])
    except subprocess.CalledProcessError as err:
        print('Error:', err)

def main():
    """ Main function """
    build("vbox.json")
    add("CentOS")

if __name__ == "__main__":
    main()
