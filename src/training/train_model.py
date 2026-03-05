from transformers import (
    BartForConditionalGeneration, 
    BartTokenizer,
    Trainer, 
    TrainingArguments,
    DataCollatorForSeq2Seq
)
from datasets import Dataset
import torch
import pandas as pd
from src.utils.config import *
from src.data_processing.preprocess import preprocess_dataset
import os

def prepare_dataset_for_training(df, tokenizer, max_input_length=MAX_INPUT_LENGTH, max_target_length=MAX_TARGET_LENGTH):
    """Prepare dataset for training"""
    def preprocess_function(examples):
        inputs = [doc for doc in examples['article']]
        targets = [summary for summary in examples['highlights']]
        
        model_inputs = tokenizer(
            inputs, 
            max_length=max_input_length, 
            truncation=True, 
            padding=False
        )
        
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(
                targets, 
                max_length=max_target_length, 
                truncation=True, 
                padding=False
            )
        
        model_inputs['labels'] = labels['input_ids']
        return model_inputs
    
    # Convert to HuggingFace Dataset
    dataset = Dataset.from_pandas(df[['article', 'highlights']])
    tokenized_dataset = dataset.map(
        preprocess_function, 
        batched=True,
        remove_columns=['article', 'highlights']
    )
    
    return tokenized_dataset

def train_bart_model():
    """Train BART model on the dataset"""
    print("Loading data...")
    train_df = pd.read_csv(f"{DATASETS_DIR}/train_data.csv")
    val_df = pd.read_csv(f"{DATASETS_DIR}/val_data.csv")
    
    # Preprocess
    train_df = preprocess_dataset(train_df)
    val_df = preprocess_dataset(val_df)
    
    # Load tokenizer and model
    tokenizer = BartTokenizer.from_pretrained(BART_MODEL_NAME)
    model = BartForConditionalGeneration.from_pretrained(BART_MODEL_NAME)
    
    # Prepare datasets
    train_dataset = prepare_dataset_for_training(train_df, tokenizer)
    val_dataset = prepare_dataset_for_training(val_df, tokenizer)
    
    # Data collator
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding=True)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=os.path.join(MODELS_DIR, 'bart_model'),
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=os.path.join(MODELS_DIR, 'logs'),
        logging_steps=100,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        save_total_limit=2,
        remove_unused_columns=False,
        fp16=torch.cuda.is_available(),
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    
    # Train
    print("Starting training...")
    trainer.train()
    
    # Save final model
    model.save_pretrained(os.path.join(MODELS_DIR, 'bart_model', 'final'))
    tokenizer.save_pretrained(os.path.join(MODELS_DIR, 'bart_model', 'final'))
    print("Training completed and model saved!")
    
    return trainer

if __name__ == "__main__":
    train_bart_model()