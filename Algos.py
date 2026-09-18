from nltk.tokenize import word_tokenize
import nltk
import numpy as np 
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from heapq import nlargest
from sklearn.cluster import AgglomerativeClustering
from nltk.corpus import stopwords 
from sklearn.cluster import KMeans
from googletrans import Translator
from nltk.stem import WordNetLemmatizer
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.decomposition import TruncatedSVD

algoArray = ["Agglomerative", "DBScan", "Kmeans"]
langs = ["English", "Spanish", "Hindi", "French", "Korea"]
langCode = ["en", "es", "hi", "fr", "ko"]
intputText = ""
summary = ""

# with open("sumdataset.txt", "r", encoding="utf8") as f:
#         intputText = f.read()

def PreprocessText():
    # Load stopwords and initialize lemmatizer
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    global intputText

    # Remove Punctuation characters
    # intputText = re.sub(r'[^\w\s]', '', intputText)

    # Lowercase Conversion
    intputText = intputText.lower()
    print(f"Lower Case Converted Text : {intputText}\n")
    print("--- End ---\n")

    # Remove numerals
    intputText = re.sub(r'\d+', '', intputText)
    print(f"Removal of numerals : {intputText}\n")
    print("--- End ---\n")

    # Remove extra spaces and duplicate words
    # intputText = ' '.join(set(intputText.split()))
    # print(f"Removal of Extra Spaces and duplicate words : {intputText}\n")
    # print("--- End ---\n")

    # Tokenize
    tokens = word_tokenize(intputText)
    print(f"Tokens : {tokens}\n")
    print("--- End ---\n")

    # Converting all words to Base Form
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    print(f"Converted Tokenized words to Base Form : {tokens}\n")
    print("--- End ---\n")

    # Stop-words Removal
    tokens = [word for word in tokens if word not in stop_words]
    print(f"stop words removal : {tokens}\n")
    print("--- End ---\n")

    processed_text = ' '.join(tokens)
    print(f"final processed text : {processed_text}\n")
    print("--- End ---\n")

    # Create word frequency dictionary
    word_freq = {}
    for word in processed_text:
        if word not in word_freq:
            word_freq[word] = 1
        else:
             word_freq[word] += 1

    # Normalize word frequencies
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    global sent_list
    # Tokenize the text into sentences
    sent_list = nltk.sent_tokenize(intputText)
    
    #Set a Randam Seed for numpy
    np.random.seed(42)

    # Create TF-IDF representation with explicitly set stop words
    tfidf_vectorizer = TfidfVectorizer(stop_words=nltk.corpus.stopwords.words('english'))
    global X
    X = tfidf_vectorizer.fit_transform(sent_list)

    # Perform sentiment analysis using VADER
    sid = SentimentIntensityAnalyzer()
    global sentiment_scores
    sentiment_scores = [sid.polarity_scores(sentence)['compound'] for sentence in sent_list]

    # Apply Latent Semantic Analysis (LSA)
    global num_topics
    num_topics = 20  # Specify the number of topics (clusters)
    lsa = TruncatedSVD(n_components=num_topics,random_state=42)
    global X_lsa
    X_lsa = lsa.fit_transform(X)

def Agglomerative():
    PreprocessText()
     
    # Apply Hierarchical Clustering on the LSA-transformed data
    hierarchical = AgglomerativeClustering(n_clusters=num_topics)
    sentences_clusters = hierarchical.fit_predict(X_lsa)

    # # Calculate sentiment scores for each sentence
    # sentiment_scores = calculate_sentiment_scores(sent_list)

    # Rank sentences in each cluster based on a combination of TF-IDF scores and sentiment scores
    headings_indicators = ["-", ":", "="]
    cluster_ranked_sentences = {}
    for cluster_num in range(num_topics):
        cluster_indices = [i for i in range(len(sent_list)) if sentences_clusters[i] == cluster_num]
        cluster_combined_scores = [0.8 * X[i, :].max() + 0.2 * sentiment_scores[i] for i in cluster_indices]
        sorted_indices = [x for _, x in sorted(zip(cluster_combined_scores, cluster_indices), reverse=True)]
        cluster_ranked_sentences[cluster_num] = sorted_indices

    # Display the ranked sentences for each cluster
    for cluster_num in range(num_topics):
        # print(f"\nCluster {cluster_num + 1} Ranked Sentences:")
        for idx in cluster_ranked_sentences[cluster_num]:
            sentence = sent_list[idx]
            # Check if the sentence contains any heading indicators
            if not any(indicator in sentence.lower() for indicator in headings_indicators):
                print("-", sent_list[idx])

    # Display the generated summary (select sentences based on ranking)
    filtered_summary_sent = []
    for cluster_num in range(num_topics):
        try:
            selected_sentence = nlargest(2, [idx for idx in cluster_ranked_sentences[cluster_num] if
                                             not any(indicator in sent_list[idx].lower() for indicator in
                                                     headings_indicators)], key=lambda x: X[x, :].max())[0]
            filtered_summary_sent.append(selected_sentence)
        except IndexError:
            print(f"Error: Index out of range in cluster {cluster_num + 1}. Check the indices and the length of "
                  f"cluster_ranked_sentences.")

    # Display the generated summary without headings
    global summary
    summary = " ".join([sent_list[idx] for idx in filtered_summary_sent])
    summary = summary.capitalize()
    print(f"\nGenerated Extractive Summary: {summary}")

