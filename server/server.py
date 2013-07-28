from flask import Flask
import flask
from flask import *
from flaskext.uploads import *
import IPython
app = Flask(__name__)

#from parser.parse import parse
from solver.solver import Solver

@app.route('/solve',methods=['GET','POST','PUT'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        extension = request.files['photo'].filename.split(".")[-1]
        path = "tmp/tmp."+extension
        request.files['photo'].save(path)
        return flask.jsonify({'response':[{'problem':'3x+4=10','steps':['something'],'solution':'x = 2'}]})

        s = parse(path)
        solver = Solver()
        return solver.solve(s)

    return "You uploaded a file!"

@app.route("/")
def hello():
        return "Solver!"

if __name__ == "__main__":
    app.run(host='172.16.240.220')
