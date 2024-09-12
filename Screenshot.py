import os
import pyautogui
import time

def screenshotProfile(counter, wait=0):
    time.sleep(wait)
    path = os.getcwd() + f"\\Profiles\\screenshot-{counter}.png"
    # Coordinates of top left and size of image
    pyautogui.screenshot(path, region=(950,330,1130,290))
    counter += 1
    
def screenshotTotalDeads(counter, wait=0):
    time.sleep(wait)
    path = os.getcwd() + f"\\TotalDeads\\screenshot-{counter}.png"
    # Coordinates of top left and size of image
    pyautogui.screenshot(path, region=(1803,700,230,55))
    
    counter += 1
    
def screenshotTotalDeadsForTracker(counter, wait=0):
    time.sleep(wait)
    path = os.getcwd() + f"\\TotalDeads\\screenshot-{counter}.png"
    # Coordinates of top left and size of image
    pyautogui.screenshot(path, region=(1788,1140,230,55))
    counter += 1
    
def screenshotKillTiers(counter, wait=0):
    time.sleep(wait)
    path = os.getcwd() + f"\\KillTiers\\screenshot-{counter}.png"
    # Coordinates of top left and size of image
    pyautogui.screenshot(path, region=(1358,667,235,333))
    counter += 1
    
screenshotTotalDeads(counter=159)