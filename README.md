## Simple python script to lock manjaro when a bluetooth device (e.g. smartphone, smartwatch) is not connected or too far away from the computer.

I use it on manjaro with i3wm in conky.

### Setup

Requires
 
 * python 3.7 and package pybluez 
 * hcitool - linux tool
 * slock - locker (you can change the locker, see constants in bluetooth_slock_proximity.py)
 * awesome font (optional, usefull for conky)


#### Sample of how my i3 bar looks

When android is connected there is an OK sign next to it, when it's not, a X appears instead.

![i3bar](https://i.imgur.com/GQCpGMB.png)


TODO

[ ] Refactor
[ ] Document

