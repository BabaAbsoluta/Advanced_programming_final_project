import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Download necessary NLTK data (only need to run these once)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('averaged_perceptron_tagger_eng',quiet=True)


def clean_and_extract_words(text):
    # Convert to lowercase
    text = text.lower()

    # Tokenize the text
    words = word_tokenize(text)

    # Get English stopwords
    stop_words = set(stopwords.words('english'))

    # Filter out stopwords
    filtered_words = [word for word in words if word not in stop_words]

    # Apply POS tagging
    tagged_words = pos_tag(filtered_words)

    # Extract nouns (NN*) and adjectives (JJ*)
    important_words = [word for word, tag in tagged_words
                       if tag.startswith('NN') or tag.startswith('JJ')]

    return important_words