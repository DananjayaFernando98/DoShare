from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_list = []
    for file_name in files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        size = os.path.getsize(file_path)
        file_list.append({'filename': file_name, 'size': size})
    return render_template('index.html', files=file_list)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('file')
    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return jsonify({'error': 'File type not allowed'}), 400
    
    return jsonify({'message': 'File(s) uploaded successfully'}), 201

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'success': True, 'message': f'File {filename} deleted successfully'}), 200
    else:
        return jsonify({'success': False, 'error': f'File {filename} not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
