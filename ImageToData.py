import pytesseract
from glob import glob
from PIL import Image
import re
import cv2
import math 
import ImageToDataEasyOCR
import easyocr

# Setting tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def returnPlayerID(profilePic):
    print(f"{profilePic} (ID)")
    # Governor ID location
    crop_area = (0, 0, 423, 47)
    
    image = Image.open(profilePic)

    # Crop the image to show Gov ID
    cropped_image = image.crop(crop_area)
    # cropped_image.show()
    
    # Use pytesseract to extract text from the cropped area
    # Sample of text = "Governor(!D: 78648664)"
    text = pytesseract.image_to_string(cropped_image, lang="eng")
    
    # Extracts only the number part of the text
    match = re.search(r'\d+', text)
    if match:
        playerID = match.group()
    # If no match found return 0
    else: 
        playerID = 0
        
    return int(playerID)
    
def returnPlayerPower(profilePic):
    print(f"{profilePic} (Power)")
    crop_area = (440, 205, 700, 250)
    
    image = Image.open(profilePic)

    # Crop the image to show Gov ID
    cropped_image = image.crop(crop_area)
    #cropped_image.show()
    
    # Use pytesseract to extract text from the cropped area
    text = pytesseract.image_to_string(cropped_image, lang="eng")
    
    # Remove commas
    power = text.replace(',', '').strip()
    return(int(power))

def returnPlayerKP(profilePic):
    print(f"{profilePic} (kp)")
    crop_area = (820, 204, 1125, 256)
    
    image = Image.open(profilePic)

    # Crop the image to show Gov ID
    cropped_image = image.crop(crop_area)
    # cropped_image.show()
    
    # Use pytesseract to extract text from the cropped area
    text = pytesseract.image_to_string(cropped_image, lang="eng")    
    kp = text.replace(',', '').strip()
    
    # Special case where tesseract fails to recognize a single 0
    if kp == "":
        kp = 0
        
    return(int(kp))

def returnPlayerTotalDeads(profilePic):
    print(f"{profilePic}")
    image = Image.open(profilePic)   
    # image.show()
    text = pytesseract.image_to_string(image, lang="eng")
    text = text.replace(',', '').strip()
    
    if text == "":
        deads = 0
    else:     
        try:
            # Attempt to convert the text to an integer
            deads = int(text)
        except ValueError:
            print("Tesseract Interpreted String")
            return ImageToDataEasyOCR.returnPlayerTotalDeads(profilePic)     
    # print(profilePic)
    return deads


def returnPlayerKillTiers(profilePic, kp=None):
    print(f"{profilePic} (Tesseract)")
    image = Image.open(profilePic)  
    
    # Initialize an empty list to hold the processed numbers
    tiers = []
    
    slidingWindowY = 66
    trim_amount = 5  # Number of pixels to trim from top and bottom
    
    # Factor by which to resize the cropped image
    resize_factor = 2  # Increase the size by 2x
    
    # Divides KillTier images into 5 equally sized windows
    for slide in range(5):
        crop_area = (0, slidingWindowY * slide + trim_amount, 235, slidingWindowY * (slide+1) - trim_amount)
        cropped_image = image.crop(crop_area)
        
        # Resize the cropped image to make text larger
        new_size = (cropped_image.width * resize_factor, cropped_image.height * resize_factor)
        resized_image = cropped_image.resize(new_size, Image.Resampling.LANCZOS)
        # resized_image.show()

        text = pytesseract.image_to_string(resized_image)    
        text = text.strip().replace(',', '')
        
        if text == "":
            tiers.append(0)
            continue

        try:
            # Attempt to convert the text to an integer
            tiers.append(int(text))
        except ValueError:
            return ImageToDataEasyOCR.returnPlayerKillTiers(profilePic,kp, tiers)

    if kp == calculate_kp_from_tiers(tiers):     
        return tiers
    
    else:
        return ImageToDataEasyOCR.returnPlayerKillTiers(profilePic,kp, tiers)

def process_images(imagePaths, extractionFunction, kp_list=None):
    results = []
    
    if(kp_list == None):
        for imagePath in imagePaths:
            result = extractionFunction(imagePath)
            results.append(result)
        return results
    
    else:
        for i in range(len(imagePaths)):
            result = extractionFunction(imagePaths[i], kp_list[i])
            results.append(result)
        return results
    
def calculate_kp_from_tiers(tiers):
    return math.floor(tiers[0]/5 + tiers[1]*2 + tiers[2]*4 + tiers[3]*10 + tiers[4]*20)

# Storing all image names in a list
# profilesPaths = glob('Profiles/screenshot*')
# import random
# randnum = random.randint(0,9)
# print(returnPlayerKillTiers(f"KillTiers/screenshot-{1}.png"))
# print(process_images(profilesPaths, returnPlayerPower))
# print(process_images(profilesPaths, returnPlayerKP))
# print(process_images(profilesPaths, returnPlayerID))

# print(returnPlayerKillTiers(f"KillTiers/screenshot-{285}.png"))