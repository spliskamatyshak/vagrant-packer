#!/usr/bin/env python3
"""
Program to build vagrant box and add to vagrant boxes list

Usage:
    make.py [-iphdc CONFIG_JSON]
    make.py [--builder-name NAME --box-name=BOX --media=ISO]
            [(--check-sum=CHECK_SUM --check-sum-type=CHECK_SUM_TYPE)]
            [(--proxy=PROXY [--user-name=PROXY_USERNAME --password=PROXY_PASSWORD])]

Options:
    -h --help                                          Show this screen.
    -d --debug                                         Debug mode.
    -c CONFIG_JSON --config-json=CONFIG_JSON           Path to json configuration file
    -p --print-config                                  Print a json configuration example
    -i --interactive                                   Input information interactively
    -n NAME --builder-name=NAME                        Name of the packer builder
    -b BOX --box-name=BOX                              Name of the vagrant box
    -m ISO --media=ISO                                 URL to ISO
    -k CHECK_SUM --check-sum=CHECK_SUM                 Check sum for ISO [default: ""]
    -t CHECK_SUM_TYPE --check-sum-type=CHECK_SUM_TYPE  Check sum type [default: none]
    -x PROXY --proxy PROXY                             Proxy, if needed
    -u PROXY_USERNAME --user-name=PROXY_USERNAME       Proxy username, if needed
    -s PROXY_PASSWORD --password=PROXY_PASSWORD        Proxy password, if needed

"""

import subprocess
import json
from docopt import docopt

def collect_data():
    """ Collect data interactively from user """
    return 0

def compile_data(args):
    """ Take data from arguments and create json object """
    return 0

def build_data(args):
    """ Pull the data together into a json object """
    if args['--config-json']:
        with open(args['--config-json'], "r") as json_file:
            return json.load(json_file)
    elif args['--interactive']:
        return collect_data()
    return compile_data(args)

def craft_files(data):
    """ Create files for build, add and test of box """
    print("Crafting files...")

def build_box():
    """ Build virtualbox vagrant box image """
    try:
        subprocess.run(["packer", "build", "-force", "vbox.json"])
        return 0
    except subprocess.CalledProcessError as err:
        print('Error: Packer failed, {}', err)
        return 1

def add_box(box, name):
    """ Add vagrant box image to vagrant """
    try:
        subprocess.run(["vagrant", "box", "add", "--force", "--name=" + name,
                        "packer_" + box + "_virtualbox.box"])
        return 0
    except subprocess.CalledProcessError as err:
        print('Error: Vagrant box add failed, {}', err)
        return 2

def test_box():
    """ Test with test-kitchen """
    try:
        subprocess.run(["kitchen", "test"])
        return 0
    except subprocess.CalledProcessError as err:
        print('Error: Kitchen testing failed, {}', err)
        return 4

def main(args):
    """ Main function """
    json_data = build_data(args)
    craft_files(json_data)
    build_result = build_box()
    if build_result == 0:
        add_result = add_box(json_data['builder']['name'], json_data['box_name'])
        if add_result == 0:
            return test_box()
        return add_result
    return build_result

if __name__ == "__main__":
    ARGS = docopt(__doc__)
    if ARGS["--debug"]:
        print(ARGS)
    exit(main(ARGS))
