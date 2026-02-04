from enum import Enum

class UserRole(str, Enum):
    hr = "hr"
    applicant = "applicant"

class JobSeniority(str, Enum):
    intern = "intern"
    junior = "junior"
    mid = "mid"
    senior = "senior"

class QuestionType(str, Enum):
    choose_one = "choose_one"
    choose_many = "choose_many"
    text_based = "text_based"

class SortByOptions(str, Enum):
    min = "min"
    max = "max"
    created_at = "created_at"