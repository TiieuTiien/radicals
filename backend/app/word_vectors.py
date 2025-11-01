import pandas as pd
import numpy as np
import json

hanzii_filepath = "data/hanzii_db.csv"

hanzii_df = pd.read_csv(hanzii_filepath)

with open("data/learned_words.txt", "r", encoding="utf-8") as file:
    word_list = [w.strip() for w in file if w.strip()]

with open("data/radical_list.json", "r", encoding="utf-8") as json_file:
    radical_list = json.load(json_file)


def get_word_vector(word, radical_list, agg="mean"):
    """
    Tính vector cho một từ dựa vào vector của từng chữ.
    agg: 'mean' (mặc định) hoặc 'sum'
    """
    vs = []
    for char in word:
        
        # Tìm bộ thủ trong chữ
        row = hanzii_df.loc[hanzii_df["character"] == char]
        if row.empty:
            raise ValueError(f"Không tìm thấy chữ {char}")
        radical = row["radical"].values[0]
        
        # Lấy vector bộ thủ
        if radical in radical_list:
            vs.append(radical_list[radical])
            
    if not vs:
        return None
    
    vs = np.stack(vs)
    return vs.mean(axis=0) if agg == "mean" else vs.sum(axis=0)


vectors = []
valid_words = []

for w in word_list:
    v = get_word_vector(w, radical_list)
    if v is not None:
        valid_words.append(w)
        vectors.append(v)

word_list = valid_words
word_vectors = np.stack(vectors)

print("✅ Số từ hợp lệ:", len(word_list))
print(word_list, "\n")
print("✅ Kích thước vector:", word_vectors.shape)

with open("data/word_list.json", "w", encoding="utf-8") as f:
    json.dump(word_list, f, ensure_ascii=False, indent=2)

# Lưu vector (numpy)
np.save("data/word_vectors.npy", word_vectors)

def find_similar_word(query_word, word_list, word_vectors, radical_vectors, top_k=5):
    v_query = get_word_vector(query_word, radical_vectors)
    
    if v_query is None:
        print("❌ Không tìm thấy vector cho từ:", query_word)
        return
    
    sims = word_vectors @ v_query / (
        np.linalg.norm(word_vectors, axis=1) * np.linalg.norm(v_query) + 1e-9
    )
    
    top_idx = np.argsort(sims)[::-1][:top_k]
    
    print("Word list: ", word_list)
    for i in top_idx:
        print(f"    Word {i}")
        print(f"{word_list[i]} — similarity={sims[i]:.2f}")
        
find_similar_word("时间", word_list, word_vectors, radical_list)