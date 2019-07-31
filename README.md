# Log-Analysis
An internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

## Project Description
Your task is to create a reporting tool that prints out reports (in plain text) based on the data in the database. 
This reporting tool is a Python program using the psycopg2 module to connect to the database.

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

## Download the sql data
Next, download the data here ```https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip```. You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.
To load the data, ``cd`` into the vagrant directory and use the command ``psql -d news -f newsdata.sql``.
Here's what this command does:

``psql`` — the PostgreSQL command line program
``-d news`` — connect to the database named news which has been set up for you
``-f newsdata.sql`` — run the SQL statements in the file newsdata.sql
connect to your newly created database using ``psql news``

## Questions
What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top

Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

## How to run
load the data onto the database
```python
psql -d news -f newsdata.sql
```
connect to the database
```python
psql -d news
```
## Create Views

```python
create view total_web_view as select date(time), count (*) as views from log 
group by date(time) order by date(time);
```

```python
create view error_web_view as select date(time), count (*) as views from log 
where status != '200 OK' group by date(time) order by date(time);
```
```python
create view main as select total_web_view.date, (100.00 * error_web_view.views / total_web_view.views) 
as error_percentage from total_web_view 
join error_web_view 
on total_web_view.date = error_web_view.date 
order by date; 
```
## Running the web app:
Run the app using:
```python
  $ python app.py
```
```python
  open http://localhost:8000/
```
## Author
This project was created and built by Osumgba Chiamaka popularly known as pearl in the tech community
https://www.linkedin.com/in/chiamaka-osumgba/ 
https://web.facebook.com/osumgba.chiamaka
https://twitter.com/KindnessOsumgba
https://www.instagram.com/kindnessosumgba/
