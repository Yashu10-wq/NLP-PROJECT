from keybert import KeyBERT

def extract_keywords_keybert(text, top_n=5):
    """
    Extracts keywords from text using KeyBERT.

    Args:
        text (str): The input text.
        top_n (int): The number of top keywords to extract.

    Returns:
        list: A list of the top_n keywords (strings).
    """
    kw_model = KeyBERT()
    keywords_with_scores = kw_model.extract_keywords(text, top_n=top_n)
    # Extract only the keywords (first element of each tuple)
    keywords = [keyword for keyword, score in keywords_with_scores]
    return keywords

if __name__ == '__main__':
    user_text = input("Please enter the text you want to extract keywords from: ")
    num_keywords = int(input("How many top keywords would you like to extract? (e.g., 5, 10): "))

    keywords = extract_keywords_keybert(user_text, top_n=num_keywords)
    print("\nOriginal Text:")
    print(user_text)
    print("\nExtracted Keywords (Top", num_keywords, "):")
    print(keywords)