import os.path     # 파일 및 폴더 관련
import cgi, cgitb  # cgi 프로그래밍 관련
import joblib      # AI 모델 관련
import sys, codecs # 인코딩 관련
from pydoc import html # html 코드 관련 : html을 객체로 처리?
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import sys, os
from PIL import Image
from cv_module import *
import io


SCRIPT_MODE = True

cgitb.enable()

def showHTML(msg):
    print("Content-Type: text/html; charset=utf-8")

    print(f"""
        
        <!DOCTYPE html>
        <html lang="ko">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>웹은 어려웡</title>
        """+
        """
        <style>

            body {
                background-color:rgb(246, 251, 255)
            }

            header {
                height:20vh;
                padding-top:3vh;
                font-size : 25px;
                font-weight: bold;
                background-color:rgba(190, 224, 254, 0.575);
                text-align: center;
                border: 1px solid rgb(191, 194, 197);
            }

            nav {
                display:flex;
                padding-left:8vh;
                justify-content:space-between;
                height:5vh;
                width:90vw;
            }

            nav div {
                flex-grow:1;
                display:flex;
                padding: 10px;
                background-color:rgba(190, 224, 254, 0.575);
                justify-content: center;
                align-items: center;
                border: 1px solid rgb(191, 194, 197);
                width: 40vw;
                text-align: center;
           
            }
            
            a {
                color: rgb(46, 36, 36, 0.6);
                font-size: 15px;
                text-decoration: none;
                font-weight: bold;
            }

            a:visited {
                color : rgba(46, 36, 36, 0.6)
            }

            a:hover {
                color: rgba(46, 36, 36, 0.6)
            }

            a:active {
                color: rgba(46, 36, 36, 0.317)
            }

            section {
                display: flex;
                padding-top:8vh;
                padding-left: 8vh;
                justify-content:space-between;
                width: 90vw;
            }

            section div {
                flex-grow: 1;
                padding: 10px;
                justify-content: center;
                align-items: center;
                border: 1px solid rgb(191, 194, 197);
                width: 40vw;
                text-align: center;
            }

            ul {
                font-size: 20px;
                margin-right: 30px;
                text-align: center;
                list-style-type: none;
            }

            li {
                padding-top: 20px;
                padding-bottom: 20px;
            }

            form {
                margin-top: 30px;
                width: 40vw;
                margin-left: 30vw;
                padding-bottom: 20px;
                border: 1px solid rgb(191, 194, 197);
                justify-content: center;
                align-items: center;
                text-align: center;
            }

            .form_inner {
                display: flex;
                justify-content: center;
                align-items: center;
            }

            input[type="file"] {
                height:30vh;
                width:20vw;
                padding:10px;
            }

            input[type="submit"] {
                width:20vw;
                height:30px;
                background-color: rgb(236, 232, 255, 0.6);
                font-weight: bold;
            }

            #result {
                display:flex;
                width:50vw;
                height:10vh;
                margin-top: 50px;
                margin-left: 25vw;
                background-color: rgba(190, 224, 254, 0.575);
                justify-content: center;
                align-items: center;
                border: 1px solid rgb(191, 194, 197);
                font-size: 25px;
            }

        </style>
    </head>
        <body>
        <header>
            <h1>아마존 리뷰 감정 분석 모델</h1>
        </header>
        <form enctype="multipart/form-data" method="post">
            <div class='form_inner'>
    """)
    print(f"""

                <ul>
                    <li><input type='file' name='image' 
                        accept='image/*' onchange='previewImage(event)'
                        required></li>
                </ul>
            </div>
            <div id=submit><input type='submit' value='제출'></div>
        </form>
        <div id='result'>{image}</div>     
""")
print("""
         <script>
            function previewImage(event) {
                const preview = document.getElementById('image-preview');
                const file = event.target.files[0];

                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                    }
                    reader.readAsDataURL(file);
                }
            }
        </script>
        </body>
        </html>
    """)
    
model_names = ['min_model_cv.pth']
model_paths = []


if SCRIPT_MODE:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

if SCRIPT_MODE:
    for mod in model_names:
        model_paths.append(os.path.dirname(__file__)+ '/models/'+mod) # 웹상에서는 절대경로만
else:
    for mod in model_names:
        model_paths.append('./models/'+mod) 

form = cgi.FieldStorage()

if 'image' not in form:
    msg = "<p>파일을 선택하지 않았습니다.</p>"
    words = ''

else:
    file_field = form['image']
    msg = ''
    image = Image.open(io.BytesIO(file_field)

    result = []

    if file_field.filename:
        preprocessed_image = min_preprocessing_img(image)
        result = min_predict_value(preprocessed_image, model_paths[0])

        if result:
            msg = f"<p>이 동물은 표범 입니다.</p>"
        
        else:
            msg = f"<p>이 동물은 표범이 아닙니다.</p>"

    else:
        msg = "<p>올바른 파일을 업로드하세요.<p>"

showHTML(msg)