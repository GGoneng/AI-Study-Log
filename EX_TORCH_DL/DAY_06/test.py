import joblib
from MinModule import *
import pandas as pd

sentence = "it's a good thing!"

preprocessed_sentence = preprocessing(sentence)

print(preprocessed_sentence)

def custom_analyzer(x):
    return x

loaded_vectorizer = joblib.load(r'C:\Users\KDP-2\OneDrive\바탕 화면\Python\EX_TORCH_DL\WEB\cgi-bin\count_vectorizer.pkl')
input_vector = loaded_vectorizer.transform([preprocessed_sentence]).toarray()

print(input_vector)
input_vectorDF = pd.DataFrame(input_vector)

print(f'\n\n{input_vectorDF}')

h_inouts = range(400, 99, -100)

best_model = BCFModel(in_in = 630, in_out = 50, out_out = 1, h_ins = h_inouts, h_outs = h_inouts)
best_model.load_state_dict(torch.load(r'C:\Users\KDP-2\OneDrive\바탕 화면\Python\EX_TORCH_DL\WEB\cgi-bin\model_weights_3.pth', weights_only=True))
result = predict_value(input_vectorDF, best_model)

if result.item() == 0:
    answer = '부정적인 문장입니다.'

elif result.item() == 1:
    answer = '긍정적인 문장입니다.'

print(answer)
