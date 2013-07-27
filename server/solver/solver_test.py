from solver.solver import solve

def test_solve():
    if solve("1+5")!="0":
        print "Fail"
    else:
        print "Succeed"
