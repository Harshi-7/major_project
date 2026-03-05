import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
DATASETS_DIR = os.path.join(DATA_DIR, 'datasets')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Create directories if they don't exist
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, DATASETS_DIR, MODELS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# Model configurations
BART_MODEL_NAME = "facebook/bart-large-cnn"
PEGASUS_MODEL_NAME = "google/pegasus-cnn_dailymail"

# Training parameters
MAX_INPUT_LENGTH = 1024
MAX_TARGET_LENGTH = 150
BATCH_SIZE = 4
EPOCHS = 3
LEARNING_RATE = 2e-5

# Dataset configuration
DATASET_NAME = "cnn_dailymail"
DATASET_CONFIG = "3.0.0"
TEST_SIZE = 0.1
VAL_SIZE = 0.1
RANDOM_SEED = 42