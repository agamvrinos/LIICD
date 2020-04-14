[![Build Status](https://travis-ci.com/agamvrinos/CloneDetector.svg?token=xNKvEzh6d3zxdYfRyEWC&branch=master)](https://travis-ci.com/agamvrinos/CloneDetector)
[![BCH compliance](https://bettercodehub.com/edge/badge/agamvrinos/CloneDetector?branch=master)](https://bettercodehub.com/)

# CloneDetector

Two Python implementations of an Incremental Clone Detector. 

1. The **Original** one implements Hummel's clone-index based approach
2. The **LSH-based** utilizes Locality Sensitive Hashing (LSH) to calculate the clones for similar files, avoiding thus the calculation of large intermediate data representations.

## Install

For both sub-projects:

Install dependencies via `pip install requirements.txt`

## Run

Both implementations can simply be run via the main script `main.py`
