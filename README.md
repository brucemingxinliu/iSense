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
    B[left_match.py] --> D
    
    classDef img fill:#f9f,stroke:#333,stroke-width:2px;
    
    D["<img src='https://github.com/brucemingxinliu/iSense/blob/master/leftres.JPG' width='100'/>"]
```  