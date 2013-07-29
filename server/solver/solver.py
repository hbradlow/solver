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
        return None

    def _simple(self,s):
        try:
            return str(sympy.sympify(s))
        except:
            return None

    def solve(self,s):
        if len(s)<2:
            return None
        for char in s:
            if char not in NUMBERS and char not in OPERATIONS:
                return self._wolfram(s)
        if s[-1] in OPERATIONS:
            s = s[0:-1]
        if len(s)<2:
            return None
        return self._simple(s)
