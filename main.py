#!/usr/bin/env python3
"""
Legal Document Summarizer
Main entry point for the application
"""

import argparse
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_processing.dataset_loader import load_and_prepare_data
from src.training.train_model import train_bart_model
from src.inference.generate_summary import SummaryGenerator
from app.app import create_app

def main():
    parser = argparse.ArgumentParser(description='Legal Document Summarizer')
    parser.add_argument('--mode', type=str, default='web',
                        choices=['web', 'train', 'inference'],
                        help='Mode to run the application')
    parser.add_argument('--input', type=str,
                        help='Input file for inference mode')
    parser.add_argument('--output', type=str,
                        help='Output file for inference mode')
    parser.add_argument('--model', type=str, default='bart',
                        choices=['bart', 'pegasus'],
                        help='Model to use')
    
    args = parser.parse_args()
    
    if args.mode == 'web':
        print("Starting web application...")
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.mode == 'train':
        print("Starting training...")
        # First load and prepare data
        print("Loading dataset...")
        load_and_prepare_data()
        
        # Then train the model
        print("Training BART model...")
        train_bart_model()
    
    elif args.mode == 'inference':
        if not args.input:
            print("Error: --input is required for inference mode")
            sys.exit(1)
        
        print(f"Running inference with {args.model} model...")
        generator = SummaryGenerator(model_type=args.model)
        generator.summarize_file(args.input, args.output)

if __name__ == "__main__":
    main()