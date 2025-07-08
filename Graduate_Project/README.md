# 📌 Project Title

> ### **Fall Detection System**



<br><br>
## 📖 Overview

This system is designed to rapidly detect falls, especially among the elderly population, and immediately notify caregivers to enable prompt response and intervention.  
Unlike typical vision-based approaches, it detects falls **without any wearable sensors**, using only a camera module.
The system extracts skeleton keypoints and treats them as time-series data—similar to gyroscope readings—enabling fall detection through temporal analysis rather than standard image classification.  
A functional prototype was also implemented and deployed on a Raspberry Pi for real-world demonstration.


<br><br>
## 🛠️ Tech Stack

| Category        | Tools / Frameworks                |
|----------------|-----------------------------------|
| OS              | Windows 11 HOME                  |
| Language        | Python 3.x, HTML5, CSS3, JavaScript(ES6) |
| Libraries       | torch, sklearn, matplotlib, flask     |
| Environment     | Jupyter Notebook / VSCode / DBeaver   |
| RDBMS           | MariaDB                               |
| Hardware        | GPU                                   |


<br><br>
## 📂 Project Structure

```bash
.
├── GRU_AutoEncoder_model/     # Final model using GRU-based AutoEncoder
│   ├── GRUAutoEncoderModule.py     # Module containing functions for training
│   └── GRU_AutoEncoder.ipynb       # Notebook for training and evaluation              
├── LSTM_Model/                # Initial LSTM-based model
│   ├── Data_Preprocesssing.ipynb   # Data Preprocessing
│   ├── Graph.ipynb                 # Visualization of Data Pattern
│   ├── LSTM_model.ipynb            # Notebook for training and evaluation 
│   └── [...]                
├── MyWEB/                     # Web interface
│   ├── models/                     # Pretrained models
│   ├── static/                     # Static files
│   ├── templates/                  # HTML templates for Flask rendering
│   └── __init__.py                 # Flask app initialization
└── [...]               
```

<br><br>
## 💡Install Dependency

```bash
pip install -r requirements.txt
```
