# Input: image with 1+ equations in it
# Output: list of strings representing the equations

from json import dumps
from subprocess import Popen
import subprocess
from lines import cluster
from cc import get_bounding_boxes
from cropper import crop

class TesseractOperation:
    def run(self, filename, psm='10', charset='arith', clean=False):
        psm = "7"
        charset = 'arith'

        outfile = filename + '.txt'
        import os
        args = ('/usr/local/bin/tesseract', filename, filename, '-psm ' + psm, charset)
        os.system(" ".join(args))
        try:
            return open(outfile).read().strip()
        except:
            return ""


class ArithmeticPipeline:
    tesser = TesseractOperation()

    def handle(self, segs):
          
        result = []
        for s in segs:
            text = self.tesser.run(s, '7', 'arith')
            result.append(text)

        return result


class MatrixPipeline:
    def handel(self, segs):
        return []


class Pipeline:
    pipeline_stages = {'arith': [ArithmeticPipeline()], 'mat': [None]}

    def handle(self, img):
        segs = self.segment(img)
        arith_segs = segs.get('arith')
        mat_segs = segs.get('mat')
        #print "SEGS",segs

        for arith_stage, mat_stage in zip(Pipeline.pipeline_stages['arith'], Pipeline.pipeline_stages['mat']):
            arith_segs, mat_segs = arith_stage.handle(arith_segs), arith_stage.handle(mat_segs)

        result = {'arith': arith_segs, 'mat': mat_segs}
        
        return result


    def segment(self, img):
        """
        img should be filename
        """

        raw_boxes = get_bounding_boxes(img)
        clusters = cluster(raw_boxes)
        images = crop(img,[c.bounding_box() for c in clusters])

        result = {'arith': images, 'mat': []}
        return result
