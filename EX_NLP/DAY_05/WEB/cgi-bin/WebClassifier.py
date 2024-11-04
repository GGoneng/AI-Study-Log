# 위에 라인 : 셀 내용을 파일로 생성/ 한번 생성후에는 마스킹

# 모듈 로딩--------------------------------------------
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
import MinModule
from MinModule import SentenceClassifier    
import HyeModule
from HyeModule import SentenceClassifier
import HunModule
from HunModule import SentenceClassifier
import WoongModule
from WoongModule import SentenceClassifier


# 동작관련 전역 변수----------------------------------
SCRIPT_MODE = True    # Jupyter Mode : False, WEB Mode : True
cgitb.enable()         # Web상에서 진행상태 메시지를 콘솔에서 확인할수 있도록 하는 기능

# 사용자 정의 함수-----------------------------------------------------------
# WEB에서 사용자에게 보여주고 입력받는 함수 ---------------------------------
# 함수명 : showHTML
# 재 료 : 사용자 입력 데이터, 판별 결과
# 결 과 : 사용자에게 보여질 HTML 코드

def showHTML(msg):
    print("Content-Type: text/html; charset=utf-8")
    print("""
        
        <!DOCTYPE html>
        <html lang="ko">
        <head>
        <meta charset="UTF-8">
        <title>이민하의 눈물</title>
        """+
        """
        <style>
            *{
                margin: 0;
                padding:0;
            }
            body {
                background-color: #f2f5f8; /* 부드러운 파란색 */
            }
            div.wrap{
                display: flex; 
                height:100vh;
                justify-content: center; 
                align-items: center;
            }
            div.wrap_inner{
                float:left;
                width:60%;
                max-width: 800px;
                margin:0 auto;
            }
            div.title{
                float:left;
                width:100%;
                text-align:center; 
                margin-bottom:30px;
                font-size:40px;
                font-weight:bold;
                color:#37474f; /* 진한 회색 */
            }
            div.imgbox{
                width:50%;
                float:left;
            }
            div.imgbox > img {width:100%;}
            div.animal{
                width:100%;
                float:left;
                padding:10px 0 10px 0;
                margin-top:30px;
                background-color:#78909c; /* 차분한 청회색 */
                border:solid #546e7a 4px; /* 진한 청회색 */
                color:#ffffff; /* 흰색 글자 */
                font-size:25px;
                font-weight:bold;
                text-align:center;
            }
            div.u-list{
                float:left;
                width:46%;
                padding:0 2% 0 2%;
            }
            ul {
                width:100%;
                float:left;
                list-style-type: none;
                padding: 0; 
            }
            li {
                width:100%;
                margin: 10px 0;
            }
            input[type="text"] {
                width: 90%;
                height : 120px; 
                padding: 11px; 
                border: 2px solid #b0bec5; /* 연한 청회색 */
                border-radius: 5px; 
                font-size: 16px; 
                transition: border-color 0.3s;
            }

            input[type="submit"]{
                width: 100%;
                height : 60px;
                border: 2px solid #ffab91; /* 연한 주황색 */
                border-radius: 5px;
                background-color: #ffccbc; /* 부드러운 주황색 */
                font-size:20px;
                font-weight:bold;
                color: #d84315; /* 짙은 주황색 */
                margin-top: 10px;
            }
            input[type="submit"]:hover{
                border-color: #bf360c; /* 더 진한 주황색 */
                color: #bf360c;
            }
        </style>
        </head>
        <body>
        <form>
        """)
    print(f"""
            <div class='wrap'>
                <div class='wrap_inner'>
                    <div class='title'> 초기 진단 모델 </div>
                    <div class='u-list'>
                        <ul>
                            <li><input type='text' name='word1' placeholder='한국어만 입력해주세요' value={words}></li>
                            <li><input type="submit" value="검사"></li>
                        </ul>
                    </div>
                    <div class='imgbox'><img src='https://img.hankyung.com/photo/201708/BD.14478006.1.jpg'/ id='image-preview'></div>
                    <div class='animal'>{msg}</div>

                </div>
            </div>
        </body>
        </form>
    """)



# 기능 구현 ------------------------------------------------
# (1) WEB 인코딩 설정

model_names = ['min_model', 'hye_model', 'hun_model', 'woong_model']
model_paths = []
model_file = []
if SCRIPT_MODE:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach()) #웹에서만 필요 : 표준출력을 utf-8로

# # (2) 모델 로딩
if SCRIPT_MODE:
    for mod in model_names:
        model_paths.append(os.path.dirname(__file__)+ '/models/'+mod+'.pth') # 웹상에서는 절대경로만
else:
    for mod in model_names:
        model_paths.append('./models/'+mod+'.pth') 
        

for pat in model_paths:
    model_file.append(torch.load(pat, weights_only=False,map_location=torch.device('cpu')))

# (3) WEB 사용자 입력 데이터 처리
# (3-1) HTML 코드에서 사용자 입력 받는 form 태크 영역 객체 가져오기
form = cgi.FieldStorage()

sick_list = ["순환/호흡기 질환", "소화기계/내분비계 질환", "임신/비뇨기 질환", "감염성 질환", "알 수 없음"]

if 'word1' not in form:
    msg = "<p>텍스트를 입력하지 않았습니다.</p>"
    words = ""

# (3-2) Form안에 textarea 태크 속 데이터 가져오기
else:
    msg = ""
    words = form.getvalue('word1', default = "")
    result = [] 
    if not ('' == words):
        res_show = True
        min_text = MinModule.min_preprocessing_text(words)
        hye_text = HyeModule.hye_preprocessing_text(words)
        hun_text = HunModule.hun_preprocessing_text(words)
        woong_text = WoongModule.woong_preprocessing_text(words)
        result.append(MinModule.min_predict_value(min_text, model_paths[0]))
        result.append(HyeModule.hye_predict_value(hye_text, model_paths[1]))
        result.append(HunModule.hun_predict_value(hun_text, model_paths[2]))
        result.append(WoongModule.woong_predict_value(woong_text, model_paths[3]))
        msg = result
    
        idx = []

        for i in range(len(result)):
            if result[i] == 1:
                idx.append(i)
            
            elif 1 not in result:
                idx = []
                idx.append(4)

        if len(idx) == 1:
            msg = f"<p>이 질환은 {sick_list[idx[0]]} 입니다.</p>"

        elif len(idx) == 2:
            msg = f"<p>이 질환은 {sick_list[idx[0]]} 또는 {sick_list[idx[1]]} 입니다.</p>"
        
        elif len(idx) == 3:
            msg = f"<p>이 질환은 {sick_list[idx[0]]} 또는 {sick_list[idx[1]]} 또는 {sick_list[idx[2]]} 입니다.</p>"
        
        elif len(idx) == 4:
            msg = f"<p>이 질환은 {sick_list[idx[0]]} 또는 {sick_list[idx[1]]} 또는 {sick_list[idx[2]]} 또는 {sick_list[idx[3]]} 입니다.</p>"

# # (4) 사용자에게 WEB 화면 제공

showHTML(msg)
