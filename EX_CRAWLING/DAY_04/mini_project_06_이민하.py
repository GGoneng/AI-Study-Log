from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import nltk 
from nltk.corpus import stopwords 
from collections import Counter


text = open('output.txt', encoding = 'utf-8').read().lower()
STOPWORDS.add('data')
STOPWORDS.add('i')
STOPWORDS.add('bio')
STOPWORDS.add("i'm")
STOPWORDS.add('awaybio')
token_list = text.lower().split()
token_tagged = nltk.tag.pos_tag(token_list)

tag_list = list()

for word, tag in token_tagged:
    # 제외할 단어 목록 + 명사, 고유명사: 단수, 복수 포함
    if tag in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ, RB']: 
        tag_list.append(word)

counts = Counter(tag_list)
tags = counts.most_common(40)
print(tags)



img_mask = np.array(Image.open('book.jpg'))

wordcloud = WordCloud(width = 400, height = 400,
                      background_color = 'white', max_font_size = 200,
                      stopwords = STOPWORDS,
                      repeat = True, colormap = 'tab20b', mask = img_mask)

cloud = wordcloud.generate(text)

plt.figure(figsize = (10, 8))
plt.axis('off')
plt.imshow(cloud)
plt.show()