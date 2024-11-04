import cgi, cgitb
import sys, codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

cgitb.enable()

def showHTML():
    print("Content-Type: text/html; charset=utf-8")

    print(f"""
        
        <!DOCTYPE html>
        <html lang="ko">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>머신러닝은 어려웡</title>
        """+
        """
        <style>
            * {
                text-align: center;
            }

            body {
                background-color:rgb(246, 251, 255)
            }

            header {
                height:20vh;
                padding-top:7vh;
                font-size : 30px;
                font-weight: bold;
                color:rgb(154, 208, 255);
            }

            nav {
                display:flex;
                padding:8vh;
                justify-content:space-between;
                height:7vh;
            }

            nav div {
                flex-grow:1;
                display:flex;
                padding: 10px;
                background-color:rgb(154, 208, 255);
                justify-content: center;
                align-items: center;
                border-left: 1px solid white;
                border-right: 1px solid white;
            }
            
            a {
                color: rgb(46, 36, 36);
                font-size: 22px;
                font-weight: bold;
                text-decoration: none;
            }

            a:visited {
                color : rgb(46, 36, 36)
            }

            a:hover {
                color: rgb(46, 36, 36)
            }

            a:active {
                color: rgba(46, 36, 36, 0.317)
            }

            section {
                display: flex;
                padding: 8vh;
                height: 7vh;
                justify-content:space-between;
            }

            section div {
                flex-grow: 1;
                padding: 10px;
                justify-content: center;
                align-items: center;
                border: 1px solid rgb(46, 36, 36);
            }

        </style>
    </head>
    """)
    print(f"""
    <body>
        <header>
            <h1>모델 연결 웹</h1>
        </header>

        <nav>
            <div><a href="./test.py">Machine Learning</a></div>
            <div><a href="#dl">Deep Learning</a></div>
            <div><a href="#cv">CV Deep Learning</a></div>
            <div><a href="#nlp">NLP Deep Learning</a></div>
        </nav>
        <section>
            <div id="ml">
                Machine Learning
            </div>
            <div id="dl">
                Deep Learning
            </div>
            <div id="cv">
                CV Deep Learning
            </div>
            <div id="nlp">
                NLP Deep Learning
            </div>
        </section>
    </body>
    </html>
        """)
    
showHTML()