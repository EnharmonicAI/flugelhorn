# Flugelhorn - Simple VR / 360 Video Stitching Automations

### What is Flugelhorn?
Flugelhorn is a convenience package to automate VR/360 Video stitching.
It was built initially to automate the workflow around videos and images captured by the insta360 Pro camera.

### Why the funny name?
No idea, it seemed like a good idea at the time.

## Install and setup
This automations package is built around insta360 Pro stitching workflows, so it goes withotu saying that insta360 software is required for this to work.

### Dependencies
* insta360Stitcher
* Python 3

### Setting up an environment
```
conda env create -f environment.yml 
pip install .
```



## Settings Documentation
### input
Basic information about the input source

#### Properties
##### type
* image
* video

##### lensCount
Number of images to stitch together.  6 for the Insta360 Pro

##### fileCount
Defaults to 1. Not positive what this does

#### Sub Elements
### imageGroup
The imageGroup tag defines the group of images that will be stitched together.
If the input type is 'video', this tag is replaced with the *videoGroup* tag

A file tag containing a single *src* attribute will be added for each file in the image group to be stitched.

### videoGroup
The videoGroup tag defines the group of videos that will be stitched together.
If the input type is 'image', this tag is replaced with the *imageGroup* tag

A file tag containing a single *src* attribute will be added for each file in the video group to be stitched.

A trim tag containing the start and end attributes with the time for the given video is added.
End time can be read from mp4 metadata?


### blend
General settings for the stitching process.

How the XML attributes correspond to GUI settings
GUI:
*Stitching Mode*
New Optical Flow:
    * useOpticalFlow: 1
    * useNewOpticalFlow: 1
    * useTopFixer: 0
Optical Flow:
    * useOpticalFlow: 1
    * useNewOpticalFlow: 0
    * useTopFixer: 0
Scene-Specific Template:
    * useOpticalFlow: 0
    * useNewOpticalFlow: 0
    * useTopFixer: 0

Checkboxes:
Use Default Circle Position
corresponds to blend.calibration:useDefaultCircle

Gyroscopic Stabilization
corresponds to gyro tag, enable: 1/0 attribute

Use Hardware Decoding and Encoding correspond to the preference.encode and preference.decode tags

Software encoding speed:
GUI: XML
fastest: preset: superfast
fast: preset = veryfast
medium: preset = faster
High Quality (slow) = fast
Highest Quality (slowest) = preset=medium

Encoding profile
See h.264 docs for more info
* baseline
* main
* high


### Stitching Settings
#### Sampling Type
Corresponds to blend.samplingLevel tag
* Fast (fast)
* Medium (medium)
* Slow (slow)

#### Content Type
Controlled with blend.mode
##### Monoscopic
Controlled with blend.mode = 'pano'

##### Stereo (Left Eye on Top)
Controlled with blend.mode = 'stereo_top_left'

##### Stereo (Right Eye on Top)
'stereo_top_right'


##### Stereo 
Used for image (non-video) stitching only
'stereo_separate'

Reference Frame settings
##### Zenith Optimization
Corresponds to blend.useTopFixer 

Either the calibration tag can be used to specify a captureTime of a frame for use in stitching calibration, or a specific offset can be generated and used for input.

This offset setting includes a 
```xml
<offset>
    <pano>values</pano>
    <stereoLeft>values</stereoLeft>
    <stereoRight>values</stereoRight>   
```

This also affects the gyro angle adjusts (pan, tilt, roll).  The default for these values is 0.  The default for distance appears to be 603.3333333333334



### Output
Image/Video
There are two main choices regarding output
Resolution

Standard Resolution
8K 7680x3840
6K 6400x3200
5K 5120x2560
4K 3840x1920
2.5K 2560x1280

Custom Resolutions are also allowed


Format
#### MP4





#### PNG
This outputs a sequence of PNG files to an output folder
output.type = 'sequence'
```xml
<output type="sequence">
    <sequence format="png" />
</output>/
```

#### JPEG
This outputs a sequence of PNG files to an output folder
output.type = 'sequence'
```xml
<output type="sequence">
    <sequence format="jpg" />
</output>/
```

### Audio Output







    'blend': {
        'useOpticalFlow': PropertyDef([True, False], True),
        'useNewOpticalFlow': PropertyDef([True, False], True),
        'mode': PropertyDef(['pano'], None),
        'samplingLevel': PropertyDef(['slow', 'medium', 'fast'], 'fast'),
        
        'useTopFixer': PropertyDef([True, False], False)
    },
    'blend_calibration': {
        'lensVersion': PropertyDef(None, 7),
        'lensType': PropertyDef(None, 12),
        'captureTime': PropertyDef(None, None),
        'captureTimeIndex': PropertyDef(None, None),
        'useDefaultCircle': PropertyDef([True, False], True),
        'useDefaultOffset': PropertyDef([True, False], True)
    },
    'encode': {
        'useHardware': PropertyDef([True, False], False),
        'threads': PropertyDef(None, 1),
        'preset': PropertyDef(['superfast'], 'superfast'),
        'profile': PropertyDef(['baseline', 'main', 'high'], 'baseline')
    },
    'decode': {
        'useHardware': PropertyDef([True, False], False),
        'threads': PropertyDef(None, 1),
        'count': PropertyDef(None, 1)
    },
    'blender': {
        'type': PropertyDef(['auto', 'cuda', 'opencl', 'cpu'], 'auto')
    },
    'gyro': {
        'version': PropertyDef([1, 2, 3], 2),
        'type': PropertyDef(['pro'], 'pro'),
        'enable': PropertyDef([True, False], True),
        'filter': PropertyDef(['akf'], 'akf')
    },
    'gyro_calibration': {
        'gravity_x': PropertyDef(None, None),
        'gravity_y': PropertyDef(None, None),
        'gravity_z': PropertyDef(None, None)
    },
    'gyro_angle': {
        'diff_pan': PropertyDef(None, None),
        'diff_tilt': PropertyDef(None, None),
        'diff_roll': PropertyDef(None, None),
        'distance': PropertyDef(None, None)
    },
    'color': {
        'brightness': PropertyDef(None, None),
        'contrast': PropertyDef(None, None),
        'highlight': PropertyDef(None, None),
        'shadow': PropertyDef(None, None),
        'saturation': PropertyDef(None, None),
        'tempture': PropertyDef(None, None),
        'tint': PropertyDef(None, None),
        'sharpness': PropertyDef(None, None)
    },
    'depthMap': {
        'enable': PropertyDef([True, False], False),
        'path': PropertyDef(None, ''),
        'inverse': PropertyDef([True, False], True)
    },
    'output': {
        'width': PropertyDef([6400, 5120, 3840, 2560], 3840),
        'height': PropertyDef([1280, 1920, 2560, 3200], 1920),
        'dst': PropertyDef(None, None),
        'type': PropertyDef(['video'], 'video')
    },
    'video': {
        'fps': PropertyDef([1, 5, 23.98, 24, 25, 29.97, 30, 60], 29.97),
        'codec': PropertyDef(['h264', 'h265'], 'h264'),
        # TODO(ryan): This should be calculated?
        'bitrate': PropertyDef(None, 62914560),
        'useInterpolation': PropertyDef([True, False], False) 
    },
    'audio': {
        'type': PropertyDef(['pano'], 'pano'),
        'device': PropertyDef(['insta360'], 'insta360')
    }
}
