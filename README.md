# AudioRasp
## Software for raspberry pi based music system. 
### pure python

## Why did i write this

My CD player started to act funny, skipping a seconds of recording. Sure, i could have it repaired or bought a new one, but this was more fun way to do this.

## Photo of setup
![alt text](https://github.com/Andrzej-Zimoch/AudioRasp/blob/master/AudioRasp.JPG?raw=true)

## Hardware used in project

Project is based on Raspberry Pi 3 B+ with few additional things:
- Potentiometer 10k
- Rotary Encoder
- ADC chip MCP3008
- MFRC522 chip
- Pendrive big enough to have couple of hundreds of albums 
- A lot of jumperwires
- A RFID cards with frequency same as MFRC chip 

I'm also planning on adding amplifier HAT for Raspberry

# How it works?
You download songs and store album name on RFID card with WRITE.py

You play songs, control volume and change songs with READ.py

## WRITE.py
It takes album's name and link to Spotify playlist. 

Then it downloading songs with Spotipy, store them on pendrive in order from 0 to max song number

That way it's easier to make list of songs in READ.py

Album's name is stored on RFID card.

## READ.py
After putting card with album's name on MFRC chip, script is reading it and looking for coresponding folder on pendrive.

List of songs is made and it starts playing.

While playing, you can control volume with potentiometer.

With encoder you can switch songs, turning it left or right.

While pushed, encoder is pausing/resuming songs.

If you want to change album, simply put another card on reading chip and push encoder.

