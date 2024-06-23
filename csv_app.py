from flask import Flask, request, render_template, send_file, redirect, url_for
import pandas as pd
import os
from chinese_to_arabic import chinese_to_arabic, chinese_to_arabic_direct

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # 处理文件
        df = pd.read_csv(file_path, encoding='utf-8')
        df['生年'] = df['生年（大写）'].apply(chinese_to_arabic_direct)
        df['卒年'] = df['卒年（大写）'].apply(chinese_to_arabic_direct)
        df['享年'] = df['享年（大写）'].apply(chinese_to_arabic)

        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.csv')
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        return send_file(output_path, as_attachment=True, download_name='output.csv')


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, port=5001)

