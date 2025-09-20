from konlpy.tag import Okt

okt = Okt()
text = "마음에 꽂힌 칼한자루 보다 마음에 꽂힌 꽃한송이가 더 아파서 잠이 오지 않는다"

okt_tags = okt.pos(text, norm = True, stem = True)
print(okt_tags)

okt_nouns = okt.nouns(text)
print(okt_nouns)