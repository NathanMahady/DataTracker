import re
import cv2
from PIL import Image
import easyocr
import math

def returnPlayerTotalDeads(profilePic):
    print(f"{profilePic} (EasyOCR)")
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)  # For English
    # displayImage(profilePic)
    
    
    # Read text from an image
    result = reader.readtext(profilePic)

    deads = []
    for detection in result:
        deads.append(int(detection[1].replace(",","")))
   
    print(deads)
    return deads[0]

def returnPlayerKillTiers(profilePic, kp=None, tesseract_tiers=None):
    print(f"{profilePic} (EasyOCR)")
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)  # For English
    # displayImage(profilePic)
    
    
    # Read text from an image
    result = reader.readtext(profilePic)
        
    # Print the results
    tiers = []
    
    for detection in result:
        tiers.append(int(detection[1].replace(",","")))
        
    if kp == calculate_kp_from_tiers(tiers):     
        return tiers
    
    else:
        return autocorrect_tiers(tiers, tesseract_tiers, kp)

def process_images(imagePaths, extractionFunction, kp=None):
    results = []
    
    if(kp == None):
        for imagePath in imagePaths:
            result = extractionFunction(imagePath)
            results.append(result)
        return results
    
    else:
        for imagePath in imagePaths:
            result = extractionFunction(imagePath, kp, tesseract_tiers)
            results.append(result)
        return results
    
def displayImage(pathToImage):
    image = Image.open(pathToImage)   
    image.show()
    
def calculate_kp_from_tiers(tiers):
    return math.floor(tiers[0]/5 + tiers[1]*2 + tiers[2]*4 + tiers[3]*10 + tiers[4]*20)
        
def is_valid_number(value):
    """Helper function to check if a value is a valid integer."""
    try:
        int(value)
        return True
    except ValueError:
        return False

def autocorrect_tiers(easy_ocr_tiers, tesseract_tiers, actual_kp):
    print(f"easy_ocr_tiers: {easy_ocr_tiers}")
    print(f"tesseract_tiers:{tesseract_tiers}")
    print(f"actual_kp: {actual_kp}")
    
    # If EasyOCR has more than 5 numbers, trim it to the first 5
    if len(easy_ocr_tiers) > 5:
        easy_ocr_tiers = easy_ocr_tiers[:5]
    
    possible_tiers_combinations = [[]]

    # Iterate through the arrays and compare
    for i in range(5):
        if easy_ocr_tiers[i] == tesseract_tiers[i]:
            # If they agree, use this value
            for combo in possible_tiers_combinations:
                combo.append(easy_ocr_tiers[i])
        else:
            # If they disagree, and tesseract_tiers[i] is an integer
            if isinstance(tesseract_tiers[i], int):
                new_combinations = []
                for combo in possible_tiers_combinations:
                    # One combination with the easy_ocr value
                    new_combinations.append(combo + [easy_ocr_tiers[i]])
                    # Another combination with the tesseract value
                    combo.append(tesseract_tiers[i])
                possible_tiers_combinations.extend(new_combinations)
            else:
                # If tesseract_tiers[i] is not a valid integer, use only the easy_ocr value
                for combo in possible_tiers_combinations:
                    combo.append(easy_ocr_tiers[i])

    # Test all possible combinations
    for combination in possible_tiers_combinations:
        calculated_kp = calculate_kp_from_tiers(combination)
        if calculated_kp == actual_kp:
            print("Successfully corrected!")
            return combination
    
    # If none of the combinations matcked actual kp
    print("Could not match actual kp :(")
    return ["", "", "", "", ""]

    
print(returnPlayerKillTiers(f"KillTiers/screenshot-{104}.png"))
