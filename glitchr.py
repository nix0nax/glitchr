import cv2
from pedalboard import Pedalboard, Chorus, Reverb, Bitcrush, Distortion, LadderFilter, LowpassFilter, load_plugin, HighpassFilter, Phaser, PitchShift
from pedalboard.io import AudioFile
import numpy as np
from scipy.io.wavfile import write
from pynput.mouse import Controller
from sklearn.preprocessing import minmax_scale

rate = 44100

videoname = "test.mp4"

# Open the default camera
cam = cv2.VideoCapture(0)

# Load the video file
video = cv2.VideoCapture(videoname)

# Get the default frame width and height
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fileout = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

# Make a Pedalboard object, containing multiple audio plugins:
board = Pedalboard([Reverb(), LowpassFilter()])

mouse = Controller()

# Check if the video file was successfully loaded
if not video.isOpened():
    print("Error: Could not open video file")
    exit()
    
    


# Loop through the frames of the video or cam
while True:
    # Read the next frame
    # comment/uncomment here to change cam or video input
    ret, frame = video.read() 
    #ret, frame = cam.read()
    
    normousex = mouse.position[0] / 1920
    normousey = mouse.position[1] / 1080
    board[0].room_size = normousex
    board[1].cutoff_frequency_hz = mouse.position[1] * 10
    board[0].wet_level = normousey
    
    # Check for the 'q' key to quit the video playback
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    
    # Check if the frame was successfully read
    if not ret:
        video = cv2.VideoCapture(videoname)
        continue
    
    res = frame.shape
    
    flattened = frame.flatten().astype(np.float32)
    #flatscaled = minmax_scale(flattened, (-1, 1))
    
    effected = board(flattened, rate)
    #effectedscaled = minmax_scale(effected, (0, 255))
    
    unflattened = effected.reshape(res).astype(np.uint8)
    #write('test.wav', rate, frame)
    # Display the frame in a window
    cv2.imshow('Video', unflattened)
    
    fileout.write(unflattened)
    
    
    


# Release the video object and close the window
video.release()
fileout.release()
cv2.destroyAllWindows()
