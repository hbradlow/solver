# Input: image with 1+ equations in it
# Output: list of strings representing the equations

from json import dumps
from subprocess import Popen
from parser.lines import cluster

class TesseractOperation:
    def run(self, filename, psm='7', charset='math', clean=False):
        outfile = filename + '.txt'
        args = ('tesseract', filename, filename, '-psm ' + psm, charset)
        print ' '.join(args)
        proc = Popen(args)
        retcode = proc.wait()
        if retcode != 0:
            print 'tesseract had an error'
            return None
        result = ''
        with open(outfile, 'rb') as f:
            result = f.read().strip()
        if clean:
            args = ('rm', outfile)
            proc= Popen(args)

        print 'output file to', outfile
        print 'result', result
        return result


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
        images = croped_images(img,[c.bounding_box() for c in cluster_boxes])
        result = {'arith': images, 'mat': []}
        return result

