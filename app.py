from flask import Flask, render_template, request, send_file
import qrcode
import os
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_img_data = None
    if request.method == 'POST':
        link = request.form['link']
        if link:
            img = qrcode.make(link)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            qr_img_data = buffer.read().hex()
    return render_template('index.html', qr_img_data=qr_img_data)

@app.route('/download')
def download_qr():
    link = request.args.get('link')
    if not link:
        return "No link provided", 400
    img = qrcode.make(link)
    img_path = "static/qr_code.png"
    img.save(img_path)
    return send_file(img_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
