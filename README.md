# Amharic E-commerce Data Extractor (Full Project)

This repository contains the complete end-to-end implementation for the Amharic E-commerce Data Extractor project. It details a full pipeline from real-time data ingestion from Telegram to advanced model fine-tuning and the creation of a data-driven FinTech vendor scorecard.

---

## Objective
The primary goal is to transform unstructured Amharic text from multiple e-commerce Telegram channels into a structured dataset. This data is then used to train a Named Entity Recognition (NER) model that powers a vendor analytics engine, helping EthioMart identify promising vendors for micro-lending opportunities.

---

## Workflow Overview

### Task 1: Data Ingestion and Preprocessing
The initial workflow, implemented in local Python scripts, focuses on collecting and cleaning the data.

#### 1. Telegram Scraper Setup
- A Python script using the Telethon library connects to the Telegram API.
- It scrapes messages, images, and metadata (views, timestamps) from 7 specified e-commerce channels.
- Raw data is saved to `data/raw/`.

#### 2. Preprocessing
- A second script cleans the raw text by removing unwanted symbols and normalizing Amharic characters.
- The cleaned data is structured and saved to `data/processed/telegram_data_cleaned.csv`, ready for the next stages.

#### 3. How to Run
- **Scrape Telegram Data:**
  ```bash
  python src/services/telegram_scraper.py
  ```
- **Preprocess the Data:**
  ```bash
  python src/services/preprocess_telegram_data.py
  ```

---

### Task 2: Manual NER Labeling in CoNLL Format
To create training data for our custom model, a subset of 50 messages was manually labeled.

- **Goal:** To annotate Product, Price, and Location entities in Amharic text.
- **Format:** The CoNLL format was used, where each token is on a new line followed by its NER tag (e.g., B-Product, I-Product, O).
- **Output:** The final labeled data is saved as a plain text file (`data/processed/labeled_conll.txt`), which serves as the ground truth for model training.

#### CoNLL Labeling Example
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

#### Entity Types
- **B-Product:** Beginning of a product name (e.g., "Baby bottle")
- **I-Product:** Inside a product name
- **B-LOC:** Beginning of a location (e.g., "Addis" in "Addis Abeba")
- **I-LOC:** Inside a location
- **B-PRICE:** Beginning of a price (e.g., "ዋጋ" in "ዋጋ 1000 ብር")
- **I-PRICE:** Inside a price
- **O:** Any word that is not part of an entity

---

### Task 3: Fine-Tuning the NER Model

- **Objective:** To adapt a pre-trained language model to accurately recognize Product, Price, and Location entities in our specific dataset.
- **Implementation:**
  - The labeled `labeled_conll.txt` file was uploaded to the Colab environment.
  - Using the Hugging Face ecosystem (`transformers`, `datasets`, `evaluate`), the data was loaded, tokenized, and prepared for training.
  - Special care was taken to align NER labels with the tokenizer's sub-word outputs, a critical step for model accuracy.
  - The Hugging Face Trainer API was used to handle the fine-tuning loop, with appropriate hyperparameters (learning_rate, num_train_epochs, etc.) set.
- **Output:** The best-performing fine-tuned model was saved, creating a complete, portable artifact ready for inference and production use.

---

### Task 4: Model Comparison & Selection
To ensure the most effective model was chosen, a comparative analysis was conducted between three different architectures.

#### Models Tested
- **bert-base-multilingual-cased:** A general-purpose multilingual model.
- **bert-tiny-amharic:** An efficient, Amharic-specific model.
- **masakhane/afroxlmr-large:** A large model pre-trained on African languages and NER tasks.

#### Performance Results
| Model                        | Best F1-Score | Precision | Recall | Justification |
|------------------------------|---------------|-----------|--------|---------------|
| masakhane/afroxlmr-large     | 0.723         | 0.739     | 0.708  | Selected Model. Its strong pre-training on relevant languages and tasks allowed it to achieve exceptional performance, even with a small training dataset. |
| bert-base-multilingual-cased | 0.227         | 0.250     | 0.208  | Rejected. Performed poorly, proving that general-purpose models are not always suitable for specialized tasks without extensive data. |
| bert-tiny-amharic            | 0.000         | 0.000     | 0.000  | Rejected. Completely failed to learn the task, indicating its architecture was too small to handle the complexity of NER. |

---

### Task 5: Model Interpretability
To build trust and understand our model's behavior, we used interpretability techniques.

- **Tooling:** LIME (Local Interpretable Model-agnostic Explanations) was used to analyze why the model made certain predictions on specific examples.
- **Insight:** This process helped identify edge cases and flawed heuristics the model might have learned. For instance, analyzing why the model mislabeled a positional word as a location provides a clear path for future data augmentation and model improvement.

---

### Task 6: Vendor Scorecard for Micro-Lending
The final task connects our technical work directly to EthioMart's business goal.

- **Objective:** To create a data-driven "Lending Score" to rank vendors based on their business activity and market reach.
- **Metrics Calculation:**
  - The fine-tuned NER model was first used to extract entities from all 7,000 scraped messages.
  - This structured data was then combined with message metadata to calculate:
    - **Posting Frequency:** Average number of posts per week.
    - **Average Views per Post:** An indicator of customer engagement.
    - **Average Price Point:** To understand the vendor's market segment.
  - **Lending Score Formula:** A weighted score was designed to quantify vendor potential:
    - `Score = (Average Views per Post * 0.6) + (Average Posts per Week * 0.4)`
- **Output:** A summary table ranking vendors by their Lending Score, providing EthioMart with a clear, actionable tool for its micro-lending decisions. The full analysis is available in the final PDF report.

---

## Project Structure
```
Amharic E-commerce Data Extractor/
├── data/
│   ├── raw/              # Raw scraped messages and images
│   └── processed/        # Cleaned data and labeled CoNLL file
├── notebooks/
│   └── NER_Model_Fine_Tuning_and_Analysis.ipynb # Tasks 3-6
├── src/
│   └── services/         # Scraper and preprocessing scripts (Task 1)
├── reports/
│   └── EthioMart_Vendor_Analytics_Report.pdf # Final blog-style report
├── requirements.txt
└── README.md
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
