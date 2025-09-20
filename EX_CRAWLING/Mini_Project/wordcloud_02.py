from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

text = open('alice.txt').read()
STOPWORDS.add('said')
print('STOPWORDS:', STOPWORDS)

img_mask = np.array(Image.open('cloud.png'))

wordcloud = WordCloud(width = 400, height = 400,
                      background_color = 'white', max_font_size = 200,
                      stopwords = STOPWORDS,
                      repeat = True,
                      colormap = 'inferno', mask = img_mask).generate(text)

print(wordcloud.words_)

plt.figure(figsize = (10, 8))
plt.axis('off')
plt.imshow(wordcloud)
plt.show()