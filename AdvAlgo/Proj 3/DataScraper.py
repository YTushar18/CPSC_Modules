import requests
from bs4 import BeautifulSoup
import re
from stopwords import custom_stopwords  # Import custom stop words

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r"<[^>]*>", "", text)
    
    # Remove numbers, periods, special characters, angle brackets, and other characters you want to exclude
    text = re.sub(r"[0-9\.,‹›!\"#$%&'()*+,-/:;<=>?@[\]^_`{|}~]", "", text)
    
    # Remove excess spaces by replacing multiple spaces with a single space
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

def getWepageData(url):

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = clean_text(soup.get_text())
    
    # Tokenize the text
        words = text.split()

    # Remove custom stop words
        filtered_words = [word for word in words if word.lower() not in custom_stopwords]

    # Join the filtered words back into a text
        filtered_text = " ".join(filtered_words)

    # Print the cleaned text with numbers, periods, special characters, and angle brackets "‹" and "›" removed (spaces are kept)
        # print("Cleaned Text:")
        # print(filtered_text)

    # Extract and print all the links
        # print("\nLinks:")
        # for link in soup.find_all("a", href=True):
        #     print(link["href"])
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)
    
    return filtered_text        