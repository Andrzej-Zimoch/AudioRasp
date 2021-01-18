#!/usr/bin/env python
# - *- coding: utf- 8 - *-

#imports
import RPi.GPIO as GPIO
import subprocess
from mfrc522 import SimpleMFRC522
import pathlib
import os, fnmatch
from os import path

#function to call terminal
def subprocess_cmd(command):
    process = subprocess.Popen(command, shell=True)
    process.communicate()

#function to find files and change theirs names in order from 0 to max song
def nameChange(folder_selected):

        #all files
        listOfFiles = os.listdir(folder_selected)
        #extenstion filter
        pattern = "*.mp3"
        #add all .pattern files to f_list        
        f_list=[]
        for file in listOfFiles:
        
            if (fnmatch.fnmatch(file, pattern)):
                new_path=os.path.join(folder_selected,str(file))
                
                if (path.exists(new_path)):
                    f_list.append(file)

        #songs are ordered in alpabetical order right now
        #order files in order of time adding to folder
        #1. dictinary for names and times of adding to folder
        time_dic={}

        for i in f_list:
                
                fname = pathlib.Path(os.path.join(folder_selected,str(i)))
                assert fname.exists(), f'No such file: {fname}'  # check that the file exists
                #print(fname:fname.stat())
                time_dic.update({fname:fname.stat().st_ctime})


        #2. Order files         
        sorted_dict = dict( sorted(time_dic.items(),
                                key=lambda item: item[1],
                                reverse=False))

        #list of names of files
        name_list=list(sorted_dict.keys())
        print(name_list)


        #changes names starting from 0  
        num=0

        for entry in name_list:
        
            if (fnmatch.fnmatch(entry, pattern)):
                print(entry)
                
                
                if (path.exists(entry)):
                        n_path = os.path.join(folder_selected+("/%d.mp3"%num))
                        # get the path to the file in the current directory
                        src = path.realpath(entry)        
                        # rename the original file
                        os.rename(entry,n_path)
                        num +=1
        


#setting of MFRC522 chip
reader = SimpleMFRC522()
GPIO.cleanup()

#main 
try:    
        #ask for album name and spotify link
        a_name = input("New Album's name:")
        a_link = input("New Album's link:")
        
        #USB pendrive for storing songs
        loc='/media/pi/PATRIOT/Music/'
        #spotify client              
        t1="export SPOTIPY_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        #spotify secret
        t2="export SPOTIPY_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        #open terminal to download album to location
        t3='spotify_dl -l ' + a_link+ " -o "+loc
        
        subprocess_cmd(str(t1)+"; "+str(t2)+"; "+str(t3))

        nameChange(os.path.join(loc,a_name))
        
        #put RFID card on MFRC522
        print("Now place your tag to write")
        #store album name on card
        reader.write(a_name)
        print("Written")
finally:
        GPIO.cleanup()
        
        
         




