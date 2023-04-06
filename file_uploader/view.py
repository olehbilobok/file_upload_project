from flask import Flask, render_template, request, send_from_directory, jsonify
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    # Get the list of uploaded files
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'filenames': filenames})
    return render_template('index.html', filenames=filenames)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the uploaded file from the form data
    file = request.files['file']
    # Save the file to the server
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return '', 201


@app.route('/download/<filename>')
def download_file(filename):
    # Return the requested file to the user
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
