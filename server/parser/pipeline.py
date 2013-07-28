# Input: image with 1+ equations in it
# Output: list of strings representing the equations

from json import dumps
from subprocess import Popen
import subprocess
from parser.lines import cluster,matrix_cluster
from parser.cc import get_bounding_boxes
from parser.cropper import crop

class TesseractOperation:
    def run(self, filename, psm='7', charset='arith', clean=False):
        outfile = filename + '.txt'
        import os
        args = ('/usr/local/bin/tesseract', filename, filename, '-psm ' + psm, charset)
        os.system(" ".join(args))
        try:
            return open(outfile).read().strip()
        except:
            return ""

def ocr(segs):
    result = []
    for s in segs:
        text = self.tesser.run(s, '7', 'arith')
        result.append(text)
    return result

class Pipeline:

    def handle(self, img, kind='arith'):
        segs = self.segment(img)
        arith_segs = segs.get('arith')
        mat_segs = segs.get('mat')
        #print "SEGS",segs

        arith_segs, mat_segs = ocr(arith_segs), ocr(mat_segs)

        result = {'arith': arith_segs, 'mat': mat_segs}
        print "RESULT::::",result
        return result[kind]


    def segment(self, img): 
        """
        img should be filename
        """
        raw_boxes = get_bounding_boxes(img)
        matrix_clusters = matrix_cluster(raw_boxes)
        clusters = cluster(raw_boxes)
        matrix_images = crop(img,[c.bounding_box() for c in matrix_clusters])
        images = crop(img,[c.bounding_box() for c in clusters])

        result = {'arith': [images], 'mat': [matrix_images]}
        return result
