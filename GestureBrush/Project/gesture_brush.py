import cv2
import numpy as np
import math

# Constants
curr_tool = "Select Tool"
curr_color = (22, 22, 255)  # Default color: bright red
trad = 15  # tools selection radius
crad = 15  # color selection radius 
var_inits = False  # variables initialised? No
bthickness = 4  # brush thickness
erad = 30  # erase radius
x_prev, y_prev = 0, 0  # initialize variables

# Hand landmarks (similar to MediaPipe)
HAND_LANDMARKS = {
    'WRIST': 0,
    'THUMB_TIP': 4,
    'INDEX_FINGER_TIP': 8,
    'MIDDLE_FINGER_TIP': 12,
    'RING_FINGER_TIP': 16,
    'PINKY_TIP': 20,
    'INDEX_FINGER_PIP': 6,
    'MIDDLE_FINGER_PIP': 10,
    'RING_FINGER_PIP': 14,
    'PINKY_PIP': 18
}

def getTool(x):
    """Select tool based on x position"""
    if x < 200:
        return "Draw"
    elif x < 250:
        return "Line"
    elif x < 300:
        return "Rectangle"
    elif x < 350:
        return "Circle"
    else:
        return "Erase"

def getColor(y):
    """Select color based on y position"""
    if y < 100:
        return (89, 222, 255)  # Yellow
    elif y < 140:
        return (87, 217, 126)  # Grass Green
    elif y < 180:
        return (203, 194, 0)  # Aqua Blue
    elif y < 220:
        return (22, 22, 255)  # Bright Red
    else:
        return (230, 108, 203)  # Magenta

