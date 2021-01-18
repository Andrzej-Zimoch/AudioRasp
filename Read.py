#!/usr/bin/env python
# - *- coding: utf- 8 - *-
#imports
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from pygame import mixer
from mutagen.mp3 import MP3
import time
import os, os.path
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import alsaaudio

#SETTING MIXER
mixer.init() 
# Setting the volume    
mixer.music.set_volume(0.5)

#alsa volume
m = alsaaudio.Mixer()
vol = m.getvolume()
newVol = 100
m.setvolume(newVol)

#MCP3008 settings
SPI_PORT   = 0
SPI_DEVICE = 1
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#SETTING ENCODER FOR PAUSE/RESUME 
#FOR SWITCHING SONGS
#pins
clk = 22 #17
dt = 27 #24 
sw= 17 #23
#GPIO setting
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#First position of song Encoder
clkLastState = GPIO.input(clk)
dtLastState = GPIO.input(dt)

#current song number
global cur_song
cur_song= 0

#boolean for pausing
global isPaused
isPaused = False

#function for pausing
def pause():
    mixer.music.pause()
    global isPaused
    isPaused = True

#function for resuming        
def resume():
    mixer.music.unpause()
    global isPaused
    isPaused=False
        
#function for adding one to current song
def nextSong(album,max_song):
    global isPaused
    isPaused=False
    
    global cur_song
    cur_song += 1
    
    if (cur_song<max_song):
        time.sleep(1)
    else:
        #if there is no more songs, listen to more albums
        #print("nie ma nic więcej")
        Listen(album)

#function for subtracting one from current song
def previousSong(album,max_song):
    global isPaused
    isPaused=False
        
    global cur_song
    if (cur_song!=0):
        cur_song -=1
        
        time.sleep(1)
    else:
        cur_song=0
        time.sleep(1)

#function for playing whole album    
def playAlbum(album,song,max_song):
       
    # Loading the song 
    mixer.music.load("/media/pi/PATRIOT/Music/"+ str(album) +"/"+ str(song) +".mp3")
    #song_src = MP3('/media/pi/PATRIOT/Music/In the Court of the Crimson King/'+str(song)+'.mp3')
    #song_l = song_src.info.length
    mixer.music.play()

    # Start playing the song 
    mixer.music.play()
    print('gram')
   
    while (True):
        
        #check potentiometer
        value = mcp.read_adc(0)
        #round value and make it percentage of max volume
        #volume in mixer is set between 0 and 1 so divide by 100
        vol_value=round(value,0)
        vol_value=(value*100)/102300
        print(vol_value)
        mixer.music.set_volume(vol_value)
        
        
        #check encoder
        clkState = GPIO.input(clk)        
        dtState = GPIO.input(dt)  
        
        #turning encoder: right
        if clkState != clkLastState:
            if dtState != clkState:
                nextSong(album,max_song)
                print("w prawo:" +str(cur_song))
                playAlbum(album,cur_song,max_song)
                time.sleep(1)

        #turning encoder: left
        if dtState != dtLastState:
            if dtState != clkState:
                previousSong(album,max_song)
                print("w lewo: "+str(cur_song))
                playAlbum(album,cur_song,max_song)
                time.sleep(1)
                
        #button in encoder for pausing
        if GPIO.input(sw) == GPIO.LOW:
            print("button")
            print(isPaused)
            #while paused listen if album card was switched
            if (isPaused == False):
                pause()
                Listen(album)
                
            elif (isPaused == True):
                resume()
            
            time.sleep(0.5)

        #play next song after previous one ended
        if not(mixer.music.get_busy()):
            print("nic nie gra")
            nextSong(album,max_song)
            playAlbum(album,cur_song,max_song)
            time.sleep(1)
    

#function for looking for Album's card             
def Listen(previous_album):
    print("Szukam płyty")
    #setting RFID chip
    reader = SimpleMFRC522()
    id, text = reader.read()
    print(id)
    print(text)
    
    #below is needed to make text on cards bug free
    text=text.replace("  ","")
    if(text[-1]==" "):
        text=text[:-1]
    
    #load music album from pendrive
    lista = os.listdir("/media/pi/PATRIOT/Music/"+ str(text))
    #number of songs 
    number_files = len(lista)-1
    print("max_song: "+str(number_files))
    #list of all songs in album
    song_list =[]
    for i in range (0,number_files):
        song_list.append(i)

    #in pause state if album card was switched    
    if(text != previous_album):
        global cur_song
        cur_song = 0
        PlaySong(text,cur_song,number_files)

    #if album ended and this function is called play this album from the start     
    
    if(text == previous_album and cur_song==number_files):
        
        cur_song = 0
        PlaySong(text,cur_song,number_files)

    
 
def PlaySong(text,cur_song,number_files):
    playAlbum(text,cur_song,number_files)
    

try:
    #first listen
    #there is no previous album yet
    previous_album=""
    #Check for album card for the first time
    text,number_files = Listen(previous_album)
    ##############################
    while True:
        nextSong(text,number_files)
      
finally:
        GPIO.cleanup()










