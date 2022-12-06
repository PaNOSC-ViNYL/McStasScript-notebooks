import sys
import os

# Find path where quizlib is loaded from
day_path = os.path.dirname(os.path.realpath(__file__))
days_path = os.path.dirname(day_path)
notebook_path = os.path.dirname(days_path)

# Add to path if not present
if notebook_path not in sys.path:
    sys.path.insert(0, notebook_path)

# Now we can import quizlib
import quizlib

# Return the appropriate Quiz to the caller
def exercise_1():
    return quizlib.McStasScriptQuiz()

def exercise_2():
    return quizlib.DiagnosticsQuiz()