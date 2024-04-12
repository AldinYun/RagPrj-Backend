from transformers import BertTokenizer, BertModel
import torch

# KoBERT 모델 및 토크나이저 불러오기
tokenizer = BertTokenizer.from_pretrained("jhgan/ko-sbert-multitask")
model = BertModel.from_pretrained("jhgan/ko-sbert-multitask")

def embed_sentence(sentence):
    # 문장을 토큰으로 분할하고 토큰 ID로 변환
    inputs = tokenizer(sentence, return_tensors="pt")
    # 입력을 모델에 전달하여 벡터 임베딩 얻기
    with torch.no_grad():
        outputs = model(**inputs)
    # [CLS] 토큰에 해당하는 벡터 가져오기
    cls_token_embedding = outputs.last_hidden_state[:, 0, :]
    # CPU로 벡터 이동하여 반환
    return cls_token_embedding.cpu().numpy()

