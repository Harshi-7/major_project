import pandas as pd
import re
from transformers import AutoTokenizer
from src.utils.config import *

def clean_text(text):
    """Basic text cleaning"""
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:""''()\-]', '', text)
    return text.strip()

def preprocess_dataset(df, text_column='article', summary_column='highlights'):
    """Preprocess the dataset"""
    processed_df = df.copy()
    
    # Clean text
    processed_df[text_column] = processed_df[text_column].apply(clean_text)
    processed_df[summary_column] = processed_df[summary_column].apply(clean_text)
    
    # Remove empty rows
    processed_df = processed_df[
        (processed_df[text_column].str.len() > 50) & 
        (processed_df[summary_column].str.len() > 10)
    ]
    
    return processed_df

def tokenize_data(tokenizer, texts, summaries, max_input_length=MAX_INPUT_LENGTH, max_target_length=MAX_TARGET_LENGTH):
    """Tokenize the data for training"""
    model_inputs = tokenizer(
        texts, 
        max_length=max_input_length, 
        truncation=True, 
        padding=True,
        return_tensors='pt'
    )
    
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            summaries, 
            max_length=max_target_length, 
            truncation=True, 
            padding=True,
            return_tensors='pt'
        )
    
    model_inputs['labels'] = labels['input_ids']
    return model_inputs

if __name__ == "__main__":
    # Test preprocessing
    train_df = pd.read_csv(f"{DATASETS_DIR}/train_data.csv")
    processed_train = preprocess_dataset(train_df)
    print(f"Original size: {len(train_df)}, Processed size: {len(processed_train)}")