from flask import Flask, request, jsonify, render_template, render_template_string
from src.utils import extract_text_from_pdf,convert_report_to_markdown
from flask_cors import CORS
from werkzeug.utils import secure_filename
import base64
from src.ai_utils import get_report_summary, get_sentence_explanation, generate_chatbot_response, generate_report_from_image
from src.utils import extract_text_from_pdf,convert_report_to_markdown


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# In-memory cache for sentence explanations
sentence_cache = {}
# API Routes
# API Routes
@app.route('/api/generate-summary', methods=['POST'])
def generate_summary_api():
    try:
        data = request.get_json()
        document_text = data.get('documentText', '')

        if not document_text:
            return jsonify({'error': 'No document text provided'}), 400

        # Call AI model
        ai_response = get_report_summary(document_text)

        return jsonify(ai_response)

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/explain-sentence', methods=['POST'])
def explain_sentence_api():
    try:
        data = request.get_json()
        sentence = data.get('sentence', '')
        context = data.get('context', 'Medical Document')

        if not sentence:
            return jsonify({'error': 'No sentence provided'}), 400

        # Clean the sentence to avoid encoding issues
        sentence = sentence.strip()

        # Check if we already have this explanation cached
        if sentence in sentence_cache:
            return jsonify({'explanation': sentence_cache[sentence]})

        # Call AI model
        explanation = get_sentence_explanation(sentence, context)

        # Cache the explanation
        sentence_cache[sentence] = explanation

        return jsonify({'explanation': explanation})

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


# File upload route
@app.route('/api/upload-document', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if file:
            filename = secure_filename(file.filename)
            file_extension = filename.lower().split('.')[-1] if '.' in filename else ''

            # Handle different file types
            if file_extension == 'pdf':
                content = extract_text_from_pdf(file)
                file_type = 'text'


            elif file_extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'dcm']:
                # Generate document from medical image
                file.seek(0)  # Reset file pointer
                content = generate_report_from_image(file)
                file_type = 'image'
                # Convert image to base64 for display
                file.seek(0)
                image_data = base64.b64encode(file.read()).decode('utf-8')
                image_url = f"data:image/{file_extension};base64,{image_data}"
            else:
                # Handle text files
                content = file.read().decode('utf-8', errors='ignore')
                file_type = 'text'

            # Convert to markdown for better display
            markdown_content = convert_report_to_markdown(content)

            response_data = {
                'filename': filename,
                'content': content,  # Original text for AI processing
                'markdown': markdown_content,  # Formatted markdown for display
                'file_type': file_type,  # Indicate if this was generated from image
                'message': 'File processed successfully'
            }

            # Add image data if it's an image file
            if file_type == 'image':
                response_data['image_url'] = image_url

            return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    try:
        data = request.get_json()

        message = data.get('message', '')
        context = data.get('context', {})  # Enhanced context with text and image
        chat_history = data.get('chat_history', [])

        # Extract context components
        document_text = context.get('document_text', '') if isinstance(context, dict) else context
        image_data = context.get('image_data') if isinstance(context, dict) else None
        has_image = context.get('has_image', False) if isinstance(context, dict) else False

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        response = generate_chatbot_response(message, document_text, image_data)

        return jsonify({
            'response': response,
            'context_used': bool(document_text) or bool(image_data),
            'has_text_context': bool(document_text),
            'has_image_context': bool(image_data),
            'model_used': 'mock_medical_multimodal_chatbot',
            'processing_time': '1.0s'
        })

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


# Cache status route for debugging
@app.route('/api/cache-status')
def cache_status():
    return jsonify({
        'cached_sentences': len(sentence_cache),
        'cache_keys': list(sentence_cache.keys())[:5]  # Show first 5 for debugging
    })

# Main route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print("🚀 Starting Medical AI Demo Server...")
    print("📋 This is a local development server")
    print("🤖 Using mock AI responses (replace with real OpenAI API)")
    print("-" * 50)

    app.run(host='127.0.0.1', port=5000, debug=True)

    print("-" * 50)
    print("📖 Instructions:")
    print("1. Open http://127.0.0.1:5000 in your browser")
    print("2. Click 'Analyze Report with AI'")
    print("3. Click on any sentence for explanations")
    print("4. Modify the code to add your OpenAI API key for real AI")