from datasets import load_dataset
import pandas as pd
import os
from src.utils.config import DATASETS_DIR, DATASET_NAME, DATASET_CONFIG

def load_cnn_dailymail_dataset():
    """Load CNN/DailyMail dataset"""
    print("Loading CNN/DailyMail dataset...")
    try:
        dataset = load_dataset(DATASET_NAME, DATASET_CONFIG)
        return dataset
    except Exception as e:
        print(f"Error loading dataset: {e}")
        print("Using a smaller sample for testing...")
        # Fallback to a smaller dataset if CNN/DailyMail fails
        dataset = load_dataset("xsum", split="train[:100]")
        return {"train": dataset, "validation": dataset, "test": dataset}

def prepare_data_splits(dataset):
    """Prepare train/validation/test splits"""
    # Convert to pandas for easier manipulation
    train_df = pd.DataFrame({
        'article': dataset['train']['document'] if 'document' in dataset['train'].column_names else dataset['train']['article'],
        'highlights': dataset['train']['summary'] if 'summary' in dataset['train'].column_names else dataset['train']['highlights']
    })
    
    # If validation and test exist, use them, otherwise create splits
    if 'validation' in dataset and len(dataset['validation']) > 0:
        val_df = pd.DataFrame({
            'article': dataset['validation']['document'] if 'document' in dataset['validation'].column_names else dataset['validation']['article'],
            'highlights': dataset['validation']['summary'] if 'summary' in dataset['validation'].column_names else dataset['validation']['highlights']
        })
    else:
        # Split train data into train/val
        val_df = train_df.sample(frac=0.1, random_state=42)
        train_df = train_df.drop(val_df.index)
    
    if 'test' in dataset and len(dataset['test']) > 0:
        test_df = pd.DataFrame({
            'article': dataset['test']['document'] if 'document' in dataset['test'].column_names else dataset['test']['article'],
            'highlights': dataset['test']['summary'] if 'summary' in dataset['test'].column_names else dataset['test']['highlights']
        })
    else:
        # Use validation as test if no test set
        test_df = val_df.sample(frac=0.5, random_state=42)
        val_df = val_df.drop(test_df.index)
    
    # Save to CSV
    os.makedirs(DATASETS_DIR, exist_ok=True)
    train_df.to_csv(os.path.join(DATASETS_DIR, 'train_data.csv'), index=False)
    val_df.to_csv(os.path.join(DATASETS_DIR, 'val_data.csv'), index=False)
    test_df.to_csv(os.path.join(DATASETS_DIR, 'test_data.csv'), index=False)
    
    print(f"Train size: {len(train_df)}, Validation size: {len(val_df)}, Test size: {len(test_df)}")
    return train_df, val_df, test_df

def load_and_prepare_data():
    """Main function to load and prepare data"""
    dataset = load_cnn_dailymail_dataset()
    return prepare_data_splits(dataset)

if __name__ == "__main__":
    load_and_prepare_data()