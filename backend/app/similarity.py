import numpy as np
from utils import cosine_similarity, get_vector, get_word_vector

def find_similar_char(char, hanzii_df, radical_vectors, top_k=5):
    row = hanzii_df.loc[hanzii_df["character"] == char]
    if row.empty:
        print(f"❌ Không tìm thấy chữ {char}")
        return
    idx = row.index[0]
    v = radical_vectors[idx]
    
    # Vector hóa: tính cosine similarity cho toàn bộ 1 lần
    sims = radical_vectors @ v
    
    top_idx = np.argsort(sims)[::-1][:top_k]
    
    return [(hanzii_df.iloc[i]['character'], hanzii_df.iloc[i]['radical'], sims[i]) for i in top_idx]

def find_similar_word(word, hanzii_df, radical_list, word_list, word_vectors, top_k=5):
    v_query = get_word_vector(word, hanzii_df, radical_list)
    if v_query is None: return []
    
    sims = cosine_similarity(word_vectors, v_query)
    idxs = np.argsort(sims)[::-1][:top_k]
    
    return [(word_list[i], sims[i]) for i in idxs]