# High level Design Documentation and System Overview 

## Introduction
This project is for iSense vision software V1.0. \
Licensed under keySense LLC 祁新科技有限公司 \
Author Bruce Liu\
Date: 2024/12/06
## Requirements
OpenCV libraries 
Numpy

## System Overview
```mermaid
graph TD;
    A[GUI.py] --> B[left_match.py]
    A[GUI.py] --> C[right_match.py]
<<<<<<< HEAD

```  

From each left and right match exe, a confidence score will be generated\
Each score should be 0 to 1 and if the combined score is larger than 0.8, then the part is PASS, else is NG

## Connection and Integration
The current deployment is for TCP camera, so the run time is for RJ45 connection
=======
    B[left_match.py] --> D[![leftres](https://github.com/user-attachments/assets/ce582da9-00bb-4e56-8ba0-8e3ff326eb52)]

```  
>>>>>>> 1e880eecca98d6d8c2108ee9ab70f82e6a1fdf8b
