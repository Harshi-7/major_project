from flask import Blueprint, render_template, request, jsonify
from src.inference.generate_summary import SummaryGenerator
import os

# Create blueprint
main_bp = Blueprint('main', __name__)

# Initialize summarizer (lazy loading)
_summarizer = None

def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = SummaryGenerator(model_type='bart')
    return _summarizer

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/features')
def features():
    return render_template('features.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    text = data.get('text', '')
    model = data.get('model', 'bart')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        summarizer = get_summarizer()
        summary = summarizer.summarize_text(text)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model': 'bart'})