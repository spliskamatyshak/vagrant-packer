#!/usr/bin/env python3
"""
Program to build CentOS vagrant box and add to vagrant boxes
"""

import subprocess

def build(name):
    """ Build virtualbox vagrant box image """
    try:
        subprocess.run(["packer", "build", "-force", name])
        return 0
    except subprocess.CalledProcessError as err:
        print('Error: Packer failed, ', err)
        return 1

def add(name):
    """ Add vagrant box image to vagrant """
    try:
        subprocess.run(["vagrant", "box", "add", "--force", "--name=" + name,
                        "packer_cent7_virtualbox.box"])
        return 0
    except subprocess.CalledProcessError as err:
        print('Error: Vagrant box add failed, ', err)
        return 2

def main():
    """ Main function """
    if build("vbox.json") == 0:
        add("CentOS")

if __name__ == "__main__":
    main()
