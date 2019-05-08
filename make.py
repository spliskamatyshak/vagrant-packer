#!/usr/bin/env python3
"""
Program to build vagrant box and add to vagrant boxes list

Usage:
    make.py [-hd]
    make.py [-pd] --interactive
    make.py [-pd] --config-json=CONFIG_JSON
    make.py [-pd] [--builder-name=NAME --box-name=BOX --media=ISO]
            [(--check-sum=CHECK_SUM --check-sum-type=CHECK_SUM_TYPE)]
            [(--proxy=PROXY [--user-name=PROXY_USERNAME --password])]

Options:
    -h --help                                          Show this screen.
    -d --debug                                         Debug mode.
    -i --interactive                                   Take interactive input.
    -c CONFIG_JSON --config-json=CONFIG_JSON           Path to json configuration file.
    -p --print-config                                  Print a json configuration example.
    -n NAME --builder-name=NAME                        Name of the packer builder.
    -b BOX --box-name=BOX                              Name of the vagrant box.
    -m ISO --media=ISO                                 URL to ISO.
    -k CHECK_SUM --check-sum=CHECK_SUM                 Check sum for ISO.
    -t CHECK_SUM_TYPE --check-sum-type=CHECK_SUM_TYPE  Check sum type.
    -x PROXY --proxy=PROXY                             Proxy, with port, if needed.
    -u PROXY_USERNAME --user-name=PROXY_USERNAME       Proxy username, if needed.
    -s --password                                      Proxy password, if needed.

"""

import subprocess
import json
import sys
import getpass
import jinja2
from docopt import docopt

class VagrantBox():
    """ Class defining vagrant box """

    def __init__(self, args):
        self.args = args
        self.build_data = {
            "builder": {
                "name": "cent7",
                "iso_url": "http://centos.mirrors.tds.net/pub/linux/centos/7.6.1810/isos/x86_64/CentOS-7-x86_64-DVD-1810.iso",
                "iso_checksum": "6d44331cc4f6c506c7bbe9feb8468fad6c51a88ca1393ca6b8b486ea04bec3c1",
                "iso_checksum_type": "sha256"
                },
            "box_name": "CentOS",
            "proxy": "",
            "proxy_username": "",
            "proxy_password": ""
            }

    def collect_data(self):
        """ Collect data interactively from user """
        ans1 = input("Enter builder name [{}]: ".format(self.build_data["builder"]["name"]))
        if ans1 != "":
            self.build_data["builder"]["name"] = ans1

        ans2 = input("Enter ISO url [{}]: ".format(self.build_data["builder"]["iso_url"]))
        if ans2 != "":
            self.build_data["builder"]["iso_url"] = ans2

        ans3 = input("Enter ISO checksum [{}]: ".format(self.build_data["builder"]["iso_checksum"]))
        if ans3 != "":
            self.build_data["builder"]["iso_checksum"] = ans3

        ans4 = input("Enter ISO checksum type [{}]: ".format(self.build_data["builder"]["iso_checksum_type"]))
        if ans4 != "":
            self.build_data["builder"]["iso_checksum_type"] = ans4

        ans5 = input("Enter Vagrant box name [{}]: ".format(self.build_data["box_name"]))
        if ans5 != "":
            self.build_data["box_name"] = ans5

        ans6 = input("Enter proxy, i.e. http(s)://proxy.domain.com:port: ")
        if ans6 != "":
            self.build_data["proxy"] = ans6

        ans7 = input("Enter proxy user name: ")
        if ans7 != "":
            self.build_data["proxy_username"] = ans7

        ans8 = getpass.getpass(prompt="Enter proxy password: ")
        if ans8 != "":
            self.build_data["proxy_password"] = ans8

    def compile_data(self):
        """ Take data from arguments and create json object """
        if self.args["--builder-name"]:
            self.build_data["builder"]["name"] = self.args["--builder-name"]
        if self.args["--media"]:
            self.build_data["builder"]["iso_url"] = self.args["--media"]
        if self.args["--check-sum"]:
            self.build_data["builder"]["iso_checksum"] = self.args["--check-sum"]
        if self.args["--check-sum-type"]:
            self.build_data["builder"]["iso_checksum_type"] = self.args["--check-sum-type"]
        if self.args["--box-name"]:
            self.build_data["box_name"] = self.args["--box-name"]
        if self.args["--proxy"]:
            self.build_data["proxy"] = self.args["--proxy"]
        if self.args["--user-name"]:
            self.build_data["proxy_username"] = self.args["--user-name"]
        if self.args["--password"]:
            self.build_data["proxy_password"] = getpass.getpass(prompt="Enter password: ")

    def make_data(self):
        """ Pull the data together into a json object """
        if self.args["--config-json"]:
            with open(self.args["--config-json"], "r") as json_file:
                self.build_data = json.load(json_file)
        elif self.args["--interactive"]:
            self.collect_data()
        self.compile_data()

        if self.args["--print-config"]:
            print(self.build_data)

    def get_data(self):
        """ Retrives build_data """
        return self.build_data

def craft_files(debug, data):
    """ Create files for build, add and test of box """
    print("Crafting files...")
    if debug:
        print(data)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))

    template = env.get_template("ks.cfg.j2")
    with open("ks.cfg", "w") as config_file:
        print(template.render(data=data), file=config_file)

    template = env.get_template("vbox.json.j2")
    with open("vbox.json", "w") as config_file:
        print(template.render(data=data), file=config_file)

    template = env.get_template("kitchen.yml.j2")
    with open(".kitchen.yml", "w") as config_file:
        print(template.render(data=data), file=config_file)

def build_box():
    """ Build virtualbox vagrant box image """
    try:
        subprocess.run(["packer", "build", "-force", "vbox.json"])
        return 0
    except subprocess.CalledProcessError as err:
        print("Error: Packer failed, {}", err)
        return 2

def add_box(box, name):
    """ Add vagrant box image to vagrant """
    try:
        subprocess.run(["vagrant", "box", "add", "--force", "--name=" + name,
                        "packer_" + box + "_virtualbox.box"])
        return 0
    except subprocess.CalledProcessError as err:
        print("Error: Vagrant box add failed, {}", err)
        return 4

def test_box():
    """ Test with test-kitchen """
    try:
        subprocess.run(["bundle", "install", "--path", "vendor/bundle"])
        subprocess.run(["kitchen", "test"])
        return 0
    except subprocess.CalledProcessError as err:
        print("Error: Kitchen testing failed, {}", err)
        return 8

def main(args):
    """ Main function """
    new_box_data = VagrantBox(args)
    new_box_data.make_data()
    json_data = new_box_data.get_data()
    if args["--debug"]:
        print(json_data)

    craft_files(args["--debug"], json_data)

    result = build_box()
    if result == 0:
        result += add_box(json_data["builder"]["name"], json_data["box_name"])
        if result == 0:
            return result + test_box()
        return result
    return result

if __name__ == "__main__":
    NO_ARGS = len(sys.argv) - 1 == 0
    ARGS = docopt(__doc__)
    if ARGS["--help"] or NO_ARGS:
        print(__doc__)
        exit(0)
    if ARGS["--debug"]:
        print(ARGS)
    exit(main(ARGS))
