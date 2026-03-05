from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
from src.utils.config import PEGASUS_MODEL_NAME

class PegasusSummarizer:
    def __init__(self, model_name=PEGASUS_MODEL_NAME):
        print(f"Loading PEGASUS model: {model_name}")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load model and tokenizer
        self.tokenizer = PegasusTokenizer.from_pretrained(model_name)
        self.model = PegasusForConditionalGeneration.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()
        print(f"Model loaded on {self.device}")
    
    def summarize(self, text, max_length=150, min_length=40, num_beams=4):
        """Generate summary for a single text"""
        # Tokenize input
        inputs = self.tokenizer(
            text, 
            max_length=1024, 
            truncation=True, 
            return_tensors='pt'
        ).to(self.device)
        
        # Generate summary
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
    
    def summarize_batch(self, texts, batch_size=8, **kwargs):
        """Generate summaries for multiple texts"""
        summaries = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            
            # Tokenize batch
            inputs = self.tokenizer(
                batch_texts,
                max_length=1024,
                truncation=True,
                padding=True,
                return_tensors='pt'
            ).to(self.device)
            
            # Generate summaries
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
        
        return summaries

if __name__ == "__main__":
    # Test the summarizer
    summarizer = PegasusSummarizer()
    test_text = "The United States Declaration of Independence was adopted by the Second Continental Congress on July 4, 1776, at Independence Hall in Philadelphia. The document announced that the thirteen American colonies then at war with Great Britain were now independent states, and thus no longer a part of the British Empire. Written primarily by Thomas Jefferson, the Declaration explains why the thirteen colonies regarded themselves as independent sovereign states no longer subject to British colonial rule."
    
    summary = summarizer.summarize(test_text)
    print(f"Original: {test_text[:200]}...")
    print(f"Summary: {summary}")