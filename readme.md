# Setup

### Install python packges:
`pip install --user --upgrade numpy scipy matplotlib quandl`

### Install tensorflow

#### Pip install ([official docs](https://www.tensorflow.org/install/pip))

`pip install --user --upgrade tensorflow-gpu`

#### Docker install ([official docs](https://www.tensorflow.org/install/docker))

Prerequisite: [Install nvidia-docker](https://github.com/NVIDIA/nvidia-docker)

`docker pull tensorflow/tensorflow:latest-gpu-py3`

_NOTE: It is not recommended to run the train session without GPU support_