#!/usr/bin/env python3
"""Diagnostic test IDs only, no model keys or source content."""
import json
import sys
import unittest
sys.path.insert(0, "/work")
try:
    suite = unittest.TestLoader().discover("/work/tests", pattern="test_public.py")
    result = unittest.TestResult()
    suite.run(result)
    print("PUBLIC_DIAGNOSTIC:" + json.dumps({
        "tests":result.testsRun,
        "failures":[t.id() for t, _ in result.failures],
        "errors":[t.id() for t, _ in result.errors],
        "was_successful":result.wasSuccessful(),
    }))
except Exception as e:
    print("PUBLIC_DIAGNOSTIC:"+json.dumps({"exception_type":type(e).__name__}))
