from utils import load_data, print_similarity_words
from similarity import find_similar_char, find_similar_word

def main():
    df, radical_list, radical_vectors, word_list, word_vectors = load_data()
    
    print("Characters that have similar radical: ")
    print_similarity_words(find_similar_char("我", df, radical_vectors))
    
    print("\nWords that have similar radical: ")
    print_similarity_words(find_similar_word("色时间", df, radical_list, word_list, word_vectors))

if __name__ == "__main__":
    main()
