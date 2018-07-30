# Flugelhorn - Simple VR / 360 Video Stitching Automations

### What is Flugelhorn?
Flugelhorn is a convenience package to automate VR/360 Video stitching.
It was built initially to automate the workflow around videos and images captured by the insta360 Pro camera.

### Why the funny name?
No idea, it seemed like a good idea at the time.

## Install and setup
This automations package is built around insta360 Pro stitching workflows, so it goes withotu saying that insta360 software is required for this to work.

### Dependencies
* insta360Stitcher software
* Python 3

If you don't already have it, he Anaconda distribution with **conda** environment manager is highly recommended
Get it [here](https://www.anaconda.com/download/).

### Setting up an environment
```
conda create -f environment.yml
pip install .
```

## Run the automations
### Copy and stitch
Copy directories from a **source** SD card to a media drive, stitch the **raw** files, and output a single video file (.mp4) to a **stitched** directory. Define settings for the stitching with a **settings** YAML file

#### Mac OSX example

```
copy-and-stitch \
  --source=/Users/ryan/Projects/test_videos/new_source \
  --raw=/Users/ryan/Projects/test_videos/raw \
  --stitched=/Users/ryan/Projects/test_videos/stitched \
  --settings=/Users/ryan/Projects/flugelhorn/settings/daily_mono.yaml
```


#### Windows example
From bash (Git bash or cygwin)
```
copy-and-stitch \
  --source=/f/test \
  --raw=/c/Users/ryan/Documents/VideoRaw \
  --stitched=/c/Users/ryan/Documents/VideoStitched \
  --settings=/c/Users/ryan/Projects/flugelhorn/settings/daily_mono.yaml
```


### Stitch
Stitch **raw** files and output a single video file (.mp4) to a **stitched** directory. Define settings for the stitching with a **settings** YAML fill. This automation skips any file copying, and will stitch the raw files from their current location.

#### Mac OSX example
```
stitch \
  --raw=/Users/ryan/Projects/test_videos/raw \
  --stitched=/Users/ryan/Projects/test_videos/stitched \
  --settings=/Users/ryan/Projects/flugelhorn/settings/daily_mono.yaml
```

#### Windows example
From bash (Git bash or cygwin)
```
stitch \
  --source=/f/test \
  --raw=/c/Users/ryan/Documents/VideoRaw \
  --stitched=/c/Users/ryan/Documents/VideoStitched \
  --settings=/c/Users/ryan/Projects/flugelhorn/settings/daily_mono.yaml
```
