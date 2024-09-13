# Euglena Trash Cleanup Game

This project is an interactive game where the player manipulates euglena cells (microscopic organisms) with light to simulate cleaning up trash from the sea. The game is controlled via a joystick, which adjusts the position of four LED lights to guide the euglena towards a virtual trash icon. The goal is to move the euglena across a vertical blue line, representing the sea boundary, to pick up and dispose of the trash (a plastic bottle). Once the trash is successfully moved out of the sea, the game displays a "You win!" message. If the euglena escapes tracking, a "Lost" message is displayed.

## Features
- Real-time tracking of euglena using computer vision.
- User control through LED lighting that directs the euglena's movement.
- Virtual blue line representing the sea boundary.
- Trash pickup and drop mechanics.
- Visual feedback for winning or losing the game.

## Requirements
- Python 3.x
- A phone camera to stream video to the computer (via a generated QR code).
- Four LED lights and joystick control for manipulating the euglena's movement.

## Dependencies
- `opencv-python` (for OpenCV functionality)
- `opencv_browser_camera` (to stream phone camera feed to your PC)
- `numpy` (for array and numerical operations)

## How to Play
1. **Setup the camera**: 
   - Use a phone camera to observe the euglena under a microscope. The camera feed is streamed to the computer using the `opencv_browser_camera` module.
   - A QR code is generated for connecting the phone camera stream.

2. **Initialize the game**: 
   - The first frame of the camera feed is cropped to the desired region, and the user selects an euglena from the frame to track.

3. **Move the euglena**: 
   - Control the euglena's movement with a joystick that manipulates LED lights on the microscope slide.
   - Guide the euglena to the virtual trash icon on the left side of the vertical blue line (the "sea").

4. **Win condition**:
   - Once the euglena passes over the trash, the icon attaches to the euglena and follows its movements.
   - Lead the euglena (with the attached trash) across the vertical blue line to the right side of the frame to drop the trash and display the "You win!" message.

5. **Lose condition**:
   - If the tracker loses sight of the euglena, the game displays a "Lost" message.

## Code Explanation

- **Frame Cropping**: The camera feed is cropped using predefined dimensions for a closer view of the euglena and the virtual game field.
- **Vertical Blue Line**: A blue line is drawn one-third of the way across the screen to separate the "sea" from the "land".
- **CSRT Tracker**: OpenCV's CSRT tracker is used to follow the selected euglena throughout the game.
- **Trash Icon**: The trash icon, represented by a plastic bottle image, is initially placed on the left side of the screen (the sea). When the euglena crosses its position, the icon attaches to the euglena and follows it.
- **Win Condition**: The player wins if the euglena successfully moves the trash from the sea (left) to the land (right), crossing the vertical blue line.
- **Loss Condition**: If the tracking fails, a "Lost" message is displayed.

## Usage Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/euglena-trash-cleanup.git
   cd euglena-trash-cleanup
