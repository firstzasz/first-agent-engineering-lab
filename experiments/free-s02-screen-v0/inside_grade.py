import json
import sys
import unittest
from pathlib import Path
sys.path[:0] = ['/work','/lab/experiments/relayboard/evaluator']
try:
    suite = unittest.TestLoader().discover('/work/tests', pattern='test_public.py')
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    import evaluator
    outcome = evaluator.evaluate_s02()
    print('GRADE_JSON:' + json.dumps({'public_pass': result.wasSuccessful(), 'public_tests': result.testsRun, 'frozen_oracle_pass': outcome.passed, 'frozen_oracle_failures': outcome.failures}))
except Exception as e:
    print('GRADE_JSON:' + json.dumps({'public_pass': False, 'frozen_oracle_pass': False, 'exception_type': type(e).__name__}))
