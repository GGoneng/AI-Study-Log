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
from MinModule import * 


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
        <title>왜이리 어려움?</title>
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
            input[type="file"] {
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
        <form enctype="multipart/form-data" method="post">
        """)
    print(f"""
            <div class='wrap'>
                <div class='wrap_inner'>
                    <div class='title'> 동물 판별 모델 </div>
                    <div class='u-list'>
                        <ul>
                            <li><input type='file' name='word1' accept='image/*' onchange='previewImage(event)' required></li>
                            <li><input type="submit" value="검사"></li>
                        </ul>
                    </div>
                    <div class='imgbox'><img src='data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMVFhUXFxcaFxgXGBYXGBodGBgbGxgaHRgdHSggGBolGxcYITEiJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGhAQGyslHR0tLS0tLS0tLS0tLS0tLS0tLSstLS0tLS0tLS0uLS0tLSstLSstKy0tLS0tLS0tLS0tLf/AABEIAKgBLAMBIgACEQEDEQH/xAAcAAABBAMBAAAAAAAAAAAAAAAFAAQGBwIDCAH/xABNEAABAwIEAwQECwYCCAUFAAABAgMRAAQFEiExBkFREyJhcQcygZEUF1JUk6Gxs9HS8CM1QnTB4RVyJTNkc4KSsvEkNGJj0xZDU6LC/8QAGAEBAAMBAAAAAAAAAAAAAAAAAAECAwT/xAAgEQEBAAIDAQEBAQEBAAAAAAAAAQIREiExA1FBE/Bh/9oADAMBAAIRAxEAPwCjaVKlQKlSpUCpV7FeUCpUqVAqVKlQKlSpUCpVkEzW5Foo8qBvSp6iwVTyzsUkgE77VW5RMlCQ2TyrMWqzyqUpw1CNSR7a2s2qFEwdo1jrVea0wRE2q/k0vgyulTD4OjWO9HTX9bVoKEkwND5VH+ieCLi0X0pC0X0qXotElIO3X+1Y3aW0AEyfEa0/0OCIm2V0rBTZFSwhszk15+VM12madEgg1M+hwR0ppRR/4CnMQdOnQ1qfwvof1+hVucV40FCTXpQaOWTLYIBBKj4U9u7JJEBOs9NqjkjR5h/ooxR5pt5thJQ4hK0HtWhKVpCkmCqRoRTj4nMX+bp+mZ/NXRHAo/0bY/ylt9yijlXQ5b+JzF/m6fpmfzUvicxf5un6Zn81dKWmN27rzlu26lTrUZ0DcT9RjYxtImKIUHLfxOYv83T9Mz+al8TmL/N0/TM/mrqSlQct/E5i/wA3T9Mz+al8TmL/ADdP0zP5q6kpUHLfxOYv83T9Mz+al8TmL/N0/TM/mrqSlQcPBNGsJ4Yff1CCE9TpPLSpnwZ6O1OJDz2iTr7PCpngy2BmQnvrTIIAnKATA6SRrWWf0142w+XL1WaPR87GZRyjx/sN6fWfo1JSVOOpQBr3jy67VP7ZCnVLgLCNRqCDy92orJ5+2RmbdVECIOnSs/8AWtv8YgnxdtGA2+lZ6AiY2mOk6UBxPgd5qTGgO5/tVgYZw121wp/MENpTlaA3JO/kP60Wfs3UZkLVmSo7GCIEaeWh3pfplD/LG9KJfw1xOpSY600ir7Xw6gxEazUT4k4LQUkpUAqTlMQDHU8qvj9pfWWfxuPir69qUWPBNw4JyECdzCR9Zk+YFSfC+BWRAWCtXOTlT+J9lXv0kZ/51WFIVZfF3CNqlkqYOVxAkpHqkc96rSrS78VuOj7DreTPIb1IrW10zEeyg+FOQI99GWWiowDA571nnV8Y1OoBkjSdpr21tCSCqdNfxou3hoMFRk1vUgJBAqm1+gJ9xLjkDly99OAkpVJ8KxtQkKUeZM05aXm2qtWjBxfd07o5nrQztB2mWdI5UWUyNgKGFn9pB5D+tJU2Can4y8hqCPsppdpGbTl/3pyP+9a3nwN+dNmjWzfGcojfWt99ZfxJnlt4U1CMzySKkR1EdKlVGHAZ72uojwrayowRMyTHh+taN3rSMusChCkpVok9YH9aDZZBI1gTtTq5dCRPtoZmIHlt+NDcSxAnSrYy2q26dX8C/u2x/lLb7lFa+OlXYs3DZx2gBzb58gBzdn/7nT2xrFbOBP3bY/ylt9yiolxR6Tl2ty7bi1B7MgZlOkTKQoHKEaCCOdbsVT4ViTjDqH2lQtJkHcHqD1SRoRzmuiOE+IW723S8jQ7OI5oUNx5cweYIrnLinF+0dU+2wltKzKkJUSkKO5GggHp1nrW3gnji4s387bedCtHEZiEqHIzBhQ3BjqOdB1DSqE8K+khi7dSwW1tOKnLJSpBIBJSFCDMA7gTU2oBvEt6ti0uHkRnbZcWnMJEpQSJEiRIqnx6VcQ/2f6NX56ujFbMPMutHZxtaD/xJI/rXL7jZSSlQhQJBHQjQ/XQdUIOg8qyoTwniHwizt3juptOb/MBCv/2BotQUg/iT6VK7wbtG0ZlqyKUUgaHKARB100oc5xPhiQpth1aQrdRCiTrJJJGpJP1CjamiMLW24oBbyVpJ00SdP6VSeGYcXXwwFJSSopzK0SI3NZzDc7af6WXpdvDmN2Ti27e3W68pclRKnO6ExJOsJG1N/SRhThCJKTbZh2h7LO6iOi/Wg7TGk1KeCeHGbK3DbZCidVrMSon7B4U/xaQk/JIIImN/Heo4SeJn0tvauLO3dKB8DWtCY7oXleB6gKMR1hQPnT3/AAG5cCT26y4nUZzorqnKCAJ+qmWAYoi2uHGHVj1jk0I7u4E7K93topjGIOoUHWAl0TtmE+e0SOmm9Z2VrjnJ4WHY2FktKBC0EAg6KmPHeiV7kWgIUAQrTyjx61X/ABbiS1/tQAh1kiQN+9yM7g/UaNcN8RtvNgKbVnk5kjcdTAmapwaT6Ixjj7zDhbVcKgHQkmY8aZPY856jRUs/LKyQPKraxDhuzxAZlNkEp0gqQfGddxUAZ4CWi8LCZyb5jIhME+R1EVeSSMcsrsFRiGRlxTh75SQPb9tQypvxhwo62cwIUOSRqY8utAGOF7xfq2zpG85THv5VtjZIyylZ4WzIHWjXQA7bmnuBcKvkaBBVBiViNOU9adq4WuWkkuI31JQcwk1jc8b5Wklk7BxiqmzChI661sVjbUaqovY8M3bn/wBleSJzOQlMDnrr7hTV8soOUrYcPRCgrXoZjWpxsqtA0vtuuQg976o5zRNlASn8BQXGmgXkBIyExO39KkjSYGpOgHKpzn4nGhqngVaEg+NN1IXnkkARE9fZW/ELfvJUkTrr5V5iLZiU8qpprts7Rv1ZUTWt5kSJVp4iDWzDLYIEq9Y7+FOb20C0lO+m45VMiLQQ4ihlZSNec06bxuBohUdQk0PwQhtxXaJlXKRvG9ST4TIgN6eytOoyBXbx10wEwnyg1sXaEAHL3hrpRVKSToAPM6+6vCg7mD56VRPkC8wcTp9dRy/ZIUalTlrkWVgwFbjl/amV1YFQPXkdqtjdVGU3HT3An7tsf5S2+5RUV489H717dh5pbaEltKV5805kkwQADPdIG/KpVwJ+7bH+UtvuUUcrZkplXofuSIL7BB8F/hUT4z4UXYZGu2aU4oTlQFDKnqZEakQPI1b/ABzx41ZpLbRS5c7ZZlKPFcf9Mgnwqh8dx9bj5cfUVrXqpXTkBHIADYdKB9wlZPu3LCEH9qXEkKT/AA5TmKv+ECfZXTtV56IeHW22BeEpU68IEEHIifV8FEgEjlAHI1YdAq5s4wbCb66Cdu3c+tRJ+smuk65t4z/8/d/79z/qNBcHokUThjU8lugfSKqZVDPRF+7G/wDO794qpnQcsurcvkMNpdKRlVmGu6QSJ9gio0cKCXg2XkJ1HeJIidenQ0Q4JxDI7lneY/XtodxAw426W3FZykDKo7kHbWqze09JBgarxtl+4ZvCAysognMFgRqJkQaOW3HuJpTldYQ8k/8ACSPAg7eyq9t8SWhl1geo6UE+aDpHnt7K1JvHUlJC1AoEJ19UdB76moSbiHH0rVna7ZlwHVteqDyMEGI8wPOjXDF4HiIWUyO9rMnaCCNuY8arhbhO5JqR8FpKlqAnQSefh/X66pnOmmF1U0SVIKy9kkiMw2KQZEg8qDqeUp9K205VCYcbOhHRVHXMMdWIyLUkgggJJG3lQ5nAiycgZebKiIJBA16K5f3rHlI17/g1g3FjifXcKoIACQJT5jc1Ln8W7VJLSIUQElxYKQDygHU/ZQSzwtu1QYSO0VuqASVGIV7AaeXrjzbJLaQ65CQkaTJ5qP11z5fe+YtZ8/7Q+zYQl4IUS676ytTG/Tp5VIFWuIKV3HkNpGyUoSfYSsGaZ4NhD9uC6otruHCkLVogAEHupO58qfW7ypBUkpcTqpsEnKD6pVrEmNqjHGz2pzynkMMXwN3sypWVDmpzJUgAGDqU5cp99COCbp5Ti+2cC1iEjXKBHMITA9utZcccVKDJaRo4vug/JB0KvCKgdnxKq2QWbMqddMl19Ukf8InQeJro+fzlxZZZ3el6YulhbQF8lgpHNcn3azt41T/EOG4HKixcLbUJ0hS0HynUew0Lcwu4Uj4Zel5xsamSSkk7J1O3lR/iY2Fsxa31gzbvNOKUhxt1IVCwmYI3TvMeAroxnFhl2b4NhGe3LrRCwhR7TmtEnQkb5T1FC+IrlTQSoDQmD7qk/BVr262b5hptpTThTcNtmErac0Pd+SJnWaZY1Zoc7RCYyyrLttJioutnc6Qn/GDvzpOYuvkfqE0Kv7UtLKFAgjr9vjTYqq+orcqLf4odt6k/D+dTeZYiT7xG8cqjHDmGF5zUd1OpJ28qniSlAjeqZ6Wlpg/ZIXooQAZ9vXwoW26pCylRhM6EkSfLmaLPvxy9lBb2cwUUTJ93siTVZ2sOtr0/QrBZG6d/fTNm7SRzSfEEfbSdWpOoM9AaaI9eCylUrBG/TQeVDGHAQBIMmdDTy4dhJUOcSmBoZ8KFobSNQIBk6E7/ANKbS6k4G/dtj/KW/wByim/pBxK4t7Jx22SCoaKVzbSQZcCYhRGm+g31inHAn7tsf5S2+5RRtaQQQQCCIIOoIPKtmLlq2YW6tKEJUtxaoAEqUon7TuST4k0Rx7gG6tIeuGwpKoOZBzpb/wDSvofHboau/hngi1snFutglaicpVr2aSfUT9knWpKtIIIIBB0IOoM0HNXD2Pv2TocZWRtnQZyLHRSefgdxyNXZwhxzb30I/wBW/BlpR3jUlCv4xGvXTaoxxj6LgrM7YwlW5YJASeuRR0T/AJTp4iivov4PNq327yYuHBAB3bR8nwUYBPsHI0E8rm3jP/z93/v3P+o10lXOfHrWXEbof+6T/wAwCv8A+qC2fRF+7G/87v3iqmdQf0OOE4cB8l1wD2wr7VGpxQcQMulKgpOhBkVLsRcTd2naR+1aGp8BuD7NfZUNo5wrd5XS2fVdSUn27GosS1YdZAqSScwKSogcvCtgsgpwjxp2wwWgUZiShS0qBAgEnuqSdyCN6zRbqzSBrFQvjNwzawwvXPYpOUykDTeSB9hn2VbduWLNsNMsiEQCowSo9TO81WdniqGbtlyVqyuguJEZZjLpzJ/CrNxeyCx2iVKhXTXKfIa1h9t2z8Xwk3Wq6x9eylJSAdQNI9kf1rXaYgp1zI2c45Qc2vI+AqNY5hj6lSVJykcieW2h61NPR/hybS1U8sAuPHTQkpSNAJ56yawzwkm22OV/GnGipoNmZUF94JO/gfCvMMxVy4u3W1Zm22k6HQakHU9QPwpojEHlvOpUhKF5gUJVBUoczEwB50TseBbl1XaKcSlDjiFOxIORGobHWTuedZ/LDvtp9MtQeuMLDbTTjSVvOt6JzrMSojM4rqoCt99ZrXObWSDzGo69Tz6Uew1LqlLLjaW20mGwDJUPlHTSmeLKKBIGYjTRXe+v2V2TD9cdz/FBcWqKrh0EzkISABuekDcCsuFOI7GyQ2pVut95RPaggAJEkAIJO+xqV8U8LvOOKfYbTCx3kEwuflDlNRPDMDQyXheWVw4HEQgt5Mzap9YGSDW0kk0rb/UfxPiS6uErS66ShbnaFA0QFHoP4R4DStOF2Sn3W2Ekys6bkTHT6vdUoxZGF9itDVnetOyMq3VI0gajfUE67UsDv22LtFw2w8GkKCw0ChUkAJ9YiTOp05mraVnqQYbFu46WTlAb+DwkwJH+tUU8zm0HSDWhxAAracftXLntVWlw0hS1LcSMisxJmAJ7tR9rEFvLcCITlJgQZAkwDPhWdid7rDH2ULQc242VGo/EVD2mwVAHQTUwusPU6nVyBHKBrzmhSsHRmjOI5bTvrz6VbG9J0O4XlSkJSMqQPf7edFEgUEbsA2gkOK0016zpWnErl1hKSVzMjUdBJqvWztIVNiguMMExH1Ej7KFHiFyPWT7v70LvMXdc3VHlpSYmxAvkGCZA6fqfrp4woESDM7TUfbeKtI16jf2/2qT2FvCROpFMonGsbskJiPWJ9lNbZlQSc252o26BlOmoEih/aHSNZ3qi7pTgT922P8pbfcoo5QTgj93WX8rb/dJo3W7AqVKlQKlSpUCquuIvRf8ACrl24+FZO0UDl7LNEJA3zidulWLSoAPBnDvwC3LHadpK1LzZcnrACIk9OtHqVKg4crNlwpII3BmsK9FBN1rKk9pqULyqKBHrgZVGfYK8S/mDmRMdmnNKjlzRoQJGsTUbsb9IGR0Ep1IKSQpM7wf6VI8L4ZafGdNytSeaSIPkdarZr1pM+tSG3BmEF50vr9RBnX+JW4929S128X2ndUQn7axLIbQGkAJQkbDc+Z51i62MhExI92tZZ3ldGPXZy/ia2wSYVzAUIHsIGhHU0eC+07HtCpKFBMAHprHlVc4biLjjoaXr3jqfDbzqzX7llwt9oSCfUKEqjTkSNJ865vrjqxv8s7fQ/Fm3e0W+LdJnK2wG5zEFWqldBrUtvkvLcZT8I7NhpIKkiQVq6E8wOlRMvf8AjWkZnwWiYcVOVwK5GNB/at1hwzci7W4X8zckpBUTPhvoK0wx6Vzy/VlJxURIgDlOhMeHSo3i9z2i8x15AD9CTSwuzdObtIO2ggaeY2FYX9uoKI5eWnlO9b/xh5Q9bixO8c4kj2+Nb0XMDvpTH6mmjqXvVHsEAD+1MLm0WPWO28eO9N1Ig9ftOHUIJnYjYDpO2nM1pcvEJ0AQnQ6iJ9nICgVzbkbiBz0rUxaJ3USAPE1HKmoLMtW6Cp5XeS2Cs+Ph461WOHYqTdOvKASHM5iIgzIHuqR4xch7uJJS0P4QSM0c1HnQZWHJzEqAKY0Gv1kb1eXrtXQKlt58kakakCdKy/w9wEJ1k/8AqEfZUlZUlI7oAEaxHOtNyRM9DU7TEZet3kfKj2kbztTziS77UtAawiSOcqifsoz2gjTXbf8AW340gUzOVIJ3MCfbQRE2jnNtXure1hLqtcsDqak5TJGuleBxIMQdPdS5GjTDMJSjUnMevIeVFLcgGOR0rW2Z1+yvXBVbdrRlfCJ15RQlTpSIBBP65U7ubiTljWKHFg58wFUWdQ8Cn/Rtj/KW33KKFXnpLsG1rbUp3MhSkqhtWhSSkjWOYNEOEM3+FWmT1vgTGXnr2CY89a5rxi/uXXlunvFZzKISkCSNdAOtbsV+K9KuHxu8fDs/xNDbv0wsAHsrZ5SuQcU22Pekr+yq1w3ha9eaQ63bOKSoSFDLB68+s0atvRpiK4lpCJ+W4jTzykmgsTgbj04g8to24ayoK5DueYUkARkT8rfw8dJvVeejvgi4sblbrymlJU0UDIpRMlSTsUjTQ1YdBQvFPEd0xiV0WX3EftYyhUp7oAHcMp5dKtP0dYy9d2aXnykrzrTKU5ZCTAkTv5VS/HP7wuv98qrZ9D/7uT/vHf8AqoJtSpUqDhylSpUHtHuEMU7F8T6qtDQCskGNRvSi08WUdwfW28Bv/SgSr3RWZUj+4rK2xDOwkqO2/uofbYeX15m05wiCQNvAeNYeetN7vSU4Vw46S24SADyMTHLWpphjq+zIUEzJgA6R4kjfyqFhvEHEqzKDQAhI7uvlO1OLR34T2dmpLjfZjMpWc94xz02rlyluXrqk1PBS8s7haSk3HdkFCkx3IJkEx3jTJOJoZc7BS3UvHd3RIWeUaET7KccPYyhxS2EtrhGxjQRI6STRxy2a7QB1ABI0nWDy151flcfVbjvw9wHF1tApXmcCYJJAzpnadpFF2LpDpUUmI0IOu/M9Aag3FnEYs3BnbUUqIKVjflIBI0FbeEOJG3sxbJgmVoUBKJO4Map19lbS5Xv+McpE6VaQOUTA91D7m2iSddff0+2jtmEqSACcvvrRd4Uc0jbpW2mFArqyC9CIkVBeKz2SywknQST57CrWQ2mNRMfqDVY+kB1tb/cPeiFeHhVbFsdoSHyk67AbfjW1F7MTWD7Q86HqSZqNtNH7ygZg1pXcE6VrQTSCDNNnFkXJ851jw2rNNwdumg8t/wC1ako1n9TWTadTTZptbk+FPWEjwpswNacTpUbNNwrMoHv+umnbRqdKzff7hIMnl9dEGF0coOX5VbWHAoRselaRt3vbTi2yHYiarV46V4JEYdZD/Zbf7pNUP6QrVNpfXCCMqS5mRppDgziPASR7Kvngwf6Ps/5Vj7pNUr6dgV3xCUyUttAxqdlGT7FD6q3njG+pf6KONLRFmWXn0ILbisuYkSlUK6fKKvdVh2uP2rgzN3LKh4OI089dK5a4fsHVJWpLThAIBIQogacyBpuKckjwqUOprO9bdBLTiHADBKFBQBiYkHeCPfW+q89CRHwJ2PnCvu26sOg5w45/eF1/vlVYfo34mtLXDkh99CFdo53ZzL9b5CZV9VVVxneB5+6dGy3HCPLMQPqAoZgjKihKUpKlKkhKQSo68gNTQXyPSpZlxLaEPrzKSkEISASowNFKB3PSp3VIcBcF3Zu2HnrdbbKFZyVwkykEoGQnN62XlV30HDlKlSoFXopURwrC1OmSCEDdUGKWyd1Mm+oOcGYSu4C07gaxPLnUys7hVgjKbYpQT66O/PmAKzZ4bt1toYafSlwpBXEBUdTzTUmRh3wC0Uu2Su4eOgGYx4qJnYVwfTPndOzDHhNoddY22tST+2cVmGUBKkpAPM9KM4fcNKvUW6ic0SEpiYAmVnkDOg/GvdEdm5e2Lt7cqOYBsS0iPbBNTS3xa0t2l3KrXslFJUsBI7SB1qcMMJIfTPKonxVgV/8AC0KtyhpgBPMAnkoq61ni+INMPIS6sqkBKYSVJKj48zNY4zeox+37OyztraVP7TSRykgnpRHh/wBH+Rlv/EF53GlZkEKOnt51pl89s8c9CF7w8l1CS4jOkfK1UJ5jxFALvA3beDaNCAQFHY+PjBG4NGuNuIHksZrJKXcuigNdttPZQ6244UhlC7phYXKUrSkScqtAqPOpkUH8JcyQFBSSfAwDH2U+xHiRttHf18R+pFOexbdbCwTBSCB15++h9zbMGFLIB6kxPhrvWk6nTPXfaC8dcd9kjuJ7yx3F9RyII3qusPxNTplaipR3JOs0c9KzbL7gctFJWlsQtKf4fHxE6aVDcCnOIG9WvhPUhdTpNN0sDc70TebAHe0jeg6bntF5UDujn1qi+28pFZpb2ra4zEVmkUTs0dTXiW8x9kinDzfdr1kRrTYwthO9OVt1glvKZGx1ry5uBGh1qA2uWtaZuulHkK3OqO28/VTS5YWsCBqKAhbtBSc1Bm0qL0DTUbUeaWEIAPd2rehDei6b0adGcGfu+zn5rb/dJqn/AEttkYk4T/E20R5Zcv2pNXFweoGwsyNjbMR9EmhHHfBCL8IWlYbeRoFkZgpOpykSOZkHlJ61tPGVVbwPx6qwQ60m37TM4FZisoHqgQO6Z23o676VQoyrD2VHqXJPvLVaT6Irzk9b+9z8lefFHef/AJrb/mc/+OpQsTgTidF8wVJQlpaFEKaSoHKP4TsND5bg9KkqqrPg70b3NrcpfXcpTl/hZzHONJSoqAGU89DyiDBE64mxFNvaPvKWlGVtZBUQnvZTlAJI1KoAHMmg5mPeHe1neec10dwLaoRYW2RCUSy0TlSEySgSTG58a5vSoRoQdORmuosHtQ0wy0NkNoT/AMqQP6UDylSpUHDleivKe4Vh6nlhA6ST0A3peg8wTBVvSsg9mnc7T4Cpxhdu6yAppTabUQXVGCU6er4mnlnhSWgyEOHIpJGWT3UgSpzTbSQCeZpxauWrlgpTzamrJp0FsAyt2DqVk+tmUdq5c8+Tpww4tC+F2XHGm2rkt/CP2ipkuqGkADkNZ1ozaOXT10bVu2DdoycqnHASpwJ6EkbnoK8ssQQMWUW2yQLUKcWR6iQmUIR8gQdd5J5U0wTjq5vVXDTLSUOdistKkwmCAArxM+/yrPVy9i/IVwlzFl3R7Zttu2SSMoy7DYiDJPnWu6w91/Eir4ayWUxLIVKgPk5eZJH9q1cDJvWm1i4XnUpUJCl5lARqfHWhGD4Xhjd6sdqpb2fupUQAlWaYmJKqialqdWxYAxBabdX+HtMtPyYbeARmA2UEhXPX1ooF/wDT95eKTc3a02dygpCSheZp0fxBSJ06b86E4lw3h9xiZUq+WHswUptEKOYalIX/AAjwjSpvxVhTV5am3mIEoVMwobadZraZeMbjqoVi/BN3ZXfwmyhxlZBW3IET62nPqKkWLWBum/2JyvITEHQEKGx9vPatvAdhcs2qre4dCnQFBshRVCYlJ13ANQ+z4ycXchlSFJeSSFwCPVOpSd4I1g+FTbb4iDODXt/ZBIeQXklWUgbiOnT+tSe+bt7lJSsd5QByAx5SOtN3MV0JHeMAqBEEjkpJncc/6VVvGmKvMOKcQ4qXBCTtE+H4VM7RVnYV6OrEqU84mSoGBIypChB0jfxmq74m4QTaXWVhDhaOqVjvp8RI/rUo9HV89d4cpp9S5OYJc/ijkfGlw7c2+Fh+1U6485lU7lIhIjfSdCZ350tviJraDuDNPSmCWOyzKG5o1jDwUlu4Qjs0PALy/JnRQ9/200fQCNfbSVJuhzugnpWsHf2VpcnNHLl7q2243psOcunsrS1pNZlyB402z8vCo2lpxC8yiBvWqwYVqpVPEW4VvuKdhsCBFNp0FW96krKDuNqwaxEB3KdOhFbP8LyulydNfroKplSHhI0zD269atJKrbUiu2QsFOaDWpWZtAGhge2sL20WlYWJy85/WteXWVUHNrHWoTp01wJ+7bH+UtvuUUcoHwJ+7bH+UtvuUUcrdiVKlSoFQbi3h5F/artnFrQlZScyIkFKgRuCCJGtGaVBR/xLutXDRSpDrXaIzKkoWlIUColB0OnQnyq8KVKgVKlSoOHQKnXBWAoclS3ezAQpaoEqgeHSKjPD+GKeeASkkJ7yo5AdTyqYF4MOIbZOZDw/aaJBI+Tm+TWX1y/kbfLDd3RrhjE2m2UqRmWXLjJmcjUAE7DQJA5eNO7hTWKFxhRUhNu5mURAQQkaiAdBGk0mHrZooabZClNtqdaGh1mCQflU3uL20sSlooKhdKWpwk9flc/4orjmrdze3VZZNXRzi3ES12a7izYJh0NTkzFSUA97TVQ0+uneBX7DSm2ilLNw+gFQiDmI0kcvKgj7d2jEG0MaWyUpCUJIypTl70p3mdfGiONYE18JOJuuKyMoCy2BqSj1ROwSTy31q3Xn7/2lDLhnC1Ya8q5xC4TlVKW0hRUVqJkqjkB/WpYzwbaO3Cb9sKLilZwCqEEkbwf1tQ5nBWcTZZu7wLaygnswQEZc3dKpGk/1oq3hZcvxei5/8MhAQhoE5RA1EbRz01q1v/uqrA8pw9q+dKQgXJBCsqpgkaxrodqHcL8PP2tyt34RmaVJyGSVcxuYHnTHFuAUs3KrtV0lLAWHDMlepzQT40Zx5V26q1dsV52gr9oAQARmGp66TVpO/UXxotLld/f29xauZUsqKXkHRW+sjmDUi4hs7Zh74SqEqBMnYd4ZZjrTbhS/szc3PZs9lcp/1gIhRA5gbcx76b3Ns1ibrq0OksqT2dy0TlLakzldSD9fhWjOmKcfS88WwjQJkKJ7pHu0kj2Vng7DOJBR7NQDS8gGigCOnhTlnDrSxtdXg4AlQCwRmUOgPUEisuGOHnGVuOtvFpgpOVvSAoiVKXPOaaSkLduGEpbRkGsAZsungIoJf8LOtX6blopCFx2qnDsIgpSPExTbhjhpty67Z+/TdKnMlKToOY08BFSzjzhp6+ZS2h7s0hQKupA6VGldq94nwu7Jdcdb/YocOTYAIhOVQ8JkHyqHu3PZlecyDt7as3jjEywwwkHtGVqLLqtz6hAnocwHuqrVW5cbUF+sCdv1tSJpmu6zLAG36mnjZ+umthakEgj/ALU7VofLappHhOprW2KyVqD5Uwu7vIahIywofb9VZ3b4QmaA4deKUrbTU1vxS+Cv2Y3NTxu0bO8Pve0Cp2Boi2EETuKi7iCy1E95R1pzgl0oNKmdDp7qcf6bHrqCIO1BlYYnNIJ/XtrG0u1LSDPODWrEb5SDoR7hVZLvS25p1JwMIw2xH+yW/wByijdA+BT/AKNsf5S2+5RRyulzlSpUqBUqVKgVKlSoFSpUqDjC34guENFlCwhsiFBKUjN5mJNYt448Gw2CnKJiUpKhO8KiRvSpVHGfi3K/pWWOPtEFC4IQWxIBhJ3GorW7izqkoQshQR6uYAke3cjwNKlTjEcr+trePXCXVvBwhxaSlSgBMEAGOmgG1OsM4uvGGy208UpJkylKj71A0qVRxx/E88v1sxbjS9uWgy89mQCDAShMkAgSQBO9LCeNb23a7Fp0BuScpQhWp/zA0qVOGP4jlf0sX4zvLlstPOJUgkGOzbG22oFZYPxxe2zYaZdCUAzBQ2r6ykmlSqeMOVbkekC+DvbZ2u1iM/YM5oPKck1qa45vEvF9K0B0ggqDTUkHkRlg+2vaVNQ3Q65x55eeezGcyoJbQkE/KgCArxGtOLzi28db7FbxLfNMJAPnAlXtpUqahunGF8c3tuAGFttgfJZZ+3JNFD6WsW2+Ej6Jn8lKlTUNgzfGN2kuw4mHlBTiS22UlQ2VlKYSdBtG1Mjjj5M5xP8AlT+FKlTUN17/AI6/M5h/yp/CtSsWdJnN9QpUqahuvRi7o/iHuH4VrdxBatyD7B+FKlTjDdeIxBwbEe4VrbuVBWYHXyBpUqahtvXijpEEgjxSPwpIxRwDKMsdMqfwr2lTUN1rZxBaZykCfAVg/dKX6xB9gpUqahuphh/pXxRlptlt9IQ2hKEDsmjCUJCUiSmToBTj448X+cJ+hZ/LXlKpQ9+OPF/nCfoWfy0vjjxf5wn6Fn8teUqD3448X+cJ+hZ/LS+OPF/nCfoWfy15SoPfjjxf5wn6Fn8tL448X+cJ+hZ/LXlKg9+OPF/nCfoWfy0vjjxf5wn6Fn8teUqD/9k='/ id='image-preview'></div>
                    <div class='animal'>{msg}</div>

                </div>
            </div>
        </form>
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


# 기능 구현 ------------------------------------------------
# (1) WEB 인코딩 설정

model_names = ['min_model', 'hyuck_model', 'hwang_model', 'joo_model']
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

if 'word1' not in form:
    msg = "<p>파일을 선택하지 않았습니다.</p>"

# (3-2) Form안에 textarea 태크 속 데이터 가져오기
else:
    file_field = form['word1']
    image = Image.open(file_field.file)
    result = []

    if file_field.filename:
        preprocessed_image1 = min_preprocessing_img(image)
        result.append(min_predict_value(preprocessed_image1, model_paths[0]))

        preprocessed_image2 = hyuck_preprocessing_img(image)
        result.append(hyuck_predict_value(preprocessed_image2, model_paths[1]))

        preprocessed_image3 = hwang_preprocessing_img(image)
        result.append(hwang_predict_value(preprocessed_image3, model_paths[2]))

        preprocessed_image4 = joo_preprocessing_img(image)
        result.append(joo_predict_value(preprocessed_image4, model_paths[3]))

        animal_list = ["표범", "치타", "호랑이", "사자", "다른 것"]
        
        idx = []
        
        for i in range(len(result)):
            if result[i] == 1:
                idx.append(i)
            
            elif 1 not in result:
                idx = []
                idx.append(4)

        if len(idx) == 1:
            msg = f"<p>이 동물은 {animal_list[idx[0]]} 입니다.</p>"

        elif len(idx) == 2:
            msg = f"<p>이 동물은 {animal_list[idx[0]]} 또는 {animal_list[idx[1]]} 입니다.</p>"
        
        elif len(idx) == 3:
            msg = f"<p>이 동물은 {animal_list[idx[0]]} 또는 {animal_list[idx[1]]} 또는 {animal_list[idx[2]]} 입니다.</p>"
        
        elif len(idx) == 4:
            msg = f"<p>이 동물은 {animal_list[idx[0]]} 또는 {animal_list[idx[1]]} 또는 {animal_list[idx[2]]} 또는 {animal_list[idx[3]]} 입니다.</p>"


    else:
        msg = '<p>올바른 파일을 업로드하세요.<p>'
            
# # (4) 사용자에게 WEB 화면 제공

showHTML(msg)
