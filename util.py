import nltk
import json
import numpy as np
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# 🔹 Load FAQ
def load_faq(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    questions = [item["question"] for item in data]
    answers = [item["answer"] for item in data]
    return questions, answers


# 🔹 Synonym expansion
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms


# 🔹 Preprocessing
def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [w for w in tokens if w.isalnum()]
    tokens = [w for w in tokens if w not in stop_words]

    expanded = []
    for word in tokens:
        expanded.append(lemmatizer.lemmatize(word))
        expanded.extend(get_synonyms(word))  # add synonyms

    return ' '.join(set(expanded))


# 🔹 Spell correction (basic)
def correct_spelling(user_input, questions):
    words = user_input.split()
    corrected = []
    for word in words:
        matches = get_close_matches(word, questions, n=1, cutoff=0.8)
        corrected.append(matches[0] if matches else word)
    return ' '.join(corrected)


# 🔹 Build model
class ChatEngine:
    def __init__(self, questions):
        self.processed = [preprocess(q) for q in questions]

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.vectors = self.vectorizer.fit_transform(self.processed)

    def get_response(self, user_input, questions, answers):
        processed_input = preprocess(user_input)
        input_vec = self.vectorizer.transform([processed_input])

        similarities = cosine_similarity(input_vec, self.vectors)
        idx = np.argmax(similarities)
        score = similarities[0][idx]

        if score > 0.35:
            return answers[idx]
        else:
            return None