#!/usr/bin/env python3
"""
Simple run script for Legal Document Summarizer
This will work immediately without requiring dataset loading
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.bart_summarizer import BartSummarizer
from src.models.pegasus_summarizer import PegasusSummarizer
from app.app import create_app

def test_summarizer():
    """Test the summarizer with a sample text"""
    print("=" * 50)
    print("Testing Legal Document Summarizer")
    print("=" * 50)
    
    # Sample legal text
    sample_text = """
    The plaintiff, John Doe, hereby files this complaint against the defendant, XYZ Corporation, 
    for breach of contract and negligence. The plaintiff alleges that on or about January 15, 2023, 
    the defendant entered into a written agreement with the plaintiff to provide consulting services. 
    The defendant failed to perform their obligations under said agreement, causing damages in the 
    amount of $500,000. The plaintiff seeks compensatory damages, legal fees, and any other relief 
    the court deems proper.
    """
    
    print("\nOriginal Text:")
    print("-" * 30)
    print(sample_text[:300] + "...")
    
    # Initialize BART summarizer
    print("\nLoading BART model (this may take a moment on first run)...")
    summarizer = BartSummarizer()
    
    # Generate summary
    print("\nGenerating summary...")
    summary = summarizer.summarize(sample_text)
    
    print("\nGenerated Summary:")
    print("-" * 30)
    print(summary)
    print("=" * 50)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Legal Document Summarizer')
    parser.add_argument('--mode', type=str, default='web',
                        choices=['web', 'test'],
                        help='Mode to run the application')
    
    args = parser.parse_args()
    
    if args.mode == 'web':
        print("Starting web application...")
        print("Open http://localhost:5000 in your browser")
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.mode == 'test':
        test_summarizer()

if __name__ == "__main__":
    main()