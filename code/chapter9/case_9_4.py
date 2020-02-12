# -*- coding: utf-8 -*-
"""this is a example for chapter 9 """
class FEMError(StandardError):
    FEMErrorNum = 0
    def __init__(self, FEMError_name=None, FEMError_message=None):
        self.FEMError_name = FEMError_name
        FEMError.FEMErrorNum = FEMError.FEMErrorNum + 1
        self.FEMError_message = FEMError_message
    def __str__(self):
        if self.FEMError_message!=None and self.FEMError_name!=None:
            temp = '[FEMEno'+str(FEMError.FEMErrorNum)+'] ' + \
                self.FEMError_message + ' in: ' + self.FEMError_name
        else:
            temp = ''
        return temp
if __name__=='__main__':
    myError = FEMError('wireDrawing', 'Boundary conflict detected!')
    print myError