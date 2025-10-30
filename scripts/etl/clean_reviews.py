def clean_reviews():
    """
    Cleans the reviews data by removing duplicates, handling missing values,
    and standardizing text fields.
    """
    import pandas as pd
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    import re

    # Load the raw reviews data
    df = pd.read_csv('../../data/raw/reviews.csv')

    # Remove duplicate reviews based on 'review_id'
    df.drop_duplicates(subset='review_id', inplace=True)

    # Handle missing values: drop rows with missing 'review_text' or 'user_id'
    df.dropna(subset=['review_text', 'user_id'], inplace=True)

    # Standardize text fields: lowercase, remove punctuation, and stopwords
    nltk.download('stopwords', download_dir='nltk_data')
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    def preprocess_text(text):
        # Lowercase
        text = text.lower()
        # Remove punctuation and non-alphabetic characters
        text = re.sub(r'[^a-z\s]', '', text)
        # Tokenize and remove stopwords, then stem
        tokens = text.split()
        filtered_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
        return ' '.join(filtered_tokens)

    df['cleaned_review_text'] = df['review_text'].apply(preprocess_text)

    # Save the cleaned data to a new CSV file
    df.to_pickle('../../data/processed/cleaned_reviews.pkl')