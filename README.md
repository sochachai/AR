## Introduction
This is an augmented reality application. 
The goal is to map/play a recorded video on the surface of an object(in this demo: the cover of the Ceylon Lemon Tea Drink) that appears in a live-stream camera </br>

## Running the program
Execute Video_Replace.py or run "python Video_Replace.py" in terminal. A person holding the physical copy of the "reference.jpg" will be on livestream camera. The source video "Video_Tam.mp4" will be displaying on the physical copy of the "reference.jpg". For the readers' particular use, a personalized "reference.jpg" and its hard copy should be used. There is some concern on how to select "reference.jpg" as described in the Methodology section. 

## Results
Two videos are placed in the "Result" directory.</br>
#### Single_View.mp4 shows the desired video: a live stream with the drink cover playing a recorded video </br>
#### Multiple_View.mp4 is a comprehensive view of the video processing. To illustrate this processing, the content of the six video/picture shown are described as follows.</br>
Row 1 Column 1: None-processed live streaming with a person holding the drink </br>
Row 1 Column 2: The resized version of the recorded video to be displayed on the cover of the drink </br>
Row 1 Column 3: The resized version of the static image of the cover of the drink </br>
Row 2 Column 1: Real-time feature mapping of the static drink cover image to the drink cover in live camera </br>
Row 2 Column 2: Recorded video broadcasting on the drink cover with a black screen background </br>
Row 2 Column 3: Processed live streaming with recorded video playing on the drink cover, i.e. the same content as Single_View.mp4 

## Methodology
### To build this app, it runs through three major steps as described below. </br>
Step 1. Choose a dicernable rectangular shape, in our case, the cover of the Ceylon Lemon Tea Drink. It will serve as the target surface. Make feature detection on the selected target surface. For the feature detection, Scale-Invariant Feature Transform (SIFT) is used. </br> 
Step 2. Test the target surface is significantly detectable in the sense that feature detection points have higher quantities in amount when target surface is on camera compared to the case when target surface is off the camera </br>
Step 3. Use Homography to find the boundary of the target surface </br>
Step 4. Map the recorded video to the polygon (usually a rectangle) enclosed by the boundary of the target surface

### Some details worth mentioning
1. If the target surface is not sufficiently discernable (check Step 2 in the above section for a more quantitative description), then it could happen that the target surface will mix with surrounding objects and the virtual screen, i.e. the polygon found by Step 3 is not stably rectangular. </br>
2. When the virtual screen is not stable or approximately rectangularly shaped, the recorded cannot be played smoothly, at least not on the targer surface. With the cover of the Ceylon Lemon Tea Drink being selected as the target surface, the recorded video can be played most of the time with occasional interruption. </br>
3. A more dicernable target surface should give a more stable streaming of the recorded video.</br>
4. Orb was used for feature detection and its performance in this program is much worse than SIFT. For the reason decribed in Point 1 in this section, orb cannot make dicernable detection and gives its way to SIFT. The code using Orb is stored in "Archive/Augmented_Reality" and is independent of a successful run of the program.
   
## Copyright Disclaimer
The recorded video named "Video_Tam.mp4" is recorded partially from the source "https://www.youtube.com/watch?v=S05JEZn5g8w". It is the music video of the song “难舍难分” by the artist Alan Tam. If there is any copyright issue, please contact the owner of this repository to remove the video.


