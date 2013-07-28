from flask import Flask
import flask
from flask import *
from flaskext.uploads import *
import IPython
app = Flask(__name__)

from parser.pipeline import  Pipeline
from solver.solver import Solver

@app.route('/solve',methods=['GET','POST','PUT'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        extension = request.files['photo'].filename.split(".")[-1]
        path = "tmp/tmp."+extension
        request.files['photo'].save(path)


        p = Pipeline()
        s = p.handle(path)['arith'][0]
        solver = Solver()
        solution = solver.solve(s)

        return flask.jsonify({'response':[{'problem':s,'steps':['something'],'solution':solution}]})

    return "You uploaded a file!"

@app.route("/")
def hello():
        return "Solver!"

if __name__ == "__main__":
    app.run(host='172.16.240.220')
