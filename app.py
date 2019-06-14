# Cleo

# THE MAIN FILE

# IMPORT
import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

# IMPORT OTHER PYTHON FILES
from scripts.matrix import *
from scripts.matrix_reorder import *
from scripts.Node import *
from scripts.Node_Bundle import *

# UPLOAD FOLDER
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
ALLOWED_EXTENSIONS = {'csv', 'txt'}

# SET FLASK APP
app = Flask(__name__)

# PATH NAME
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# SET FILENAME
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# UPLOAD A FILE
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filename = request.form.get('myselect')
        return redirect(url_for('uploaded_file', filename=filename))

        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # SET FILEPATH
    myPath = "uploads/"+filename

    # MATRIX
    func = matrix_tab(myPath)
    script, div = components(func)

    # MATRIX REORDER
    func2 = matrix_reorder_tab(myPath)
    script2, div2 = components(func2)

    # NODE LINK
    func3 = node_tab(myPath)
    script3, div3 = components(func3)

    # NODE BUNDLE
    func4 = node_bundle_tab(myPath)
    script4, div4 = components(func4)

    # SEND SCRIPTS AND DIVS TO TEMPLATE HTML
    return render_template('upload.html',  script=script, div=div, script2=script2, div2=div2, script3=script3, div3=div3, script4=script4, div4=div4)

# RUN
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)