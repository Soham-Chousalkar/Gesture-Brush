#Import required Libraries
import cv2
import numpy as np

# Try to import mediapipe, if not available, show error
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    print("MediaPipe is not available. Please install it with: pip install mediapipe")
    print("For Python 3.13, you might need to use a different version or alternative.")
    MEDIAPIPE_AVAILABLE = False

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

#Mode Selection:: Middle finger positions: MIDDLE_FINGER_TIP - MIDDLE_FINGER_PIP
def fingers_up(y12, y10):
	if y10>y12:
		return True
	return False

def main():
    if not MEDIAPIPE_AVAILABLE:
        print("Cannot run without MediaPipe. Please install it first.")
        return
    
    #Detecting Hand Initialisation
    hands = mp.solutions.hands
    hand_landmark = hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=1)
    draw = mp.solutions.drawing_utils
    drawColor = mp.solutions.drawing_styles

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
    
    mask = np.zeros((480, 640, 3), np.uint8)

    #Implementation
    cap = cv2.VideoCapture(0)
    cap.set(3, 480)
    cap.set(4, 640)

    print("Gesture Brush Started!")
    print("Controls:")
    print("- Point to top area to select tools")
    print("- Point to left area to select colors")
    print("- Use index finger to draw")
    print("- Press ESC to exit")

    while True:
        _, frm = cap.read()
        frm = cv2.flip(frm, 1)
        rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
        op = hand_landmark.process(rgb)
        if op.multi_hand_landmarks:
            for i in op.multi_hand_landmarks:
                draw.draw_landmarks(frm, i, hands.HAND_CONNECTIONS, drawColor.get_default_hand_landmarks_style(), drawColor.get_default_hand_connections_style())
                x_ind, y_ind = int(i.landmark[8].x*640), int(i.landmark[8].y*480)
                # set color 
                if x_ind<50 and y_ind>60 and y_ind<260:
                    cv2.circle(frm, (x_ind, y_ind), crad, (0,0,0), 3)			
                    curr_color = getColor(y_ind)
                    frm[:40,55:95] = curr_color
                    #print("your current color is set to : ", curr_color)
                # select tool
                if y_ind<50 and x_ind>150 and x_ind<400:
                    cv2.circle(frm, (x_ind, y_ind), trad, (0,0,0), 3)
                    curr_tool = getTool(x_ind)
                    #print("your current tool is set to : ", curr_tool)
                #Detecting positions 12,10
                y12 = int(i.landmark[12].y*480)
                y10 = int(i.landmark[10].y*480)
                # Freehand Drawing
                if curr_tool == "Draw":
                    # select
                    if fingers_up(y12, y10):
                        cv2.line(mask, (x_prev, y_prev), (x_ind, y_ind), curr_color, bthickness)
                        x_prev, y_prev = x_ind, y_ind
                    # fix
                    else:
                        x_prev = x_ind
                        y_prev = y_ind
                # Drawing Line	 
                elif curr_tool == "Line":
                    # select
                    if fingers_up(y12, y10):
                        if not(var_inits):
                            x_ind_old, y_ind_old = x_ind, y_ind
                            var_inits = True
                        cv2.line(frm, (x_ind_old, y_ind_old), (x_ind, y_ind), curr_color, bthickness)
                    # fix
                    else:
                        if var_inits:
                            cv2.line(mask, (x_ind_old, y_ind_old), (x_ind, y_ind), curr_color, bthickness)
                            var_inits = False
                # Drawing Rectangle
                elif curr_tool == "Rectangle":
                    # select
                    if fingers_up(y12, y10):
                        if not(var_inits):
                            x_ind_old, y_ind_old = x_ind, y_ind
                            var_inits = True
                        cv2.rectangle(frm, (x_ind_old, y_ind_old), (x_ind, y_ind), curr_color, bthickness)
                    # fix
                    else:
                        if var_inits:
                            cv2.rectangle(mask, (x_ind_old, y_ind_old), (x_ind, y_ind), curr_color,bthickness)
                            var_inits = False
                # Drawing Circle
                elif curr_tool == "Circle":
                    # select
                    if fingers_up(y12, y10):
                        if not(var_inits):
                            x_ind_old, y_ind_old = x_ind, y_ind
                            var_inits = True
                        cv2.circle(frm,(x_ind_old,y_ind_old),int(((x_ind_old-x_ind)**2+(y_ind_old-y_ind)**2)**0.5),curr_color,bthickness)
                    # fix
                    else:
                        if var_inits:
                            cv2.circle(mask,(x_ind_old,y_ind_old),int(((x_ind_old-x_ind)**2+(y_ind_old-y_ind)**2)**0.5),curr_color,bthickness)
                            var_inits = False
                # Erase			
                elif curr_tool == "Erase":
                    # erasing
                    if fingers_up(y12, y10):
                        cv2.circle(frm, (x_ind, y_ind), erad, (0,0,0), -1)
                        cv2.circle(mask, (x_ind, y_ind), erad, 0, -1)

        #Frame and Mask Integration				
        graym=cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
        _, inv=cv2.threshold(graym,50,255,cv2.THRESH_BINARY_INV)
        inv=cv2.cvtColor(inv,cv2.COLOR_GRAY2BGR)
        frm=cv2.bitwise_and(frm,inv)
        frm=cv2.bitwise_or(frm,mask)

        frm[:50,150:400] = cv2.addWeighted(tools, 0.7, frm[:50,150:400], 0.3, 0)
        frm[:260,:50]=cv2.addWeighted(colors,0.7,frm[:260,:50],0.3,0)
        cv2.putText(frm, curr_tool, (420,30), cv2.FONT_HERSHEY_TRIPLEX, 1, curr_color, 2)
        cv2.imshow("Gesture Brush", frm)
        cv2.imshow("maskgray",graym)
        cv2.imshow("mask",mask)
        cv2.imshow("inv",inv)
        
        if cv2.waitKey(1) == 27: #Esc key
            cv2.destroyAllWindows()
            cap.release()
            break

if __name__ == "__main__":
    main() 