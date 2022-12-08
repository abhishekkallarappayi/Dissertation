import os

from flask import Flask, flash, request, redirect, render_template

from werkzeug.utils import secure_filename

app=Flask(__name__,static_url_path="/static")

app.secret_key = "secret key"

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = "C:/Test/"

# file Upload

UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):

    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#HOMEPAGE

@app.route('/')

def homepage():

    return render_template('main.html')

#TUBERCULOSIS_PAGES

@app.route('/tuberculosis_upload')

def tuberculosis_upload_form():

    return render_template('tuberculosis_upload.html')



@app.route('/tuberculosis_normal')

def normal_tuberculosis():
    path = session.get('image_path',None)
    return render_template('tuberculosis_normal.html',image_path = path)


@app.route('/tuberculosis')

def tuberculosis_case():
    path = session.get('image_path',None)
    return render_template('tuberculosis.html',image_path = path)


#PNEUMONIA_PAGES

@app.route('/pneumonia_upload')

def pneumonia_upload_form():

    return render_template('pneumonia_upload.html')


@app.route('/pneumonia_normal')

def normal_pneumonia():
    path = session.get('image_path',None)
    return render_template('pneumonia_normal.html',image_path = path)

@app.route('/pneumonia')

def pneumonia_case():
    path = session.get('image_path',None)
    return render_template('pneumonia.html',image_path = path)




@app.route('/tuberculosis_upload', methods=['POST','GET'])

def upload_tuberculosis_file():

    if request.method == 'POST':

        # check if the post request has the file part

        if 'file' not in request.files:

            flash('No file part')

            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':

            flash('No file selected for uploading')

            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash('File successfully uploaded')
            print(img_path)
            src = img_path
            dst = os.path.join("C:/Test/static/", filename)
            session['image_path'] = filename

            shutil.copy2(src, dst)



            img = cv2.imread(str(img_path))
            img_backup=cv2.imread(str(img_path))
            img = cv2.resize(img, (28,28))

            if img.shape[2] ==1:
                img = np.dstack([img, img, img])

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img=np.array(img)
            img = img/255
            img=np.array(img)
            img =img.reshape(-1,28,28,3)
            print("Predicting....")
            pred_tub=tuberculosis_model.predict(img)
            print("Completed")

            if pred_tub>0.5:

                return redirect('/tuberculosis')
                print("Tuberculosis")
            else:
                return redirect('/tuberculosis_normal')
                print("normal")


            #return redirect('/normal')
        else:

            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')

            return redirect(request.url)



 #PNEUMONIA

@app.route('/pneumonia_upload', methods=['POST', 'GET'])
def upload_pneumonia_file():
    if request.method == 'POST':

        # check if the post request has the file part

        if 'file' not in request.files:
            flash('No file part')

            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No file selected for uploading')

            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash('File successfully uploaded')
            print(img_path)
            src = img_path
            dst = os.path.join("C:/Test/static/", filename)
            session['image_path'] = filename

            shutil.copy2(src, dst)

            img = cv2.imread(str(img_path))
            img_backup = cv2.imread(str(img_path))
            img = cv2.resize(img, (28, 28))

            if img.shape[2] == 1:
                img = np.dstack([img, img, img])

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = np.array(img)
            img = img / 255
            img = np.array(img)
            img = img.reshape(-1, 28, 28, 3)
            print("Predicting....")
            pred_pne = pneumonia_model.predict(img)
            print("Completed")

            if pred_pne > 0.5:

                return redirect('/pneumonia')
                print("Pneumonia")
            else:
                return redirect('/pneumonia_normal')
                print("normal")

            # return redirect('/normal')
        else:

            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')

            return redirect(request.url)

 

if __name__ == "__main__":
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    from flask import session,url_for
    from flask_session import Session
    import os
    from pathlib import Path
    import shutil

    from tensorflow import keras
    print("Loading Tuberculosis Model")
    tuberculosis_model = keras.models.load_model(r'C:\Test\templates\tuberculosis_model')
    print("Tuberculosis Model Loaded")

    print("Loading Pneumonia Model")
    pneumonia_model = keras.models.load_model(r'C:\Test\templates\pneumonia_model')
    print("Pneumonia Model Loaded")

    app.run(host = '127.0.0.1',port = 5000, debug = False)

 
