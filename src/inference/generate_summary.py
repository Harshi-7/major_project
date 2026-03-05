from src.models.bart_summarizer import BartSummarizer
from src.models.pegasus_summarizer import PegasusSummarizer
import pandas as pd
from src.utils.config import *
import os

class SummaryGenerator:
    def __init__(self, model_type='bart'):
        """
        Initialize summarizer
        model_type: 'bart' or 'pegasus'
        """
        self.model_type = model_type
        
        if model_type == 'bart':
            # Try to load fine-tuned model, fallback to pre-trained
            model_path = os.path.join(MODELS_DIR, 'bart_model', 'final')
            if os.path.exists(model_path):
                self.summarizer = BartSummarizer(model_path)
            else:
                self.summarizer = BartSummarizer()
        elif model_type == 'pegasus':
            self.summarizer = PegasusSummarizer()
        else:
            raise ValueError("model_type must be 'bart' or 'pegasus'")
    
    def summarize_text(self, text, **kwargs):
        """Summarize a single text"""
        return self.summarizer.summarize(text, **kwargs)
    
    def summarize_file(self, input_file, output_file=None, **kwargs):
        """Summarize texts from a file"""
        # Read input file
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
            texts = df['article'].tolist() if 'article' in df.columns else df.iloc[:, 0].tolist()
        elif input_file.endswith('.txt'):
            with open(input_file, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f.readlines() if line.strip()]
        else:
            raise ValueError("Unsupported file format. Use .csv or .txt")
        
        # Generate summaries
        print(f"Generating summaries for {len(texts)} texts...")
        summaries = self.summarizer.summarize_batch(texts, **kwargs)
        
        # Save results
        if output_file:
            result_df = pd.DataFrame({
                'original': texts,
                'summary': summaries
            })
            result_df.to_csv(output_file, index=False)
            print(f"Results saved to {output_file}")
        
        return summaries

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate summaries for legal documents')
    parser.add_argument('--model', type=str, default='bart', choices=['bart', 'pegasus'],
                        help='Model to use for summarization')
    parser.add_argument('--input', type=str, required=True,
                        help='Input file (txt or csv)')
    parser.add_argument('--output', type=str,
                        help='Output file (csv)')
    parser.add_argument('--max_length', type=int, default=150,
                        help='Maximum summary length')
    parser.add_argument('--min_length', type=int, default=40,
                        help='Minimum summary length')
    
    args = parser.parse_args()
    
    # Create generator
    generator = SummaryGenerator(model_type=args.model)
    
    # Generate summaries
    generator.summarize_file(
        args.input, 
        args.output,
        max_length=args.max_length,
        min_length=args.min_length
    )

if __name__ == "__main__":
    main()