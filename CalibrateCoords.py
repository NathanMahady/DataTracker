import pyautogui
from pynput import mouse

def on_click(x, y, button, pressed):
    # Button.right
    if pressed:
        if str(button) == "Button.right":
            global xPos, yPos
            xPos = x
            yPos = y
            # print(f"x:{x} y:{y}")
            return False
        
def returnMousePosition(message):
    print(message)
    with mouse.Listener(
        on_click = on_click
    ) as listener:
        listener.join() 
    
    return xPos, yPos

# for i in range(5): 
# print(returnMousePosition("Right click for coords"))