def detect_hand_landmarks(frame):
    """Advanced hand detection with landmark tracking"""
    # Convert to HSV for better skin detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range for skin color (more specific for palm)
    lower_skin = np.array([0, 30, 60], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create mask for skin color
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Apply morphological operations to clean up the mask
    kernel = np.ones((3, 3), np.uint8)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Filter contours by area to focus on hand-sized objects
        hand_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 5000 and area < 50000:  # Filter by reasonable hand size
                hand_contours.append(contour)
        
        if hand_contours:
            # Get the largest contour (assumed to be hand)
            largest_contour = max(hand_contours, key=cv2.contourArea)
            
            # Get convex hull and defects for finger detection
            hull = cv2.convexHull(largest_contour, returnPoints=False)
            defects = cv2.convexityDefects(largest_contour, hull)
            
            # Extract landmarks
            landmarks = extract_landmarks(largest_contour, defects)
            
            return landmarks, largest_contour
    
    return None, None

def extract_landmarks(contour, defects):
    """Extract hand landmarks from contour and defects"""
    landmarks = {}
    
    # Find extreme points
    leftmost = tuple(contour[contour[:, :, 0].argmin()][0])
    rightmost = tuple(contour[contour[:, :, 0].argmax()][0])
    topmost = tuple(contour[contour[:, :, 1].argmin()][0])
    bottommost = tuple(contour[contour[:, :, 1].argmax()][0])
    
    # Wrist (bottom center)
    landmarks[HAND_LANDMARKS['WRIST']] = bottommost
    
    # Find finger tips using convexity defects
    finger_tips = []
    if defects is not None:
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i][0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
            
            # Calculate distances
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            
            # Calculate angle
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            
            # If angle is less than 90 degrees, it's likely a finger
            if angle <= 90:
                finger_tips.append(end)
    
    # Assign finger tips to landmarks
    if len(finger_tips) >= 1:
        landmarks[HAND_LANDMARKS['INDEX_FINGER_TIP']] = finger_tips[0]
    if len(finger_tips) >= 2:
        landmarks[HAND_LANDMARKS['MIDDLE_FINGER_TIP']] = finger_tips[1]
    if len(finger_tips) >= 3:
        landmarks[HAND_LANDMARKS['RING_FINGER_TIP']] = finger_tips[2]
    if len(finger_tips) >= 4:
        landmarks[HAND_LANDMARKS['PINKY_TIP']] = finger_tips[3]
    
    # Use topmost point as index finger tip if no defects found
    if HAND_LANDMARKS['INDEX_FINGER_TIP'] not in landmarks:
        landmarks[HAND_LANDMARKS['INDEX_FINGER_TIP']] = topmost
    
    return landmarks

def fingers_up(landmarks):
    """Check if fingers are up (similar to MediaPipe logic)"""
    if not landmarks:
        return False
    
    # Check if index finger is up (y position of tip < y position of wrist)
    if HAND_LANDMARKS['INDEX_FINGER_TIP'] in landmarks and HAND_LANDMARKS['WRIST'] in landmarks:
        index_tip = landmarks[HAND_LANDMARKS['INDEX_FINGER_TIP']]
        wrist = landmarks[HAND_LANDMARKS['WRIST']]
        return index_tip[1] < wrist[1]  # Finger tip above wrist
    
    return False

def main():
    global curr_tool, curr_color, x_prev, y_prev
    
    print("Gesture Brush - Hand Landmark Tracking")
    print("This version uses advanced hand landmark detection.")
    print("Controls:")
    print("- Show your hand to the camera")
    print("- Point with your index finger to draw")
    print("- Point to top area to select tools")
    print("- Point to left area to select colors")
    print("- Press ESC to exit")
    
    # Canvas Visualization
    try:
        tools = cv2.imread("tools.png")
        colors = cv2.imread("colors.png")
        if tools is None or colors is None:
            print("Warning: tools.png or colors.png not found. Creating blank images.")
            tools = np.zeros((50, 250, 3), dtype=np.uint8)
            colors = np.zeros((260, 50, 3), dtype=np.uint8)
    except:
        print("Warning: Could not load tool/color images. Creating blank images.")
        tools = np.zeros((50, 250, 3), dtype=np.uint8)
        colors = np.zeros((260, 50, 3), dtype=np.uint8)
    
    mask = np.zeros((480, 640, 3), np.uint8)

    # Implementation
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        _, frm = cap.read()
        frm = cv2.flip(frm, 1)
        
        # Detect hand landmarks
        landmarks, hand_contour = detect_hand_landmarks(frm)
        
        if landmarks and hand_contour is not None:
            # Draw hand contour
            cv2.drawContours(frm, [hand_contour], -1, (0, 255, 0), 2)
            
            # Draw landmarks
            for landmark_id, point in landmarks.items():
                cv2.circle(frm, point, 5, (255, 0, 0), -1)
                cv2.putText(frm, str(landmark_id), (point[0]+10, point[1]), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Get index finger tip for cursor
            if HAND_LANDMARKS['INDEX_FINGER_TIP'] in landmarks:
                cursor_x, cursor_y = landmarks[HAND_LANDMARKS['INDEX_FINGER_TIP']]
                
                # Draw cursor
                cv2.circle(frm, (cursor_x, cursor_y), 8, (0, 0, 255), -1)
                
                # Check if fingers are up
                fingers_extended = fingers_up(landmarks)
                
                # Set color 
                if cursor_x < 50 and cursor_y > 60 and cursor_y < 260:
                    cv2.circle(frm, (cursor_x, cursor_y), crad, (0, 0, 0), 3)
                    curr_color = getColor(cursor_y)
                    frm[:40, 55:95] = curr_color
                    
                # Select tool
                if cursor_y < 50 and cursor_x > 150 and cursor_x < 400:
                    cv2.circle(frm, (cursor_x, cursor_y), trad, (0, 0, 0), 3)
                    curr_tool = getTool(cursor_x)
                    
                # Drawing logic - draw when index finger is in drawing area and finger is extended
                if cursor_x > 100 and cursor_y > 100:  # Drawing area
                    if curr_tool == "Draw" and fingers_extended:
                        cv2.line(mask, (x_prev, y_prev), (cursor_x, cursor_y), curr_color, bthickness)
                    elif curr_tool == "Erase" and fingers_extended:
                        cv2.circle(mask, (cursor_x, cursor_y), erad, (0, 0, 0), -1)
                    
                    x_prev, y_prev = cursor_x, cursor_y
                
                # Display finger status
                status = "Fingers: UP" if fingers_extended else "Fingers: DOWN"
                cv2.putText(frm, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Frame and Mask Integration
        graym = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        _, inv = cv2.threshold(graym, 50, 255, cv2.THRESH_BINARY_INV)
        inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
        frm = cv2.bitwise_and(frm, inv)
        frm = cv2.bitwise_or(frm, mask)

        frm[:50, 150:400] = cv2.addWeighted(tools, 0.7, frm[:50, 150:400], 0.3, 0)
        frm[:260, :50] = cv2.addWeighted(colors, 0.7, frm[:260, :50], 0.3, 0)
        cv2.putText(frm, curr_tool, (420, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, curr_color, 2)
        
        # Add instructions
        cv2.putText(frm, "Show hand to camera", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow("Gesture Brush", frm)
        
        if cv2.waitKey(1) == 27:  # Esc key
            cv2.destroyAllWindows()
            cap.release()
            break

if __name__ == "__main__":
    main() 