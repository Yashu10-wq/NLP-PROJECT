from flask import Flask, render_template, request, jsonify
from keyword_extraction import extract_keywords_keybert
from translate_lang_api import hybrid_translate, detect_language  # make sure detect_language is also imported

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/keyword')
def keyword_page():
    return render_template('keyword.html')

@app.route('/translator')
def translator_page():
    return render_template('translator.html')

@app.route('/extract_keywords', methods=['POST'])
def get_keywords():
    data = request.get_json()
    text = data.get('text', '').strip()
    keywords = extract_keywords_keybert(text)
    return jsonify(keywords=keywords)

@app.route('/translate', methods=['POST'])
def get_translation():
    data = request.get_json()
    text = data.get('text', '').strip()
    target_lang = data.get('target_lang').strip().lower()

    if not text:
        return jsonify({"error": "Text is empty"}), 400

    source_lang = detect_language(text)
    print("📥 Input Text:", repr(text))
    print("🌐 Target Language:", target_lang)
    print("🧠 Detected Source Language:", source_lang)

    if source_lang == target_lang:
        return jsonify(translation=text, source_language=source_lang, note="No translation needed. Languages are same.")

    translated_text = hybrid_translate(text, target_lang)

    if translated_text:
        return jsonify(translation=translated_text, source_language=source_lang)
    else:
        return jsonify({"error": "Translation failed with both APIs"}), 500

if __name__ == '__main__':
    app.run(debug=True)
