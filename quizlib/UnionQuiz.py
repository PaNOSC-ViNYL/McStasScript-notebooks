from .quiz import Quiz

class UnionQuiz(Quiz):
    def __init__(self):
        super().__init__()

    def question_1(self, answer):
        """
        Question: Will there be multiple scattering between sphere 1 and 2?
        A: 1 -> 2
        B: 2 -> 1
        C: Yes
        D: No
        """

        feedback = {"A": "The Union simulation engine will ensure multiple scattering both ways.",
                    "B": "The Union simulation engine will ensure multiple scattering both ways.",
                    "C": "All multiple scattering will be handled!",
                    "D": "The master will handle multiple scattering between the geometries."
                    }

        self.multiple_choice(answer=answer, correct_answer="C", feedback=feedback)