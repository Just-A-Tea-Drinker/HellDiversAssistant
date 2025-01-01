import sys
import sounddevice as sd
import queue
import vosk
import json
import time



#speech recogntion
import speech_recognition as sr

import threading 
#TTS
import pyttsx3
#keyboard input
from pyKey import pressKey, releaseKey, press, sendSequence, showKeys
#similarity
import Levenshtein

import time
model_path = "vosk-model-small-en-us-0.15"  # Update with your model path
model = vosk.Model(model_path)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def recognize_speech():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Please say something...")
        start =time.time()
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                end = time.time()
                print("You said: " + result['text'])
                return result['text']
                print(end-start)
                break
class Stratagems:
    strategem_names = []
    strategems_codes = []
    strat_chosen = ''
    def __init__(self):
        with open("stratagems.txt", 'r') as file:
            content = file.readlines()
        for lines in content:
            
            line = lines.strip().split()
            if len(line)>1:
                self.strategem_names.append(line[0])
                self.strategems_codes.append(line[1])
        
       
        

            
    def InputController(self,strat):
        #turning the strategem into keyboard presses
        self.HoldCRTL()
        time.sleep(1)
        print(strat)
        for char in strat:
            if char == "W":
                self.PressW()
            if char == "A":
                self.PressA()
            if char == "S":
                self.PressS()
            if char == "D":
                self.PressD()
            time.sleep(0.05)
            
        self.RelCRTL()
    #small functions used to actually press the buttons      
    def PressW(self):
        pressKey('w')
        
        time.sleep(0.02)
        releaseKey('w')
    
    def PressA(self):
        pressKey('a')
        
        time.sleep(0.02)
        releaseKey('a')
    
    def PressS(self):
        pressKey('s')
        
        time.sleep(0.02)
        releaseKey('s')
    
    def PressD(self):
        pressKey('d')
        
        time.sleep(0.02)
        releaseKey('d')
    
    def HoldCRTL(self):
        pressKey('CTRL')

    def RelCRTL(self):
        releaseKey('CTRL')
        


 
class HandsFreeStrategems:
    rec = None
    eng = None
    get_strat = False
    strat_obj = None
    keywords = []
    def __init__(self):
        self.rec = sr.Recognizer()
        self.eng = pyttsx3.init()
        self.strat_obj = Stratagems()
        with open("keywords.txt", 'r') as file:
            content = file.readlines()
        for lines in content:
            
            line = lines.strip()
            
            self.keywords.append(line)
        self.UpdateLoop()
        

    def UpdateLoop(self):
        #simple update loop for STT
        while True:
            text =recognize_speech()
            self.KeywordSearch(text)
           
         
    def HelperSpeech(self,speech):
        #simple speech function used to parse in a string to be spoken back by TTS
        self.eng.say(speech)
        self.eng.runAndWait()

        
    def ConfidenceCheck(self,strat):
        #compares the compiled test "strategem" to the bank stratagem and selects it
        confidence = []
        for strats in self.strat_obj.strategem_names:
             confidence.append(Levenshtein.ratio(strats, strat))
        best = max(confidence)
        strat_chosen = self.strat_obj.strategem_names[confidence.index(best)]
        
        return confidence.index(best)
            
    def KeywordSearch(self,words):
        word_split = words.upper().strip().split()
        count= 0

        #checking for the "wake up" command
        if len(word_split)>1:
            if word_split[0]+word_split[1] == "WAKEUP":
                self.get_strat =True
                self.HelperSpeech("i'm ready to liberate")
        #checking for "sleep command"
        if len(word_split)>0:
        
            if word_split[0] == "SLEEP" and self.get_strat == True:
                self.get_strat =False
                self.HelperSpeech("returning to civillian life")
        #if active checks for keywords to select a stratagem

        #finds keyword close together to compile in to a strategem
        if self.get_strat == True:
            key_words=[]
            for word in word_split:
                if word in self.keywords and count<5:
                    key_words.append(word)
                    count+=1
            if len(key_words)>0:
                to_check = '_'.join(key_words)
                #checks the likiness and select the closest match
                response = self.strat_obj.strategem_names[self.ConfidenceCheck(to_check)]
                code = self.strat_obj.strategems_codes[self.strat_obj.strategem_names.index(response)]
                self.strat_obj.InputController(code)
                


if __name__ == "__main__":
    obj = HandsFreeStrategems()
    
    
    
