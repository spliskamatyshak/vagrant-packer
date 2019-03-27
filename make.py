#!/usr/bin/env python
"""
Program to build CentOS vagrant box and add to vagrant boxes
"""

import subprocess

def build(name):
    """ Build virtualbox vagrant box image """
    subprocess.run(["packer", "build", "-force", name])

def add(name):
    """ Add vagrant box image to vagrant """
    subprocess.run(["vagrant", "box", "add", "--force", "--name=" + name,
                    "packer_cent7_virtualbox.box"])

def main():
    """ Main function """
    build("vbox.json")
    add("CentOS")

if __name__ == "__main__":
    main()
