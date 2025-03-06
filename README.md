## Introduction
This is an augmented reality application. 
The goal is to map/play a recorded video on the surface of an object(in this demo: the cover of the Ceylon Lemon Tea Drink) that appears in a live-stream camera </br>

## Running the program
Execute Video_Replace.py or run "python Video_Replace.py" in terminal.

## Results
Two videos are placed in the "Result" directory.</br>
### Single_View.mp4 shows the desired video: a live stream with the drink cover playing a recorded video </br>
### Multiple_View.mp4 is a comprehensive view of the video processing. To illustrate this processing, the content of the six video/picture shown are described as follows.</br>
Row 1 Column 1: None-processed live streaming with a person holding the drink </br>
Row 1 Column 2: The resized version of the recorded video to be displayed on the cover of the drink </br>
Row 1 Column 3: The resized version of the static image of the cover of the drink </br>
Row 2 Column 1: Real-time feature mapping of the static drink cover image to the drink cover in live camera </br>
Row 2 Column 2: Recorded video broadcasting on the drink cover with a black screen background </br>
Row 2 Column 3: Processed live streaming with recorded video playing on the drink cover, i.e. the same content as Single_View.mp4 

## Methodology
### To build this app, it runs through three major steps as described below. </br>
Step 1.  Choose a dicernable retangular shape, in our case, the cover of the Ceylon Lemon Tea Drink. It will serve as the target surface. Make feature detection on the selected target surface. </br>
Step 2. Test the target surface is significantly detectable in the sense that feature detection points have higher quantities in amount when target surface is on camera compared to the case when target surface is off the camera </br>
Step 3. Use Homography to find the boundary of the target surface </br>
Step 4. Map the recorded video to the polygon (usually a rectangle) enclosed by the boundary of the target surface

## Copyright Disclaimer
The recorded video named "Video_Tam.mp4" is recorded partially from the source "https://www.youtube.com/watch?v=S05JEZn5g8w". It is the music video of the song “难舍难分” by the artist Alan Tam. If there is any copyright issue, please contact the owner of this repository to remove the video.


