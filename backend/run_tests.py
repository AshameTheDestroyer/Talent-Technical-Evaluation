"""
Test Runner for AI-Powered Hiring Assessment Platform
This script runs all tests in the test suite.
"""

import unittest
import sys
import os

# Add the backend directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def run_tests():
    """Run all tests in the test suite."""
    print("Running comprehensive test suite for AI-Powered Hiring Assessment Platform...")
    
    # Discover and run all tests in the tests directory
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)