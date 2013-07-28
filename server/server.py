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
        try:
            extension = request.files['photo'].filename.split(".")[-1]
            path = "tmp/tmp."+extension
            request.files['photo'].save(path)

            #return flask.jsonify({'response':[{'problem':"3x+4=10",'steps':['something'],'solution':"x = 2"}]})

            p = Pipeline()
            s = p.handle(path)['arith']
            print "S:",s
            solver = Solver()
            solutions = []
            problems = []
            for i in s:
                sol = solver.solve(i)
                if sol:
                    problems.append(i)
                    solutions.append(sol)
        
            print solutions
            obj = {'response':[]}
            for p,s in zip(problems,solutions):
                obj['response'].append({'problem':p,'steps':['something'],'solution':s})
            return flask.jsonify(obj)
        except Exception as e:
            print e
            IPython.embed()

    return "You uploaded a file!"

@app.route("/")
def hello():
        return "Solver!"

if __name__ == "__main__":
    app.run(host='172.16.240.220')
