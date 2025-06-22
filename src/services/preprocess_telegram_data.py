import os
import re
import csv
import pandas as pd
from typing import List

# Function to load raw data from a CSV file
def load_raw_data(file_path: str) -> pd.DataFrame:
    """
    Load raw data from the CSV file into a pandas DataFrame.

    Args:
    - file_path: The path to the CSV file containing raw scraped data.

    Returns:
    - A pandas DataFrame with raw data.
    """
    return pd.read_csv(file_path, encoding="utf-8")

# Function to clean the text data
def clean_text(text: str) -> str:
    """
    Clean raw text by removing unnecessary symbols, emojis, and excessive whitespace.

    Args:
    - text: The raw text message.

    Returns:
    - A cleaned version of the text.
    """
    if pd.isna(text):  # Handle NaN values
        return ""
    
    # Remove emojis and special characters
    text = re.sub(r'[^\w\s፡።፣፤፥፦፧፨ብበበችናየእነእና]', '', text)  # Keep Amharic punctuation
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to tokenize the text into words
def tokenize_text(text: str) -> List[str]:
    """
    Tokenize text into individual words.

    Args:
    - text: Cleaned text message.

    Returns:
    - A list of tokens (words).
    """
    return text.split()

# Function to normalize the text (handling Amharic-specific linguistic features)
def normalize_text(text: str) -> str:
    """
    Normalize text for Amharic-specific linguistic features (e.g., handling variations in characters).

    Args:
    - text: Cleaned and tokenized text.

    Returns:
    - Normalized text.
    """
    # Example: Handle variations of similar-looking Amharic characters
    text = text.replace("ሃ", "ሀ").replace("ኅ", "ሀ").replace("ሐ", "ሀ").replace("ኻ", "ሀ")
    return text

# Function to preprocess a single row of data
def preprocess_row(row: dict) -> dict:
    """
    Preprocess only the 'Message' column and retain other columns as they are.

    Args:
    - row: A dictionary representing a row of raw data.

    Returns:
    - A dictionary with the processed 'Message' column and unprocessed other columns.
    """
    cleaned_message = clean_text(row.get("Message", ""))
    tokenized_message = tokenize_text(cleaned_message)
    normalized_message = normalize_text(" ".join(tokenized_message))
    
    # Return the processed message along with unaltered other columns
    return {
        "Channel Title": row.get("Channel Title", ""),
        "Channel Username": row.get("Channel Username", ""),
        "ID": row.get("ID", ""),
        "Message": normalized_message,  # Preprocessed message
        "Date": row.get("Date", ""), 
        "Media Path": row.get("Media Path", ""),
        "View Count": row.get("View Count", ""), 
    }


# Function to preprocess the entire dataset
def preprocess_data(input_file: str, output_file: str):
    """
    Preprocess the raw data and save the cleaned data to a new CSV file.

    Args:
    - input_file: Path to the raw data CSV file.
    - output_file: Path to save the cleaned data CSV file.
    """
    raw_data = load_raw_data(input_file)
    preprocessed_data = []

    # Process each messages in the dataset
    for _, row in raw_data.iterrows():
        preprocessed_row = preprocess_row(row)
        preprocessed_data.append(preprocessed_row)

    # Save preprocessed data to a new CSV file
    preprocessed_df = pd.DataFrame(preprocessed_data)
    preprocessed_df.to_csv(output_file, index=False, encoding="utf-8")

    print(f"Preprocessed data saved to {output_file}")

# Function to integrate all preprocessing steps
def main_preprocessing():
    """
    Integrate all preprocessing steps: loading, cleaning, tokenizing, normalizing, and saving data.
    """
    input_csv = r'C:\Users\hp\Desktop\matos\tenx 10academy\week 4\Amharic E-commerce Data Extractor\data\raw\telegram_data.csv'
    output_csv = r'C:\Users\hp\Desktop\matos\tenx 10academy\week 4\Amharic E-commerce Data Extractor\data\processed\telegram_data_cleaned.csv'

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)  # Ensure the output directory exists
    preprocess_data(input_csv, output_csv)

# Run the preprocessing pipeline
if __name__ == "__main__":
    main_preprocessing()
