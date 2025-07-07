# 📌 Project Title

> **Fall Detection System**



<br><br>
## 📖 Overview

This project aims to detect potential solitary deaths of elderly people living alone by analyzing remote metering data (water and electricity).  
We first experimented with an LSTM model, but later adopted a GRU-based Autoencoder for better performance.  
The system includes a database and web interface, and I was responsible for designing the machine learning model.


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
