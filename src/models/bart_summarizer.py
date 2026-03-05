from transformers import BartForConditionalGeneration, BartTokenizer
import torch
from src.utils.config import BART_MODEL_NAME
import warnings
warnings.filterwarnings('ignore')

class BartSummarizer:
    def __init__(self, model_name=None):
        if model_name is None:
            model_name = BART_MODEL_NAME
        
        print(f"Loading BART model: {model_name}")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        try:
            # Load model and tokenizer
            self.tokenizer = BartTokenizer.from_pretrained(model_name)
            self.model = BartForConditionalGeneration.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            print(f"Model loaded successfully on {self.device}")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Please check your internet connection and try again.")
            raise
    
    def summarize(self, text, max_length=150, min_length=40, num_beams=4):
        """Generate summary for a single text"""
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text, 
                max_length=1024, 
                truncation=True, 
                return_tensors='pt'
            ).to(self.device)
            
            # Generate summary
            with torch.no_grad():
                summary_ids = self.model.generate(
                    inputs['input_ids'],
                    max_length=max_length,
                    min_length=min_length,
                    num_beams=num_beams,
                    early_stopping=True,
                    no_repeat_ngram_size=3
                )
            
            # Decode summary
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Error: {str(e)}"
    
    def summarize_batch(self, texts, batch_size=8, **kwargs):
        """Generate summaries for multiple texts"""
        summaries = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            
            try:
                # Tokenize batch
                inputs = self.tokenizer(
                    batch_texts,
                    max_length=1024,
                    truncation=True,
                    padding=True,
                    return_tensors='pt'
                ).to(self.device)
                
                # Generate summaries
                with torch.no_grad():
                    summary_ids = self.model.generate(
                        inputs['input_ids'],
                        **kwargs
                    )
                
                # Decode summaries
                batch_summaries = self.tokenizer.batch_decode(
                    summary_ids, 
                    skip_special_tokens=True
                )
                summaries.extend(batch_summaries)
            except Exception as e:
                print(f"Error processing batch {i}: {e}")
                summaries.extend([f"Error: {str(e)}"] * len(batch_texts))
        
        return summaries

if __name__ == "__main__":
    # Test the summarizer
    summarizer = BartSummarizer()
    test_text = "The United States Declaration of Independence was adopted by the Second Continental Congress on July 4, 1776, at Independence Hall in Philadelphia. The document announced that the thirteen American colonies then at war with Great Britain were now independent states, and thus no longer a part of the British Empire. Written primarily by Thomas Jefferson, the Declaration explains why the thirteen colonies regarded themselves as independent sovereign states no longer subject to British colonial rule."
    
    summary = summarizer.summarize(test_text)
    print(f"\nOriginal: {test_text[:200]}...")
    print(f"\nSummary: {summary}")