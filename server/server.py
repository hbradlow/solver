from flask import Flask
import flask
from flask import *
from flaskext.uploads import *
import IPython
app = Flask(__name__)

from parser.pipeline import  *
from solver.solver import Solver

@app.route('/matrix',methods=['GET','POST','PUT'])
def matrix():
    if request.method == 'POST' and 'photo' in request.files:
        try:
            extension = request.files['photo'].filename.split(".")[-1]
            path = "tmp/tmp."+extension
            request.files['photo'].save(path)


            s = handle_matrix(path)['arith']
            print s
            solver = Solver()
            
            m = []
            for i,row in enumerate(s):
                l = []
                for j,col in enumerate(row):
                    new_s = col.replace(".","").replace("-","").strip()
                    if not new_s:
                        l.append(0)
                    else:
                        l.append(int(new_s))
                m.append(l)


            a = solver.solve("det " + str(m))
            obj = {'response':[{'problem':str(m),'steps':['something'],'solution':str(a)}]}
            return flask.jsonify(obj)
        except Exception as e:
            print e
            IPython.embed()

    return "You uploaded a file!"

@app.route('/system',methods=['GET','POST','PUT'])
def system():
    if request.method == 'POST' and 'photo' in request.files:
        try:
            extension = request.files['photo'].filename.split(".")[-1]
            path = "tmp/tmp."+extension
            request.files['photo'].save(path)


            s = handle_simple(path)['arith']
            solver = Solver()

            a = solver.solve("solve " + ", ".join(s))
            obj = {'response':[{'problem':str(m),'steps':['something'],'solution':str(a)}]}
            return flask.jsonify(obj)
        except Exception as e:
            print e
            IPython.embed()

    return "You uploaded a file!"

@app.route('/solve',methods=['GET','POST','PUT'])
def solve():
    if request.method == 'POST' and 'photo' in request.files:
        try:
            extension = request.files['photo'].filename.split(".")[-1]
            path = "tmp/tmp."+extension
            request.files['photo'].save(path)


            s = handle_simple(path)['arith']
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