def DBScan():
    PreprocessText()
    dbscan = DBSCAN(eps=0.9, min_samples=2)  # Adjust parameters based on your preference
    dbscan.fit(X)
    sentences_clusters = dbscan.labels_
    unique_clusters = set(sentences_clusters)
    for cluster_num in unique_clusters:
        if cluster_num == -1:
            # -1 represents noise points in DBSCAN
            noise_sentences = [sent_list[i] for i in range(len(sent_list)) if sentences_clusters[i] == cluster_num]
            print(f"\nNoise Sentences:")
            for sentence in noise_sentences:
                print("-", sentence)
        else:
            cluster_sentences = [sent_list[i] for i in range(len(sent_list)) if sentences_clusters[i] == cluster_num]
            print(f"\nCluster {cluster_num + 1} Sentences:")
            for sentence in cluster_sentences:
                print("-", sentence)
    summary_sent = [nlargest(1, [sent_list[i] for i in range(len(sent_list)) if sentences_clusters[i] == cluster_num], key=len)[0] for cluster_num in unique_clusters if cluster_num != -1]
    global summary
    summary = " ".join(summary_sent)

def Kmeans():
    PreprocessText()
    # Apply KMeans Clustering on the LSA-transformed data
    num_clusters = 20  # Adjust the number of clusters based on your preference
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=20)
    kmeans.fit(X_lsa)
    sentences_clusters = kmeans.predict(X_lsa)

    # # Calculate sentiment scores for each sentence
    # sentiment_scores = calculate_sentiment_scores(sent_list)

    # Rank sentences in each cluster based on a combination of TF-IDF scores and sentiment scores
    headings_indicators = ["-", ":", "="]
    cluster_ranked_sentences = {}
    for cluster_num in range(num_clusters):
        cluster_indices = [i for i in range(len(sent_list)) if sentences_clusters[i] == cluster_num]
        cluster_combined_scores = [0.8 * X[i, :].max() + 0.2 * sentiment_scores[i] for i in cluster_indices]
        sorted_indices = [x for _, x in sorted(zip(cluster_combined_scores, cluster_indices), reverse=True)]
        cluster_ranked_sentences[cluster_num] = sorted_indices

    # Display the ranked sentences for each cluster
    for cluster_num in range(num_topics):
        print(f"\nCluster {cluster_num + 1} Ranked Sentences:")
        for idx in cluster_ranked_sentences[cluster_num]:
            sentence = sent_list[idx]
            # Check if the sentence contains any heading indicators
            if not any(indicator in sentence.lower() for indicator in headings_indicators):
                print("-", sent_list[idx])

    # Display the generated summary (select sentences based on ranking)
    filtered_summary_sent = []
    for cluster_num in range(num_topics):
        try:
            selected_sentence = nlargest(2, [idx for idx in cluster_ranked_sentences[cluster_num] if
                                             not any(indicator in sent_list[idx].lower() for indicator in
                                                     headings_indicators)], key=lambda x: X[x, :].max())[0]
            filtered_summary_sent.append(selected_sentence)
        except IndexError:
            print(f"Error: Index out of range in cluster {cluster_num + 1}. Check the indices and the length of "
                  f"cluster_ranked_sentences.")

    # Display the generated summary without headings
    global summary
    summary = " ".join([sent_list[idx] for idx in filtered_summary_sent])
    summary = summary.capitalize()
    print(f"\nGenerated Extractive Summary: {summary}")

def TranslateText(text,lang):
    translator = Translator()
    translated_summary = translator.translate(text, dest=GetLanguages(lang)).text
    return translated_summary

def Summerize(text,alogrithm):
    global intputText
    intputText = text

    if alogrithm == algoArray[0]:
      Agglomerative()
    elif alogrithm == algoArray[1]:
      DBScan()
    elif alogrithm == algoArray[2]:
      Kmeans()

def GetLanguages(lang):

    if lang == langs[0]:
        return langCode[0]
    elif lang == langs[1]:
        return langCode[1]
    elif lang == langs[2]:
        return langCode[2]
    elif lang == langs[3]:
        return langCode[3]
    elif lang == langs[4]:
        return langCode[4]
    elif lang == langs[5]:
        return langCode[5]
    
# Agglomerative()
   