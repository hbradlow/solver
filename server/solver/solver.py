import sympy
import wolframalpha
import IPython

NUMBERS = "1234567890"
OPERATIONS = "=-+*%/"

class Solver:

    def __init__(self):
        self.wolfram_client = wolframalpha.Client("XR8XP2-WXKLU74A3E")

    def _wolfram(self,s):
        res = self.wolfram_client.query(s)
        for r in res:
            title = r.node.attrib['title']
            if title in ["Solution","Result","Derivative"]:
                return r.node._children[0]._children[0].text
        return "Unknown problem type."

    def _simple(self,s):
        return str(sympy.sympify(s))

    def solve(self,s):
        for char in s:
            if char not in NUMBERS and char not in OPERATIONS:
                return self._wolfram(s)
        return self._simple(s)
