import fasttext
import requests
import urllib.parse

# Load fastText language detection model
lid_model_path = "C:/Users/DELL/OneDrive/Desktop/ASEP Project/asep2/lid.176.bin"
lid_model = fasttext.load_model(lid_model_path)

def detect_language(text):
    lid_prediction = lid_model.predict(text)
    source_lang_code = lid_prediction[0][0].replace("__label__", "")
    return source_lang_code



def translate_with_mymemory(text, source_lang, target_lang):
    try:
        encoded_text = urllib.parse.quote(text)
        url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair={source_lang}|{target_lang}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()["responseData"]["translatedText"]
        else:
            print("MyMemory Error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("MyMemory API Error:", e)
        return None

def hybrid_translate(text, target_lang):
    source_lang = detect_language(text)
    print("Detected Source Language:", source_lang)

    if source_lang == target_lang:
        print("Source and target languages are the same. No translation needed.")
        return text

  

    print("Falling back to MyMemory...")
    translation = translate_with_mymemory(text, source_lang, target_lang)
    return translation

if __name__ == "__main__":
    text_to_translate = input("Enter the text you want to translate: ")
    target_language_code = input("Enter the target language code (e.g., en, hi, fr): ").lower()

    translated_output = hybrid_translate(text_to_translate, target_language_code)

    print("\n--- Translation Results ---")
    print("Original Text:", text_to_translate)
    source_language_code = detect_language(text_to_translate)
    print("Detected Source Language:", source_language_code)
    if translated_output:
        print("Translated Text (", target_language_code, "):", translated_output)
    else:
        print("Translation failed with both APIs.")
