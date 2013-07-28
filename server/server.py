from flask import Flask
import flask
from flask import *
from flaskext.uploads import *
import IPython
app = Flask(__name__)

from parser.pipeline import  *
from solver.solver import Solver

solver = Solver()

@app.route('/custom',methods=['GET','POST','PUT'])
def custom():
    try:
        if request.method == 'POST' and 'query' in request.values:
            q = request.values['query']
            a = solver._wolfram(q)
            obj = {'response':[{'problem':q,'steps':['something'],'solution':str(a)}]}
            print obj
            return flask.jsonify(obj)
    except Exception as e:
        IPython.embed()
        print "Fail"
        return "Invalid query"


@app.route('/matrix',methods=['GET','POST','PUT'])
def matrix():
    if request.method == 'POST' and 'photo' in request.files:
        try:
            extension = request.files['photo'].filename.split(".")[-1]
            path = "tmp/tmp."+extension
            request.files['photo'].save(path)


            s = handle_matrix(path)['arith']
            
            m = []
            for i,row in enumerate(s):
                l = []
                for j,col in enumerate(row):
                    new_s = col.replace(".","").replace("-","").strip()
                    if not new_s:
                        pass
                    else:
                        try:
                            l.append(int(new_s))
                        except:
                            pass
                if l:
                    m.append(l)

            print m


            a = solver._wolfram("det " + str(m))
            obj = {'response':[{'problem':"Det("+str(m)+")",'steps':['something'],'solution':str(a)}]}
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
            m = []
            for i in s:
                new_i = i.replace(".","").strip()
                if new_i:
                    m.append(new_i)

            a = solver._wolfram("solve " + ", ".join(m))
            obj = {'response':[{'problem':"solve " + ", ".join(m),'steps':['something'],'solution':str(a)}]}
            return flask.jsonify(obj)
        except Exception as e:
            print e
            IPython.embed()

    return "You uploaded a file!"

@app.route('/solve',methods=['GET','POST','PUT'])
def solve():
    print "In solve"
    if request.method == 'POST' and 'photo' in request.files:
        try:
            extension = request.files['photo'].filename.split(".")[-1]
            path = "tmp/tmp."+extension
            request.files['photo'].save(path)


            s = handle_simple(path)['arith']

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
                if s:
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
