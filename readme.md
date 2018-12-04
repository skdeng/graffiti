# Project DSI

[![Build Status](https://travis-ci.com/skdeng/dsi.svg?branch=master)](https://travis-ci.com/skdeng/dsi)

# Setup

### Install python packges:
`pip install --user -r requirements.txt`

### Install tensorflow

#### Pip install ([official docs](https://www.tensorflow.org/install/pip))

`pip install --user --upgrade tensorflow-gpu`

#### Docker install ([official docs](https://www.tensorflow.org/install/docker))

Prerequisite: [Install nvidia-docker](https://github.com/NVIDIA/nvidia-docker)

`docker pull tensorflow/tensorflow:latest-gpu-py3`

_NOTE: It is not recommended to run the training session without GPU support_

# How to run

### dsi_runner: 
`python dsi_runner.py -c <path to config file>`