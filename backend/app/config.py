import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

HANZII_FILE = os.path.join(DATA_DIR, "hanzii_db.csv")
RADICAL_LIST = os.path.join(DATA_DIR, "radical_list.json")
RADICAL_VECTORS = os.path.join(DATA_DIR, "radical_vectors.npy")
WORD_LIST = os.path.join(DATA_DIR, "word_list.json")
WORD_VECTORS = os.path.join(DATA_DIR, "word_vectors.npy")