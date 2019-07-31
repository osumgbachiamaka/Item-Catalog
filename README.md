# Item Catalog
An application that provides a list of animals within a variety of species as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Project Description
Project implements a RESTful web application using the Python framework Flask along with implementing third-party OAuth authentication. Also the proper use of the various HTTP methods available and how these methods relate to CRUD (create, read, update and delete) operations.

## Installing the Virtual Machine
In the next part of this course, you'll use a virtual machine (VM) to run an SQL database server and a web app that uses it. The VM is a Linux server system that runs on top of your own computer. You can share files easily between your computer and the VM; and you'll be running a web service inside the VM which you'll be able to access from your regular browser.

We're using tools called Vagrant and VirtualBox to install and manage the VM. You'll need to install these to do some of the exercises. The instructions on this page will help you do this.

## Install VirtualBox
VirtualBox is the software that actually runs the virtual machine. You can download it from virtualbox.org, here. Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Ubuntu users: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

## Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from ```bash vagrantup.com. ``` Install the version for your operating system. 
```bash if vagrant is successfully installed, you will be able to run ``` vagrant --version ```  ```

## Install the Virtual Machine
You can download and unzip this file: FSND-Virtual-Machine.zip from here ```https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip ``` This will give you a directory called FSND-Virtual-Machine. It may be located inside your Downloads folder. Alternately, you can use Github to fork and clone the repository ```https://github.com/udacity/fullstack-nanodegree-vm.```

## Start the virtual machine
From your terminal, inside the vagrant subdirectory, run the command ```bash vagrant up.``` This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is. When ```bash vagrant up``` is finished running, you will get your shell prompt back. At this point, you can run ```bash vagrant ssh``` to log in to your newly installed Linux VM! 
Inside the VM, change directory to ``` /vagrant``` and look around with ```ls```. The PostgreSQL database server will automatically be started inside the VM. You can use the ```python psql``` command-line tool to access it and run SQL statements:

## Create and populate the sqlite database
Clone this project and unzip it. 
Change directory into the project folder ``` cd Item-Catalog ```. Run ``python populatecategories.py `` this will create populate the database with dummy values.
To start the application, ``python app.py`` Your application will be started on  ``http://localhost:8000/`` or ``http://localhost:8000/catalog/``

## Json Endpoints
Json api endpoints can be accessed on the following ports
```python
http://localhost:8000/items/catalog.json
```
connect to the database
```python
http://localhost:8000/catalog/<string:category_name>/<string:item_name>/JSON
```
```python
http://localhost:8000/catalog/<string:category_name>/JSON
```
## Author
This project was created and built by Osumgba Chiamaka popularly known as pearl in the tech community
https://www.linkedin.com/in/chiamaka-osumgba/ 
https://web.facebook.com/osumgba.chiamaka
https://twitter.com/KindnessOsumgba
https://www.instagram.com/kindnessosumgba/
