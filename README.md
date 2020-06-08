[![Build Status](https://travis-ci.com/agamvrinos/CloneDetector.svg?token=xNKvEzh6d3zxdYfRyEWC&branch=master)](https://travis-ci.com/agamvrinos/CloneDetector)
[![BCH compliance](https://bettercodehub.com/edge/badge/agamvrinos/CloneDetector?branch=master)](https://bettercodehub.com/)

# CloneDetector

Two Python implementations of an Incremental Clone Detector. 

1. The **Original** one implements Hummel's clone-index based approach (skipping the normalization step)
2. The **LSH-based** utilizes Locality Sensitive Hashing (LSH) to calculate the clones for files that were found to be similar.

## Install

For both sub-projects:

Install dependencies via `pip install requirements.txt`

## Run

Both implementations can simply be run via the main script `main.py`

### Arguments 

`-p`: The path to the software project to be analyzed

`-u`: The path to the configuration file that holds the commits to be analyzed