from flask import Flask
import flask
from flask import *
from flaskext.uploads import *
import IPython
app = Flask(__name__)

from parser.pipeline import  Pipeline
from solver.solver import Solver

@app.route('/matrix',methods=['GET','POST','PUT'])
def matrix():
    if request.method == 'POST' and 'photo' in request.files:
        try:
            extension = request.files['photo'].filename.split(".")[-1]
            path = "tmp/tmp."+extension
            request.files['photo'].save(path)


            p = Pipeline()
            s = p.handle(path)['arith']

            print s
            solver = Solver()
            m = []
            for i in s:
                i = i.replace(" ","")
                i = i.replace("-","")
                i = i.replace("+","")
                if not i.strip():
                    continue
                m.append([int(a) for a in list(i)])
            print m

            """
            ans = solver.solve("rref " + str(m))
            ans = ans.replace("(","")
            ans = ans.replace(")","")
            a = []
            for thing in ans.split("\n"):
                t = []
                for b in thing.split("|"):
                    t.append(int(b.strip()))
                a.append(t)
            """
            a = solver.solve("det " + str(m))
            obj = {'response':[{'problem':str(m),'steps':['something'],'solution':str(a)}]}
            return flask.jsonify(obj)
        except Exception as e:
            print e
            IPython.embed()

    return "You uploaded a file!"

@app.route('/solve',methods=['GET','POST','PUT'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        try:
            extension = request.files['photo'].filename.split(".")[-1]
            path = "tmp/tmp."+extension
            request.files['photo'].save(path)


            p = Pipeline()
            s = p.handle(path)['arith']
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
