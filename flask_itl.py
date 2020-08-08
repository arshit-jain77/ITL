import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, send_from_directory
import base64
from werkzeug import secure_filename, SharedDataMiddleware

UPLOADER_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg','jpeg','png'])

def get_as_base64(url):
    return base64.b64encode(request.get(url).content)

app = Flask(__name__)
app.config['UPLOADER_FOLDER'] = UPLOADER_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/itl'
db = SQLAlchemy(app)


@app.route("/")
def signin():
    return render_template('signin.html')

# code to check the email and password of the person signing in from the database.
@app.route("/mainpage_signin.html", methods=['GET','POST'])
def mainpage_signin():
    if request.method=='POST':
        email = request.form.get('email')
        psswd = request.form.get('psswd')
        connection = pymysql.connect(host='localhost', user='root', password='', db='itl')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM `signup` WHERE Email='"+email+"'")
            results=cursor.fetchall()
            if results[0][4]==email and results[0][5]==psswd:
                return render_template('mainpage_signin.html')
            else:
                error = 'Invalid Password/Email. Please enter the details again.'
                return render_template('signin.html', error=error)



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADER_FOLDER'],
                               filename)


app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': app.config['UPLOADER_FOLDER']
})

if __name__ == "__main__":
    app.debug = False
    app.run()







