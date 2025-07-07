# 📌 Project Title

> **Remote Metering Data-Based Monitoring System**



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
├── data/                   # Dataset or data pipeline scripts
├── models/                 # Model architecture and training scripts
├── scripts/                # Training / evaluation / inference scripts
├── utils/                  # Utility functions
├── results/                # Outputs like graphs, logs, videos
├── MyWEB/ (opt)            # Frontend or demo web interface
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
