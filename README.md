# vagrant-packer
Packer code for building CentOS Vagrant box
## Requirements
Install latest of software listed below:
- Python3
  - pip
  - jinja2
  - docopt
- Ruby
  - bundler
- Vagrant
- Packer
- VirtualBox
## Usage
run `./make.py` (refer to docopt for options)
## Output
Using default setting, this will produce a Vagrant box named `CentOS` with Centos 7.7; python and ansible installed along with VirtualBox Guest Additions for the version of VirtualBox installed.