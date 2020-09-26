import time
import unittest, os,app
from lib.HTMLTestRunner_PY3 import  HTMLTestRunner

suite = unittest.defaultTestLoader.discover('./scripts',pattern='test0*.py')

report_path = app.DIR_NAME+os.sep+'report'+os.sep+'report{}.html'.format(int(time.time()*1000))
with open(report_path,'wb')as f:
    HTMLTestRunner(stream=f).run(suite)



