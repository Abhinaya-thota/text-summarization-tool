# text-summarization-tool
Interactive NLP text summarization tool with clustering, entity recognition, translation, and text-to-speech
# Text Summarization Tool

An interactive text summarization app with three modes — algorithmic clustering, keyword-based extraction, and named entity visualization — plus multilingual translation and text-to-speech output.

## Features

- **Algorithm-based summarization** — clusters sentences by similarity using one of three algorithms (Agglomerative Clustering, DBSCAN, KMeans), ranking sentences within each cluster by TF-IDF and sentiment score, then extracting representative sentences.
- **Keyword-based summarization** — generates a summary centered on a user-provided keyword, using TF-IDF and cosine similarity to find the most relevant sentences.
- **Named entity visualization** — extracts and visually highlights entities (people, organizations, locations) using spaCy's `displacy` renderer.
- **Multilingual translation** — translates the generated summary into another language via the Googletrans API.
- **Text-to-speech** — reads the generated summary aloud using `pyttsx3`.
- **Interactive UI** — built with Streamlit; no HTML/CSS/JS required to run it.

## How It Works

1. **Preprocessing** — input text is tokenized, lowercased, stripped of stopwords, and lemmatized (NLTK).
2. **Clustering (Algorithm mode)** — sentences are vectorized (TF-IDF) and clustered by similarity; representative sentences are pulled from each cluster to ensure the summary covers every major topic in the input, not just the most repeated one.
3. **Ranking** — sentences are scored using a combination of TF-IDF weight and sentiment intensity (NLTK's `SentimentIntensityAnalyzer`).
4. **Output** — the top-ranked sentences are assembled into the final summary, optionally translated and/or read aloud.

## Tech Stack

`Python` `Streamlit` `NLTK` `spaCy` `scikit-learn` `Googletrans` `pyttsx3`

## Running It Locally

\`\`\`bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords wordnet vader_lexicon

streamlit run main.py
\`\`\`

## Repository Structure

\`\`\`
├── main.py                  # Streamlit app / UI entry point
├── Algos.py                 # Clustering-based summarization algorithms + translation
├── keywordsum.py             # Keyword-based summarization
├── visualize_entites.py      # Named entity recognition + visualization
├── Audio.py                  # Text-to-speech summary playback
├── requirements.txt
└── sumdataset.txt / bubble tea dataset.txt   # Sample input texts for testing
\`\`\`

## Future Improvements

- Add a transformer-based abstractive summarization option (e.g., BART/T5 via Hugging Face) alongside the current extractive methods
- Evaluate summary quality quantitatively using ROUGE scores
- Support real-time summarization of streaming content (e.g., an RSS feed)
- Deploy as a live demo (Streamlit Community Cloud)

---
*My first end-to-end NLP project — built as an undergraduate capstone.*
