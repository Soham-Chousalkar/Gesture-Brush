import cv2
import numpy as np

#Constants
curr_tool = "Select Tool"
curr_color = (22, 22, 255) #Default color: bright red
trad = 15 #tools selection radius
crad = 15 #color selection radius 
var_inits = False #variables initialised? No
bthickness = 4 #brush thickness
erad = 30 #erase radius
x_prev, y_prev = 0, 0 #initalize variables

#Select Tool function
def getTool(x):
	if x<200:
		return "Draw"
	elif x<250:
		return "Line"
	elif x <300:
		return"Rectangle"
	elif x<350:
		return "Circle"
	else:
		return "Erase"

#Select Color function
def getColor(y):
    if y<100:
        return (89, 222, 255) #Yellow
    elif y<140:
        return (87, 217, 126) #Grass Green
    elif y<180:
        return (203, 194, 0) #Aqua Blue
    elif y<220:
        return (22, 22, 255) #Bright Red
    else:
        return (230, 108, 203) #Magenta	

def main():
    print("Gesture Brush Demo Mode")
    print("This is a demo version without hand tracking.")
    print("The full version requires MediaPipe which is not available for Python 3.13.")
    print("Controls:")
    print("- Click and drag to draw")
    print("- Use mouse to select tools and colors")
    print("- Press ESC to exit")
    
    #Canvas Visualisation
    try:
        tools = cv2.imread("tools.png")
        colors=cv2.imread("colors.png")
        if tools is None or colors is None:
            print("Warning: tools.png or colors.png not found. Creating blank images.")
            tools = np.zeros((50, 250, 3), dtype=np.uint8)
            colors = np.zeros((260, 50, 3), dtype=np.uint8)
    except:
        print("Warning: Could not load tool/color images. Creating blank images.")
        tools = np.zeros((50, 250, 3), dtype=np.uint8)
        colors = np.zeros((260, 50, 3), dtype=np.uint8)
    
    # Global variables
    global mask, drawing, last_x, last_y
    mask = np.zeros((480, 640, 3), np.uint8)
    drawing = False
    last_x, last_y = 0, 0
    
    # Create a window
    cv2.namedWindow("Gesture Brush Demo")
    cv2.setMouseCallback("Gesture Brush Demo", mouse_callback)

    while True:
        # Create a frame
        frm = np.ones((480, 640, 3), dtype=np.uint8) * 255  # White background
        
        # Add tool and color areas
        frm[:50,150:400] = cv2.addWeighted(tools, 0.7, frm[:50,150:400], 0.3, 0)
        frm[:260,:50]=cv2.addWeighted(colors,0.7,frm[:260,:50],0.3,0)
        
        # Add current tool text
        cv2.putText(frm, curr_tool, (420,30), cv2.FONT_HERSHEY_TRIPLEX, 1, curr_color, 2)
        
        # Add mask overlay
        frm = cv2.bitwise_or(frm, mask)
        
        cv2.imshow("Gesture Brush Demo", frm)
        
        if cv2.waitKey(1) == 27: #Esc key
            cv2.destroyAllWindows()
            break

def mouse_callback(event, x, y, flags, param):
    global drawing, last_x, last_y, curr_tool, curr_color, mask
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_x, last_y = x, y
        
        # Tool selection
        if y < 50 and x > 150 and x < 400:
            curr_tool = getTool(x)
            print(f"Selected tool: {curr_tool}")
            
        # Color selection
        if x < 50 and y > 60 and y < 260:
            curr_color = getColor(y)
            print(f"Selected color: {curr_color}")
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing and 'mask' in globals():
            if curr_tool == "Draw":
                cv2.line(mask, (last_x, last_y), (x, y), curr_color, 4)
            elif curr_tool == "Erase":
                cv2.circle(mask, (x, y), 30, (0,0,0), -1)
            last_x, last_y = x, y
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

if __name__ == "__main__":
    main() 