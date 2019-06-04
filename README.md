## Project 1: Project: Catalog
The **Item Catalog** project an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system.

## Installing the Vagrant VM

#### Use a terminal
You'll be using a Unix-style terminal on your computer. If you are using a Mac or Linux system, your regular terminal program will do just fine. On Windows, we recommend using the Git Bash terminal that comes with the Git software. If you don't already have Git installed, download Git from [git-scm.com.](https://git-scm.com/downloads)
For a refresher on using the Unix shell, look back at our [Shell Workshop](https://www.udacity.com/course/shell-workshop--ud206).
If you'd like to learn more about Git, take a look at [our course about Git](https://www.udacity.com/course/version-control-with-git--ud123).

#### Install VirtualBox
VirtualBox is the software that actually runs the virtual machine. [You can download it from virtualbox.org, here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.
Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.
**Ubuntu users**: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

#### Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com](https://www.vagrantup.com/downloads.html). Install the version for your operating system.
Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.
_If Vagrant is successfully installed, you will be able to run `vagrant --version` in your terminal to see the version number._

#### Download the VM configuration
There are a couple of different ways you can download the VM configuration.
You can download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called **FSND-Virtual-Machine**. It may be located inside your **Downloads** folder.  
**Note**: If you are using Windows OS you will find a Time Out error, to fix it use the new [Vagrant file configuration](https://s3.amazonaws.com/video.udacity-data.com/topher/2019/March/5c7ebe7a_vagrant-configuration-windows/vagrant-configuration-windows.zip) to replace you current Vagrant file.
Alternately, you can use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.
Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with `cd`. Inside, you will find another directory called **vagrant**. Change directory to the **vagrant** directory:  

_$ cd Downloads/FSND-Virtual-Machine  
$ cd vagrant/_
#### Start the virtual machine
From your terminal, inside the **vagrant** subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!
#### Logged in!
If you are now looking at a shell prompt that starts with the word `vagrant`, congratulations — you've gotten logged into your Linux VM. If not, take a look at the **Troubleshooting** section below.

#### The files for this project
Inside the VM, change directory to `/vagrant` and look around with `ls`.
The files you see here are the same as the ones in the `vagrant` subdirectory on your computer (where you started Vagrant from). Any file you create in one will be automatically shared to the other. This means that you can edit code in your favorite text editor, and run it inside the VM. Files in the VM's `/vagrant` directory are shared with the `vagrant` folder on your computer. But other data inside the VM is not.

#### Logging out and in
If you type `exit` (or `Ctrl-D`) at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're in the same directory and type `vagrant ssh` again. If you reboot your computer, you will need to run `vagrant` up to restart the VM.
________________________________________
### Troubleshooting
**I'm not sure if it worked**.  
If you can type `vagrant ssh` and log into your VM, then it worked! It's normal for the `vagrant up` process to display a lot of text in many colors, including sometimes scary-looking messages in red, green, and purple. If you get your shell prompt back at the end, and you can log in, it should be OK.

`vagrant up` **is taking a long time. Why?**  
Because it's downloading a whole Linux operating system from the Internet.

**I'm on Windows, and when I run `vagrant ssh`, I don't get a shell prompt**.  
Some versions of Windows and Vagrant have a problem communicating the right settings for the terminal. There is a workaround: Instead of `vagrant ssh`, run the command `winpty` `vagrant ssh` instead.

**I'm on Windows and getting an error about virtualization**.  
Sometimes other virtualization programs such as Docker or Hyper-V can interfere with VirtualBox. Try shutting these other programs down first.

In addition, some Windows PCs have settings in the BIOS or UEFI (firmware) or in the operating system that disable the use of virtualization. To change this, you may need to reboot your computer and access the firmware settings. A [web search](https://www.google.com/search?q=enable%20virtualization%20windows%2010) can help you find the settings for your computer and operating system. Unfortunately there are so many different versions of Windows and PCs that we can't offer a simple guide to doing this.

**Why are we using a VM? It seems complicated**.  
It is complicated. In this case, the point of it is to be able to offer the same software (Linux and PostgreSQL) regardless of what kind of computer you're running on.

**I got some other error message**.  
If you're getting a specific textual error message, try looking it up on your favorite search engine. If that doesn't help, take a screenshot and post it to the discussion forums, along with as much detail as you can provide about the process you went through to get there.

**If all else fails, try an older version**.  
Udacity mentors have noticed that some newer versions of Vagrant don't work on all operating systems. Version 1.9.2 is reported to be stabler on some systems, and version 1.9.1 is the supported version on Ubuntu 17.04. You can download older versions of Vagrant from [the Vagrant releases index](https://releases.hashicorp.com/vagrant/).

## Fetch the Source Code
From your terminal, inside the vagrant subdirectory, run the command:  
`git clone https://github.com/gsiffer/Catalog.git`  
This will give you a directory named **category** complete with the source code for the flask application.

#### Run the virtual machine!
Using the terminal, change directory to vagrant (cd vagrant), then type vagrant up to launch your virtual machine.

#### Running the Catalog App
Once it is up and running, type **vagrant ssh**. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt. When you want to log out, type **exit** at the shell prompt.  To turn the virtual machine off (without deleting anything), type **vagrant halt**. If you do this, you'll need to run **vagrant up** again before you can log into it.


Now that you have Vagrant up and running type **vagrant ssh** to log into your VM.  change to the /vagrant directory by typing **cd /vagrant**. This will take you to the shared folder between your virtual machine and host machine.

Type **ls** to ensure that you are inside the directory that contains project.py, database_setup.py, and two directories named 'templates' and 'static'

The program was written in python2. Use the command python2 project.py to run the program.

Now type **python database_setup.py** to initialize the database.

Type **python lotsofitems.py** to populate the database with categories and items. (Optional)

Type **python project.py** to run the Flask web server. In your browser visit **http://localhost:8000** to view the catalog app.  You should be able to view, add, edit, and delete items and categories.

### LICENCE
https://choosealicense.com/
