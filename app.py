from flask import Flask, request, jsonify, send_file
import requests
from PIL import Image
import io

app = Flask(__name__)

# Define model API URLs
model_urls = [
    "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev",
    "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
    "https://api-inference.huggingface.co/models/stabilityai/sdxl-turbo",
    "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
]

headers = {"Authorization": "Bearer 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"}

def query(api_url, payload):
    response = requests.post(api_url, headers=headers, json=payload)
    return response.content, response.status_code

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    prompt = request.form.get('prompt')
    
    payload = {
        "inputs": prompt,
    }

    for api_url in model_urls:
        image_bytes, status_code = query(api_url, payload)
        
        if status_code == 200:
            try:
                image = Image.open(io.BytesIO(image_bytes))
                image.save('generated_image.jpeg')  # Save the image to a file
                return send_file('generated_image.jpeg', mimetype='image/jpeg')
            except Exception as e:
                return jsonify({"error": f"Image processing error: {str(e)}"}), 500
        else:
            print(f"Model at {api_url} failed with status code {status_code}. Trying next model...")

    return jsonify({"error": "All models failed to generate an image."}), 500

if __name__ == '__main__':
    app.run(debug=True)