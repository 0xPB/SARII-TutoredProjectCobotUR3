Authors :
- BRUNO Paul (paul.bruno.pro@protonmail.com)
- PELE Alexis (alexis.pele.pc@gmail.com)
Degree : LP SARII (L3)
School : IUT of Bordeaux - Department GEII
Link to school's website : https://www.iut.u-bordeaux.fr/geii
Publication date : 20/01/2023

___

# Table of contents

1. Introduction
2. Requierements
3. User Guide : HMI UR3 by BRUNO Paul & PELE Alexis
4. User Guide : Universal Robot Tablet HMI
	1. UR3
	2. UR3e
5. Global code explanation

# 1. Introduction

> [!INFO] > In this part, you will learn why this project was created. Skip to part 2 if you want to access the user guide.

This documentation has been realized within the framework of the tutored project in order to help the new users take the program in hand. This human-machine interface was designed to be as easy as possible to use for people who have never worked with a collaborative robot before (also known as a cobot).

# 2. Requirements

> [!INFO] > In this part, you will learn how to use the software we designed. Skip to 3 if you want to access the user guide.

## Required hardware :
- Computer with Linux or Windows
- Ethernet cable connected to UR3 and your computer
- Universal Robot - UR3 (with or without the Robotiq Gripper)

> [!WARNING] > For WINDOWS : If you already have the.EXE file, then you don't need to follow the steps in the following category. You can skip and go to part 3.

