import pandas as pd, numpy as np, json
from numpy.linalg import norm
from config import *

def load_data():
    """
    Load all datasets and precomputed vectors defined in config.py.

    Loads the following:
        - Hanzi dataset (CSV)
        - Radical list and vectors (JSON + NPY)
        - Word list and vectors (JSON + NPY)

    Returns
    -------
    tuple: tuple
        Tuple containing `(hanzii_df, radical_list, radical_vectors, word_list, word_vectors)`.

    hanzii_df: pandas.DataFrame
        DataFrame containing Hanzi characters and metadata such as radicals, pinyin, and stroke count.

    radical_list: dict[str, numpy.ndarray]
        Mapping of radicals to their one-hot or embedded vector representations.

    radical_vectors: numpy.ndarray
        2D array of precomputed radical vectors.

    word_list: list[str]
        List of learned words (each can be a single Hanzi or multi-character word).

    word_vectors: numpy.ndarray
        2D array of precomputed word vectors aligned with `word_list`.

    Raises
    ------
    FileNotFoundError
        If one or more expected files are missing.
    json.JSONDecodeError
        If a JSON file is malformed.
    """

    hanzii_df = pd.read_csv(HANZII_FILE)
    
    with open(RADICAL_LIST, encoding="utf-8") as f:
        radical_list = {k: np.array(v) for k, v in json.load(f).items()}
    radical_vectors = np.load(RADICAL_VECTORS, allow_pickle=True)
    
    with open(WORD_LIST, encoding="utf-8") as f:
        word_list = json.load(f)
    word_vectors = np.load(WORD_VECTORS, allow_pickle=True)

    return hanzii_df, radical_list, radical_vectors, word_list, word_vectors

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    
    return (a @ b) / (norm(a, axis=1) * norm(b) + 1e-9)

def get_vector(char, hanzii_df, radical_list):
    row = hanzii_df.loc[hanzii_df["character"] == char]
    
    if row.empty:
        return None
    
    radical = row["radical"].values[0]
    
    return radical_list.get(radical)

def get_word_vector(word, hanzii_df, radical_list, agg="mean"):
    vs = [get_vector(c, hanzii_df, radical_list) for c in word if get_vector(c, hanzii_df, radical_list) is not None]
    
    if not vs: return None
    
    arr = np.stack(vs)
    
    return arr.mean(axis=0) if agg == "mean" else arr.sum(axis=0)

def print_similarity_words(words_tuple):
    tuple_items_count = len(words_tuple[0])
    
    if (tuple_items_count == 3):
        for word in words_tuple:
            print(f"{word[0]} - radical {word[1]} - similarity={word[2]:.2f}")
            
    if (tuple_items_count == 2):
        for word in words_tuple:
            print(f"{word[0]} - similarity={word[1]:.2f}")