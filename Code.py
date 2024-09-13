import cv2
import numpy as np
from opencv_browser_camera import BrowserCamera
import time


FRAME_CROP_Y = 200
FRAME_CROP_X = 50
FRAME_CROP_H = 400
FRAME_CROP_W = 350

TRASH_BASE_X = FRAME_CROP_W / 6
TRASH_BASE_Y = FRAME_CROP_H / 6


def crop_frame(frame):
    frame = frame[FRAME_CROP_Y:FRAME_CROP_Y+FRAME_CROP_H, FRAME_CROP_X:FRAME_CROP_X+FRAME_CROP_W]
    return frame

def draw_vertical_line(frame):
    #!! Adding a vertical blue line
    cv2.line(frame, (frame.shape[1] // 3, 0), (frame.shape[1] // 3, frame.shape[0]), (255, 0, 0), 2)

cap = BrowserCamera()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)
cap.set(cv2.CAP_PROP_FPS, 20)


# Initialize the CSRT tracker
tracker = cv2.TrackerCSRT_create()

print("waiting for valid frame")
ret, frame = cap.read()
t0 = time.time()
while not ret:
    ret, frame = cap.read()
print("valid frame found")

while (time.time() - t0) < 3:
    ret, frame = cap.read()
    pass
print("Delay elapsed")

frame = crop_frame(frame)

# Select ROI (Region of Interest) for tracking
roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
tracker.init(frame, roi)

trash_image = cv2.imread("bottle.png", cv2.IMREAD_UNCHANGED)  # Load image with alpha channel if available

trash_attached = False
trash_position = [TRASH_BASE_X, TRASH_BASE_Y]
is_won = False
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = crop_frame(frame)
    draw_vertical_line(frame)
    
    # Update the tracker and get the new position
    success, box = tracker.update(frame)
    
    if success:
        (x, y, w, h) = [int(v) for v in box]
        # Draw the bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)
        # Draw a circle at the center of the bounding box
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
        # Display the position
        cv2.putText(frame, f"Center: ({center_x}, {center_y})", (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        algae_position = (center_x, center_y)

        line_x = FRAME_CROP_W // 3
        # if (algae_position[0] < line_x):
        if abs(algae_position[0] - trash_position[0]) <= 15 and abs(algae_position[1] - trash_position[1]) <= 15:
            trash_attached = True
        elif algae_position[0] > line_x + 1:
            if trash_attached == True:
                is_won = True
            else:
                trash_attached = False

        if (is_won):
            cv2.putText(frame, "You win!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            trash_attached = False
            


        if trash_attached:
            trash_position = [algae_position[0], algae_position[1] + 10]  # Trash follows algae


        height, width, _ = trash_image.shape

        # Extract the alpha channel
        alpha_channel = trash_image[:, :, 3] / 255.0  # Normalize alpha to [0, 1]
        trash_rgb = trash_image[:, :, :3]  # RGB channels

        offset = np.array((int(trash_position[1]), int(trash_position[0])))  # Top-left point for insertion

        # Ensure the region of interest (ROI) is within the frame boundaries
        roi_height, roi_width = frame.shape[:2]
        if offset[0] + height > roi_height or offset[1] + width > roi_width:
            raise ValueError("The ROI exceeds the frame boundaries.")

        # Extract the region of interest from the frame
        blend_roi = frame[offset[0]:offset[0] + height, offset[1]:offset[1] + width]

        # Blend the images
        for c in range(3):  # Iterate over the RGB channels
            blend_roi[:, :, c] = alpha_channel * trash_rgb[:, :, c] + (1 - alpha_channel) * blend_roi[:, :, c]

        # Place the blended result back into the frame
        frame[offset[0]:offset[0] + height, offset[1]:offset[1] + width] = blend_roi
   

    else:
        cv2.putText(frame, "Lost", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    # Display the result
    cv2.imshow("preview", frame)
    
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
