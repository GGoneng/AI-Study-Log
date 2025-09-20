'''
    영어 자연어 분석: NLTLK
    - https://www.nltk.org/api/nltk.tokenize.html
    - https://soyoung-new-challenge.tistory.com/31
    
'''
import nltk 
from nltk.corpus import stopwords 
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import platform


# word cloud 생성시 제외할 단어 목록 
exclude_word_list =['ChatGPT', 'GPT', 'AI', 'ai', 'Machine learning', 'users', 'data', 'information', 
                    'OpenAI', 'chatbot']

file_name = 'chatgpt_sideeffect.txt'
text = open(file_name, encoding='utf-8').read()
#------------------------------------------------------------------
# 단어별 분리 
#------------------------------------------------------------------
token_list = nltk.word_tokenize(text)
#print(word_list)

#------------------------------------------------------------------
# 품사 태깅 
#------------------------------------------------------------------
token_tagged = nltk.tag.pos_tag(token_list)
#print(tagged)

#------------------------------------------------------------------
# 불용어(stopword) 추가
#  - 의미가 없는 단어 제거 
#------------------------------------------------------------------
stop_words = stopwords.words('english') # english: 영어 불용어 확인 
#stop_words.append('불용어') # 불용어 추가 
#print('stopwords: ')
#print(stop_words)
# 단수 명사: NN, 복수명사: NNS, 고유명사(단수): NNP, 고유명사(복수): NNPS
# 형용사: JJ, 동사 원형: VB, 전치사: IN, 부사: RB 

tag_list = list()

for word, tag in token_tagged:
    # 제외할 단어 목록 + 명사, 고유명사: 단수, 복수 포함
    if word not in exclude_word_list and tag in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ, RB']: 
        tag_list.append(word)

#print(tag_list)
# 가장 많이 나온 단어부터 40개를 저장
counts = Counter(tag_list)
tags = counts.most_common(40)
print(tags)

 
#------------------------------------------------------------------
# WordCloud를 생성
#------------------------------------------------------------------

if platform.system() == 'Windows':
    path = r'c:\Windows\Fonts\malgun.ttf'
elif platform.system() == 'Darwin': # Mac OS
    path = r'/System/Library/Fonts/AppleGothic'
else:
    path = r'/usr/share/fonts/truetype/name/NanumMyeongjo.ttf'

wc = WordCloud(font_path=path, background_color="white", max_font_size=60)
#wc = WordCloud(font_path=path, background_color="black", max_font_size=60, colormap='Accent')

cloud = wc.generate_from_frequencies(dict(tags))

# 생성된 WordCloud를 test.jpg로 보낸다.
#cloud.to_file('test.jpg')

plt.figure(figsize=(10, 8))
plt.axis('off')
plt.imshow(cloud)
plt.show()

