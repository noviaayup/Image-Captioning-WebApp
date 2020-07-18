import os
import uuid
import requests
from whitenoise import WhiteNoise
from gtts import gTTS 


from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)

import run_script


UPLOAD_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = set(['jpg','jpeg','png'])
YANDEX_API_KEY = 'YOUR API KEY HERE'
SECRET_KEY = '7d441f27d441f27567d441f2b6176a'

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

# check if file extension is right
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# force browser to hold no cache. Otherwise old result returns.
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# main directory of programme
@app.route('/image-caption/', methods=['GET', 'POST'])
def upload_file():
    try:
        # remove files created more than 5 minute ago
        os.system("find static/images/ -maxdepth 1 -mmin +5 -type f -delete")
    except OSError:
        pass
    if request.method == 'POST':
        # check if the post request has the file part
        if 'content-file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        content_file = request.files['content-file']
        files = [content_file]
        # give unique name to each image
        content_name = str(uuid.uuid4()) + ".jpg"
        file_names = [content_name]
        for i, file in enumerate(files):
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_names[i]))
        
        # returns created caption
        args={
            'image' : UPLOAD_FOLDER + file_names[0],
        }
        caption = run_script.main(args)
        text=caption
        language='en'
        speech = gTTS(text = text, lang = language, slow = False)
        filesource='./static/text_save/'+file_names[0]+'text.mp3'
        speech.save(filesource)
        params={
            'imageact': '../static/images/' + file_names[0],
            'caption': caption,
            'soundit':'../static/text_save/'+file_names[0]+'text.mp3',
        } 

        return render_template('success.html', **params)
    return render_template('upload.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
    app.run(debug=False)
