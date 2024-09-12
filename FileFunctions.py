import os
import pyperclip

def createEmptyNameFile():
    # Deletes names.txt if it exists
    if os.path.exists("names.txt"):
        os.remove("names.txt")
        
    # Creating a new names.txt file    
    names = open("names.txt", "x")
    names.close()
    
def writeNametoFile():
    names = open("names.txt", "a", encoding="utf-8")
    
    # Writes name from clipboard to names
    names.write(pyperclip.paste()+"\n")

def makeProfileDirectory():
    path = os.getcwd() + "\Profiles"
    
    if not os.path.exists(path):
        os.makedirs(path)