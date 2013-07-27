# Input: image with 1+ equations in it
# Output: list of strings representing the equations

from json import dumps
import tesseract
class ArithmeticPipeline:
    def handle(self, segs):
        api = tesseract.TessBaseAPI()
        api.Init(".","eng",tesseract.OEM_DEFAULT)
        api.SetVariable("tessedit_char_whitelist", "0123456789abcdefghijklmnopqrstuvwxyz+-/*.")
        api.SetPageSegMode(7)
       
        result = []
        for s in segs:
            img_buf = open(s, 'rb').read()
            result.append(tesseract.ProcessPagesBuffer(img_buf,len(img_buf),api).strip())
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
        Return a dictionary of opencv images
        img should be filename
        """

        # hardcoded for now
        result = {'arith': [img], 'mat': []}
        return result