## Required software :
- Environment to run python code (ex. : Visual Studio Code : https://code.visualstudio.com/)
- ***Linux*** : open a terminal and copy-paste the followings commands :
	- If you don't have **pip** installed : `sudo apt install python3-pip`
	- Urx : `pip install urx`
	- Tkinter : `sudo apt-get install python-tk`
- ***Windows*** : 
	- Download and install Python : https://www.python.org/downloads/
	- Open the Command prompt
		- ``Win+R`` then type ``cmd``
		- Or type ``Command Prompt`` in the search bar
	- Copy paste the following command : `pip install urx tkinter`

> [!WARNING] >FOR WINDOWS : Select *"ADD TO PATH"* option when installing.

# 3. User Guide : HMI UR3 by BRUNO Paul & PELE Alexis

> [!INFO] > In this part, you will learn how to use the software we designed.
> Skip to 4 if you want to access the user guide.

![[photointe 1.png]]
<p class="textcenter">HMI UR3</p>
### Connect / Disconnect
The ``Connect`` button is made to enable the connection **(9)** and the ``Disconnect`` button allows you to disconnect from the cobot and will close the program's window.

### Get joints values
The ``GET JOINTS angles`` button **(1)** allows us to get the angles of the cobot motor and then autofills the fields on the Entries numbered interface **(2)**.

### Select cobot movement type
The zone **(3)** is used to select the movement mode of the cobot that should be used :
- J : Joint motion (the path is using joint angle going from one position to another)
- L :  Linear motion (the path is linear going from one position to another)
- C : Circular motion (the path is circular going from one position to another)

### Make the cobot move
The  ``Move JOINTS`` button **(4)** allows to apply the data given in the part **(2)** to the cobot.

### Get TCP coordinates
The ``Get TCP Pose`` button located in the area **(5)** allows to put in the same way as the button ``Get JOINTS angles`` **(1)** it allows to recover the position of the end effector of the cobot after having recovered them they are indicated in the boxes in the area **(6)**.

### Make cobot move according to TCP pose
The ``Move TCP`` button of the zone **(7)** applies the positions that are indicated in the zone **(6)**.

### Go to home position
The ``HOME`` position button **(8)** allows you to get back to the initial position, which is the position defined when the code was launched.

### Opening/closing the gripper
The buttons in areas **(10)** and **(11)** are used respectively to open or close the gripper that corresponds to the clamp on the head of the cobot and if you want to open the clamp more or less you can change the value and activate it in the numbered area **(12)**.

### Set custom acceleration, speed and IP for the cobot
In the zone **(13)** is all the part concerning the cobot, you can also modify the velocity and the acceleration (do not increase them too much because it can be dangerous for you and people around).

### Select app theme
The switch button **(14)** simply allows changing the color of the background of the graphic interface, either black or white.

### Opening the documentation
The button **(15)** opens a new window containing this file. The main goal is for users to have an easy way of understanding our software with the documentation included.

# 4. User Guide : Universal Robot Tablet HMI
## A. UR3

> [!INFO] > In this part, you will learn how to use the software of the constructor. Skip to 5 if you want to access the global code explanation.

![[UR_teach-pendant 1.jpg]]
<p class="textcenter">Teach Pendant - designed by Universal Robots</p>

We can find 4 main buttons on the user interface of the cobot run program, program cobot, setup cobot and shutdown cobot.

The first button Run program allows you to check the different variables that are active when the program is launched.

![[20230124_084029.jpg]]
<p class="textcenter">Teach Pendant - New Program Window</p>

This part which symbolizes the program cobot button allows the operator to load a file of type _urp_. The two buttons in the part used the model are used to navigate in the tree of the program.

![[20230124_084049 1.jpg]]
<p class="textcenter">Teach Pendant - Robot Configuration Window</p>

The button setup cobot allows you to make different configuration on it language, time, update ...

![[20230124_083935.jpg]]
<p class="textcenter">Teach Pendant - Robot Control Interface</p>

In the first two buttons (run program, program cobot) there is an interface called Move which is used to make manual movements on the cobot.
The first part allows you to move the cobot laterally and to move it up and down.

The second part at the bottom is used to make rotations on the axes of the cobot.
You can also fill in the fields on the right and then press the start button which will generate the movement.

For all interfaces, if you want to go back to the main menu, you can click on **fichier** and after **quit**.

If you want to turn off the cobot engine you need to click on the led (close to the button fichier).

## B. UR3e

> [!WARNING] >For UR3e, you have to click on the button Local/Remote control. The software isn't currently working with the UR3e.

![[IMG_20230313_163038_072.jpg]]
<p class="textcenter">Teach Pendant - Activating Local/Remote control</p>

# 5. Software global explanation

The software could be summarized as follows :
- You connect to the cobot
- You get TCP or joints value
- You modify them
- You send them back to the cobot
- The cobot moves

### Example of code to get joints values
**![](https://lh4.googleusercontent.com/TGqB947hF3RVV9nfXTXkYB1CZJMevcs0oRUULaSMfEniSRF5vrVLphAfSyRiIH40kt_n1kzgMqETylVZ8XMkY4LbGH4veb7HL-b7vlISjM7-gVgwgf4FmQ7Ku4Nwbmu_OKy4MX5G9kZTV5Wh-Tm8xo9iqXg9X0oOxjAWEBKvu5_nLQgMTBp169mDrsGgBpSU=s2048)**

### Example of code to move the cobot according to joints values

**![](https://lh4.googleusercontent.com/-RwiXDQnjTNWF6H2EEWBqyd22URAK6E5eebw9rDckTEIaM2Pqzh_MOnDyr_CO70-BKL95SYxiuqESdDrPBf_OUXUTGwbm-xMSIrO5G7mzHlJ2d9wG7LmAUdEYq9V1J6rhqOGiTH3tnE936Q5I1rfd_J1rHgL5xNouZbCdOfErRe7tVzfKzwRe7pFAH3AJn01=s2048)

> [!WARNING] >Be aware that the code presented, will not work if typed as follow into an editor, it require you to remove oriented objected programming aspect of the code and to make sure you have imported all required libraries.

### Global code explanation
![[cobot.png]]
<p class="textcenter">Explanation of URSarii class</p>

> [!success] > Congratulations, you've reached the end 🥳