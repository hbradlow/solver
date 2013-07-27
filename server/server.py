from flask import Flask
import flask
from flask import *
from flaskext.uploads import *
app = Flask(__name__)

@app.route('/solve',methods=['GET','POST','PUT'])
def upload():
    print request.__dict__
    if request.method == 'PUT' and 'photo' in request.files and False:
        filename = photos.save(request.files['photo'])
        rec = Photo(filename=filename, user=g.user.id)
        rec.store()
        flash("Photo saved.")
        return "Worked!",filename
    return "You uploaded a file!"

@app.route("/")
def hello():
        return "Solver!"

if __name__ == "__main__":
        app.run()
