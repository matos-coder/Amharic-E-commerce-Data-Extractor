# Amharic E-commerce Data Extractor (Task 1 & Task 2)

This repository contains the implementation of Task 1 (Data Ingestion & Preprocessing) and Task 2 (Manual NER Labeling) for Amharic e-commerce Telegram data. The project demonstrates how to collect, clean, and structure real-world Amharic text data for downstream NLP tasks such as entity extraction.

---

## Objective

- **Task 1:** Collect messages from multiple Ethiopian Telegram e-commerce channels, clean and preprocess the data (text, images, metadata), and store it in a structured format for further analysis.
- **Task 2:** Manually label a subset of messages in CoNLL format for Named Entity Recognition (NER), identifying products, prices, and locations in Amharic text.

---

## Workflow Overview

### Task 1: Data Ingestion and Preprocessing

The workflow is implemented in [`src/services/telegram_scraper.py`](src/services/telegram_scraper.py) and [`src/services/preprocess_telegram_data.py`](src/services/preprocess_telegram_data.py):

1. **Telegram Scraper Setup**
   - Use the provided Python script to connect to Telegram using your credentials.
   - Specify at least 5 relevant e-commerce channels in the script.
   - The script fetches messages, images, and metadata (channel, date, etc.) from each channel.
   - Raw messages and metadata are saved in `data/raw/telegram_data.csv`.
   - Images are saved in `data/raw/photos/`.

2. **Preprocessing the Data**
   - Run the preprocessing script to clean and structure the raw data.
   - **Cleaning:** Removes unwanted symbols, emojis, and extra spaces from the text.
   - **Tokenization:** Splits Amharic text into words (tokens). For advanced tokenization, you can use the `amseg` library (see comments in the script).
   - **Normalization:** Handles Amharic-specific character variations (e.g., unifying similar letters).
   - **Stopword Removal:** Removes common Amharic stopwords.
   - **Structuring:** Keeps important metadata (channel, date, media path, etc.) and saves the cleaned data in `data/processed/telegram_data_cleaned.csv`.

3. **How to Run**
   - **Scrape Telegram Data:**
     ```bash
     python src/services/telegram_scraper.py
     ```
     Follow the prompts to log in and download messages/images.
   - **Preprocess the Data:**
     ```bash
     python src/services/preprocess_telegram_data.py
     ```
     The cleaned and structured data will be saved in the processed folder.

---

### Task 2: Manual NER Labeling in CoNLL Format

1. **What is the Goal?**
   - Manually label 30-50 messages from your processed dataset for Named Entity Recognition (NER).
   - Identify and label entities such as products, prices, and locations in Amharic text.

2. **CoNLL Format Explained**
   - Each word (token) is written on its own line, followed by its entity label.
   - A blank line separates each message.
   - Example:
     ```
     ዋጋ    B-PRICE
     1000   I-PRICE
     ብር    I-PRICE
     በ     O
     አዲስ   B-LOC
     አበባ  I-LOC
     Baby   B-Product
     bottle I-Product
     ```

3. **Entity Types**
   - **B-Product:** Beginning of a product name (e.g., "Baby bottle")
   - **I-Product:** Inside a product name
   - **B-LOC:** Beginning of a location (e.g., "Addis" in "Addis Abeba")
   - **I-LOC:** Inside a location
   - **B-PRICE:** Beginning of a price (e.g., "ዋጋ" in "ዋጋ 1000 ብር")
   - **I-PRICE:** Inside a price
   - **O:** Any word that is not part of an entity

4. **How to Label**
   - Open your processed CSV file and select 30-50 messages from the "Message" column.
   - For each message:
     - Split the message into words (tokens).
     - For each word, decide if it is part of a product, price, location, or none (O).
     - Write each word and its label on a separate line.
     - Leave a blank line after each message.
   - Save your labeled data in a plain text file (e.g., `data/processed/labeled_conll.txt`).

5. **Why is this Important?**
   - This labeled data is used to train and evaluate machine learning models for entity extraction (NER).
   - Accurate labeling helps your model learn to find products, prices, and locations in Amharic text.

---

## Project Structure

```
Amharic E-commerce Data Extractor/
├── data/
│   ├── raw/              # Raw scraped messages and images
│   └── processed/        # Cleaned data and labeled CoNLL file
├── src/
│   └── services/         # Scraper and preprocessing scripts
├── requirements.txt
├── README.md
```

---

## References
- [Telethon Documentation](https://docs.telethon.dev/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [amseg Amharic Tokenizer](https://github.com/hlayile/amseg)
- [CoNLL Format for NER](https://www.clips.uantwerpen.be/conll2003/ner/)

---

## Contact
For questions or collaboration, contact:  
matiasashenafi0@gmail.com
