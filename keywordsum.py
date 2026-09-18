import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer  # Import TfidfVectorizer

summary = ""

def preprocess_text(text):
    # Tokenize the text into words
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text)

    # Convert words to lowercase
    words = [word.lower() for word in words]

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]

    return " ".join(words)

def sentence_similarity(sent1, sent2):
    # Preprocess and tokenize sentences
    sent1 = preprocess_text(sent1)
    sent2 = preprocess_text(sent2)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform sentences
    tfidf_matrix = vectorizer.fit_transform([sent1, sent2])

    # Calculate cosine similarity between the vectors
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return similarity[0][0]

def generate_similarity_matrix(sentences):
    n = len(sentences)
    similarity_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j])

    return similarity_matrix

def text_rank(sentences, similarity_matrix, d=0.85, iterations=50):
    n = len(sentences)
    scores = np.ones(n)

    for _ in range(iterations):
        new_scores = np.ones(n) * (1 - d)
        for i in range(n):
            for j in range(n):
                if i != j:
                    new_scores[i] += (d * similarity_matrix[j][i] / np.sum(similarity_matrix[j]))

        scores = new_scores

    return scores

def summarize_text(text, keyword, summary_size=5):
    sentences = sent_tokenize(text)
    keyword_sentences = [sentence for sentence in sentences if keyword.lower() in sentence.lower()]
    similarity_matrix = generate_similarity_matrix(keyword_sentences)
    scores = text_rank(keyword_sentences, similarity_matrix)
    ranked_sentences = sorted([(sentence, score) for sentence, score in zip(keyword_sentences, scores)], key=lambda x: x[1], reverse=True)
    
    selected_sentences = []
    for sentence, score in ranked_sentences:
        for word in nltk.word_tokenize(sentence):
            if word.lower() == keyword.lower():
                selected_sentences.append((sentence, score))
                break
        if len(selected_sentences) == summary_size:
            break

    global summary
    summary = ' '.join([sentence for sentence, _ in selected_sentences])

    if summary == "" or summary == None:
        summary = "400"

    print(f"Summary Text with KeyWord :  {summary}")


# with open("sumdataset.txt", "r", encoding="utf8") as f:
#         intputText = f.read()

# Generate summary based on keyword
# keyword = "linked"
# summary = summarize_text(intputText, keyword, summary_size=50)