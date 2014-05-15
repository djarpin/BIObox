BIObox
======

Biogeme is an excellent open source package for estimating discrete choice models.  Model syntax can be specified in Python and run through highly optimized numerical optimization algorithms.

Biogeme runs easily within a Linux/UNIX environment, but has difficulties on Windows.  BIObox is meant to provide a light-weight virtual machine for use in prototyping and testing Biogeme code (a more powerful, optimized system is likely to be necessary for processing any substantially sized data or complex models).

The `examples` folder includes two codes worth mentioning:

1. `nest_depth2.py` utilizes a slightly modified piece of Python code to estimate a multilevel nested logit (this functionality is not immediately obvious to execute in Biogeme).  This code is based on a non-functioning snippet originally posted to the Biogeme User Group by [j_newman_60625](https://groups.yahoo.com/neo/groups/biogeme/conversations/messages/2377).
2. `CreateBiogeme.py` automates a large portion of writing Pythonbiogeme scripts.  Further explanation is included below.

Installation
------------

1. Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. Download and install [Vagrant](http://www.vagrantup.com/downloads.html)
3. Create a new folder on your computer to hold shared documents for BIObox
4. `cd` to this directory and run `vagrant init`
5. Run `vagrant box add <db_sandbox> http://lyte.id.au/vagrant/sl6-64-lyte.box`
6. Pull codes from this git repository into the new folder
7. Run `vagrant up`
8. Run `vagrant ssh`
9. Use something like [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) to log into your virtual machine with the ssh information given by the above
10. Within PuTTY `cd /vagrant`.  This folder is shared with Windows, so it should be straightforward to place existing codes and datasets there and run them using a command like `pythonbiogeme filename dataset.dat`.

CreateBiogemeCode.py
--------------------

Although powerful, Pythonbiogeme's syntax is quite verbose, particularly as the number of alternatives, variables, or latent classes increases.  In these cases, CreateBiogemeCode.py can be used to generate an approximate skeleton Pythonbiogeme code in a few short lines.  This skeleton code should technically run, but adjustments are likely to be necessary to ensure mathematical accuracy.  To test CreateBiogemeCode.py's functionality:

1. Within PuTTY `cd /vagrant/examples`
2. Run `./test_create_biogeme_code.py`.  This code uses CreateBiogeme.py to create several example skeleton codes.
3. Once the appropriate edits are made (see comments at the top of each file) use a command like `pythonbiogeme mnl mock.dat` to run the `mnl.py` code.
