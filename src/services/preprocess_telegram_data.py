import pandas as pd
import re
import os

# 1. Load the raw scraped data from the CSV file
# Change the path if your file is in a different location
raw_csv_path = r'C:\Users\hp\Desktop\matos\tenx 10academy\week 4\Amharic E-commerce Data Extractor\data\raw\telegram_data.csv'
df = pd.read_csv(raw_csv_path)

# 2. Define a function to clean the message text
def clean_text(text):
    """
    Cleans the input text by:
    - Removing URLs
    - Removing non-Amharic letters and numbers (keeps Amharic, English, numbers, and basic punctuation)
    - Removing extra spaces
    """
    if pd.isnull(text):
        return ""
    # Remove URLs
    text = re.sub(r"http\S+", "", text)
    # Remove unwanted characters (keep Amharic, English, numbers, and basic punctuation)
    text = re.sub(r"[^\u1200-\u137F\w\s፡።፣፤፥፦፧፨.,!?]", "", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# 3. Apply the cleaning function to the 'Message' column
df['Cleaned_Message'] = df['Message'].apply(clean_text)

# 4. Tokenize the cleaned message
def tokenize_text(text):
    """
    Splits the cleaned text into a list of words (tokens).
    This is a simple whitespace split. For Amharic, more advanced tokenizers can be used if available.
    """
    return text.split()

df['Tokens'] = df['Cleaned_Message'].apply(tokenize_text)

# 5. (Optional) Remove Amharic stopwords
# You can expand this list with more Amharic stopwords as needed
amharic_stopwords = set([
    "እና", "እዚህ", "ይህ", "ያ", "ነው", "አይደለም", "እንደ", "ለ", "በ", "ከ", "ወደ", "እስከ", "እ", "የ", "ማን", "ምን", "ለምን", "የት", "እንግዲኛ"
])

def remove_stopwords(tokens):
    """
    Removes common Amharic stopwords from the list of tokens.
    """
    return [token for token in tokens if token not in amharic_stopwords]

df['Tokens_No_Stopwords'] = df['Tokens'].apply(remove_stopwords)

# 6. Organize columns for clarity
# You can add or remove columns as needed for your downstream tasks
columns_to_keep = [
    'Channel Title', 'Channel Username', 'ID', 'Date', 'Media Path', 'View Count',
    'Cleaned_Message', 'Tokens', 'Tokens_No_Stopwords'
]
df_final = df[columns_to_keep]

# 7. Save the preprocessed data to a new CSV file
preprocessed_csv_path = r'C:\Users\hp\Desktop\matos\tenx 10academy\week 4\Amharic E-commerce Data Extractor\data\raw\preprocessed_telegram_data.csv'
df_final.to_csv(preprocessed_csv_path, index=False, encoding='utf-8')

# 8. Print a message to confirm completion
print(f"Preprocessing complete! Preprocessed data saved to: {preprocessed_csv_path}")

# ---------------------------
# What this script does:
# - Loads your raw Telegram data
# - Cleans and normalizes the message text
# - Tokenizes the text into words
# - Removes common Amharic stopwords
# - Keeps important metadata (channel, date, media, etc.)
# - Saves the cleaned and structured data for further analysis