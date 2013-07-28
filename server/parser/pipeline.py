# Input: image with 1+ equations in it
# Output: list of strings representing the equations

from json import dumps
from subprocess import Popen
import subprocess
from parser.lines import cluster,matrix_cluster
from parser.cc import get_bounding_boxes
from parser.cropper import crop

class TesseractOperation:
    def run(self, filename, psm='7', charset='arith', clean=True):
        charset = 'math'
        outfile = filename + '.txt'
        import os
        args = ('/usr/local/bin/tesseract', filename, filename, '-psm ' + psm, charset)
        os.system(" ".join(args))
        try:
            return open(outfile).read().strip()
        except:
            return ""


class MatrixPipeline:
    tesser = TesseractOperation()

    def handle(self, segs):
        result = []
        for l in segs:
            res = []
            for s in l:
                text = self.tesser.run(s, '7', 'arith')
                res.append(text)
            result.append(res)
        return result

class ArithmeticPipeline:
    tesser = TesseractOperation()

    def handle(self, segs):
        result = []
        for s in segs:
            text = self.tesser.run(s, '7', 'arith')
            result.append(text)
        return result


def handle_simple(img):
    def segment(img):
        """
        img should be filename
        """

        raw_boxes = get_bounding_boxes(img)
        clusters = cluster(raw_boxes)
        total = []
        index = 0
        total,index = crop(img,[c.bounding_box() for c in clusters],index)

        result = {'arith': total, 'mat': []}
        return result

    segs = segment(img)
    arith_segs = segs.get('arith')
    mat_segs = segs.get('mat')

    arith_segs, mat_segs = ArithmeticPipeline().handle(arith_segs), ArithmeticPipeline().handle(mat_segs)

    result = {'arith': arith_segs, 'mat': mat_segs}
    
    return result



def handle_matrix(img):
    def segment(img):
        """
        img should be filename
        """

        raw_boxes = get_bounding_boxes(img)
        clusters = matrix_cluster(raw_boxes)
        total = []
        index = 0
        for row in clusters:
            images,index = crop(img,[c.bounding_box() for c in row],index)
            total.append(images)

        result = {'arith': total, 'mat': []}
        return result
    segs = segment(img)
    arith_segs = segs.get('arith')
    mat_segs = segs.get('mat')

    arith_segs, mat_segs = MatrixPipeline().handle(arith_segs), MatrixPipeline().handle(mat_segs)

    result = {'arith': arith_segs, 'mat': mat_segs}
    
    return result


