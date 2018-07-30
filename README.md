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
* Python 3 (Recommend the Anaconda distribution w/ conda.  Get it [here]())

If you don't already have it, he Anaconda distribution with **conda** environment manager is highly recommended
Get it here [https://www.anaconda.com/download/](https://www.anaconda.com/download/)

### Setting up an environment
```
conda env create -f environment.yml 
pip install .
```

## Run the automations
### Copy and stitch
Copy directories from a **source** SD card to a media drive, stitch the **raw** files, and output a to a **stitched** directory. Define settings for the stitching with a **settings** YAML file

#### Mac OSX example
```
$ copy-and-stitch \
  --source=/Volumes/SD-Video2 \
  --raw=/Users/me/Projects/NewFilm/raw \
  --stitched=/Users/me/Projects/NewFilm/stitched \
  --settings=
```

#### Windows example
```
$ copy-and-stitch \
  --source=F:\test \
  --raw=C:\Users\ryan\Documents\VideoRaw \
  --stitched=C:\Users\ryan\Documents\VideoStitched \
  --settings=C:\Users\ryan\Projects\flugelhorn\settings\daily_mono.yaml
```
