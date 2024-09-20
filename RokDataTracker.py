import pyautogui
import keyboard
import pandas as pd
import time
import pyperclip
from glob import glob
import time
from Screenshot import screenshotProfile, screenshotKillTiers, screenshotTotalDeads, screenshotTotalDeadsForTracker
import NavProfile

import ImageToData
import ImageToDataEasyOCR

from FileFunctions import writeNametoFile

from CalibrateCoords import returnMousePosition
import csv

import warnings
warnings.filterwarnings("ignore")
  
def captureScreenShots(numProfiles=10, startFrom=0, skipStart=False):
    playerNames = []
    # Skip the players with power ranking in this list
    skipTrackerPlayerProfile = [235]

    # Only needed the first time running this 
    
    #createEmptyNameFile()
    #makeProfileDirectory()

    # Handling the first 3 profiles 
    if skipStart == False:
        with open("playerNames.txt", 'w'):
            pass
    else:
        with open("playerNames.txt", 'r', encoding='utf-8') as file:
            playerNames = file.read().splitlines()
    
    i = startFrom
    if i < 3 and skipStart == False:
        profileHeight = 150
        #        for yCoord in range(475, 776, 150):
        for deltaY in range(0+i, 3):
            if keyboard.is_pressed('esc'):  # Check if the hotkey is pressed
                print("Hotkey pressed, stopping script.")
                return  # Exit the function to stop the script    
    
            # 475 is the how many pixels deep the first profile is located
            yCoord = 475 + profileHeight*deltaY
            NavProfile.clickProfile(y=yCoord,wait=0.5)
            NavProfile.copyName(wait=0.5)
            screenshotProfile(counter=i)
            with open('playerNames.txt', 'a', encoding='utf-8') as file:
                file.write(f"{pyperclip.paste()}\n")
            playerNames.append(pyperclip.paste())
            NavProfile.clickKillTiers()
            screenshotKillTiers(counter=i, wait=0.3)
            NavProfile.clickMoreInfo(0.5)
            screenshotTotalDeads(counter=i, wait=0.5)
            NavProfile.closeMoreInfo(0)
            NavProfile.closeProfile(0.3)
            i += 1

    while i < numProfiles:
        # Exits loop if esc is pressed
        if keyboard.is_pressed('esc'): 
            print("Hotkey pressed, stopping script.")
            return  # Exit the function to stop the script    
        NavProfile.clickProfile(wait=0.5)  
        
        # Code that checks if current player ranking is in skipTrackerPlayerProfile 
        # and skips clicking name if it is to avoid repeating
        
        if i+1 in skipTrackerPlayerProfile:
            time.sleep(1)
            screenshotProfile(counter=i)
            with open('playerNames.txt', 'a', encoding='utf-8') as file:
                file.write("\n")

            # Adding a placehold name for the skipped player
            playerNames.append("")
            NavProfile.clickKillTiers()
            screenshotKillTiers(counter=i, wait=0.5)
            NavProfile.clickMoreInfo(0.5)
            screenshotTotalDeadsForTracker(counter=i, wait=0.5)
            NavProfile.closeMoreInfo(0)
            NavProfile.closeProfile(0.3)
            i += 1
            continue
        
        NavProfile.copyName(wait=0.8) 
        
        currUser = pyperclip.paste()

        # Scrolls back up one player to try screenshot the missed player
        if currUser in playerNames:
            print(f"Skipped {currUser}")
            NavProfile.closeProfile(wait=1)
            NavProfile.scrollUp()
            continue
        
        screenshotProfile(counter=i)
        
        playerNames.append(pyperclip.paste())
        with open('playerNames.txt', 'a', encoding='utf-8') as file:
            file.write(f"{pyperclip.paste()}\n")
            
        NavProfile.clickKillTiers()
        screenshotKillTiers(counter=i, wait=0.5)
        NavProfile.clickMoreInfo(0.5)
        screenshotTotalDeads(counter=i, wait=0.6)
        NavProfile.closeMoreInfo(0)
        NavProfile.closeProfile(0.3)
        i += 1

def extractDataFromProfiles(numProfiles=5):
    profilesPaths = []
    for i in range(0, numProfiles):
        profilesPaths.append(f"Profiles\\screenshot-{i}.png")     
    
    player_ids = ImageToData.process_images(profilesPaths, ImageToData.returnPlayerID)
    power = ImageToData.process_images(profilesPaths, ImageToData.returnPlayerPower)
    kp = ImageToData.process_images(profilesPaths, ImageToData.returnPlayerKP)
    
    return player_ids, power, kp
   
def extractDataFromDeads(numProfiles=5):
    totalDeadsPaths = []
    for i in range(0, numProfiles):
        totalDeadsPaths.append(f"TotalDeads\\screenshot-{i}.png")     
    
    totalDeads = ImageToData.process_images(totalDeadsPaths, ImageToData.returnPlayerTotalDeads)
    return totalDeads

def extractDataFromKillTiers(numProfiles=5, kp_list=None):
    killTiersPaths = []
    for i in range(0, numProfiles):
        killTiersPaths.append(f"KillTiers\\screenshot-{i}.png")     
    killTiers = ImageToData.process_images(killTiersPaths, ImageToData.returnPlayerKillTiers, kp_list)
    return killTiers

def dataToCSV(player_ids, power, kp, deads, killTiers, numProfiles):
    with open('playerNames.txt', 'r', encoding='utf-8') as file:
        playerNames = [line.strip() for line in file.readlines()]

    playerNames = playerNames[0:numProfiles]
    
    data = {
        'Username': playerNames,
        'ID': player_ids,
        'Power': power,
        'KP': kp,
        'TotalDeads': deads,
        'T1': [t1[0] for t1 in killTiers],
        'T2': [t2[1] for t2 in killTiers],
        'T3': [t3[2] for t3 in killTiers],
        'T4': [t4[3] for t4 in killTiers],
        'T5': [t5[4] for t5 in killTiers]
    }

    df = pd.DataFrame(data)

    # Sample top of dataframe
    print(df.head())

    # Save the DataFrame to a CSV file
    df.to_csv('players_data.csv', index=False, encoding='utf-8')

def main():
    numProfiles = 5
    
    # captureScreenShots(numProfiles=numProfiles, startFrom=219, skipStart=True)
    # captureScreenShots(numProfiles=numProfiles)
    
    player_ids, power, kp = extractDataFromProfiles(numProfiles=numProfiles)
    deads = extractDataFromDeads(numProfiles=numProfiles)

    # Checks if kp was extracted from the images above, if not it uses the kp already in players_data
    if 'kp' in vars():
        killTiers = extractDataFromKillTiers(numProfiles, kp)        
    else:
        # If kp isnt defined, read kp from the csv
        df = pd.read_csv('players_data.csv')
        kp = df['KP'].tolist()
        killTiers = extractDataFromKillTiers(numProfiles, kp)
        
    dataToCSV(player_ids, power, kp, deads, killTiers, numProfiles)

if __name__ == "__main__":
    print("Press 'Esc' to stop the script.")
    start_time = time.time()
    main()
    end_time = time.time()

    # Calculate execution time
    execution_time = end_time - start_time
    print(f"Execution time: {round(execution_time,2)} seconds")