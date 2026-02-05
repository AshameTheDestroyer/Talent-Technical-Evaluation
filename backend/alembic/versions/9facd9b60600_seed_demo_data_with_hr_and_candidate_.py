"""Seed demo data with HR and candidate accounts

Revision ID: 9facd9b60600
Revises: 91905f51740d
Create Date: 2026-02-04 15:47:05.330740

"""
from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Boolean, Text
import json
from utils.password_utils import get_password_hash


# revision identifiers, used by Alembic.
revision: str = '9facd9b60600'
down_revision: Union[str, Sequence[str], None] = '91905f51740d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema with demo data."""
    # Create table objects for insertion
    users_table = table('users',
        column('id', String),
        column('first_name', String),
        column('last_name', String),
        column('email', String),
        column('password', String),
        column('role', String)
    )

    jobs_table = table('jobs',
        column('id', String),
        column('title', String),
        column('seniority', String),
        column('description', Text),
        column('skill_categories', String),
        column('active', Boolean)
    )

    assessments_table = table('assessments',
        column('id', String),
        column('job_id', String),
        column('title', String),
        column('duration', Integer),
        column('passing_score', Integer),
        column('questions', Text),
        column('active', Boolean)
    )

    # Hash the password for all users
    password_hash = get_password_hash("password123")

    # Insert HR users
    hr_users = [
        {
            'id': str(uuid.uuid4()),
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'email': 'sarah.johnson@demo.com',
            'password': password_hash,
            'role': 'hr'
        },
        {
            'id': str(uuid.uuid4()),
            'first_name': 'Michael',
            'last_name': 'Chen',
            'email': 'michael.chen@demo.com',
            'password': password_hash,
            'role': 'hr'
        },
        {
            'id': str(uuid.uuid4()),
            'first_name': 'Emma',
            'last_name': 'Rodriguez',
            'email': 'emma.rodriguez@demo.com',
            'password': password_hash,
            'role': 'hr'
        },
        {
            'id': str(uuid.uuid4()),
            'first_name': 'David',
            'last_name': 'Wilson',
            'email': 'david.wilson@demo.com',
            'password': password_hash,
            'role': 'hr'
        }
    ]

    # Insert candidate users
    candidate_users = [
        {
            'id': str(uuid.uuid4()),
            'first_name': 'Alex',
            'last_name': 'Thompson',
            'email': 'alex.thompson@demo.com',
            'password': password_hash,
            'role': 'applicant'
        },
        {
            'id': str(uuid.uuid4()),
            'first_name': 'Jessica',
            'last_name': 'Lee',
            'email': 'jessica.lee@demo.com',
            'password': password_hash,
            'role': 'applicant'
        },
        {
            'id': str(uuid.uuid4()),
            'first_name': 'Ryan',
            'last_name': 'Patel',
            'email': 'ryan.patel@demo.com',
            'password': password_hash,
            'role': 'applicant'
        },
        {
            'id': str(uuid.uuid4()),
            'first_name': 'Olivia',
            'last_name': 'Kim',
            'email': 'olivia.kim@demo.com',
            'password': password_hash,
            'role': 'applicant'
        }
    ]

    # Combine all users
    all_users = hr_users + candidate_users

    # Insert users
    op.bulk_insert(users_table, all_users)

    # Insert sample jobs
    jobs = [
        {
            'id': str(uuid.uuid4()),
            'title': 'Senior Python Developer',
            'seniority': 'senior',
            'description': 'We are looking for an experienced Python developer to join our team. The ideal candidate should have experience with web frameworks, databases, and cloud technologies.',
            'skill_categories': json.dumps(['python', 'django', 'flask', 'sql', 'cloud']),
            'active': True
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Junior Data Analyst',
            'seniority': 'junior',
            'description': 'We are looking for a Junior Data Analyst to join our analytics team. The ideal candidate should have experience with data visualization, statistical analysis, and SQL queries.',
            'skill_categories': json.dumps(['sql', 'python', 'excel', 'tableau', 'statistics']),
            'active': True
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Mid-Level Software Engineer',
            'seniority': 'mid',
            'description': 'We are looking for a Mid-Level Software Engineer with experience in Python, Django, and REST APIs.',
            'skill_categories': json.dumps(['python', 'django', 'rest-api', 'sql', 'testing']),
            'active': True
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'DevOps Engineer',
            'seniority': 'mid',
            'description': 'We are looking for a DevOps Engineer to help us improve our CI/CD pipelines and infrastructure automation.',
            'skill_categories': json.dumps(['docker', 'kubernetes', 'aws', 'jenkins', 'terraform']),
            'active': True
        }
    ]

    # Insert jobs
    op.bulk_insert(jobs_table, jobs)

    # Create a mapping of job titles to IDs for assessment creation
    job_mapping = {job['title']: job['id'] for job in jobs}

    # Create sample assessments with questions
    assessments = []

    # Python Developer Assessment
    python_questions = [
        {
            "id": str(uuid.uuid4()),
            "text": "What is the difference between a list and a tuple in Python?",
            "weight": 3,
            "skill_categories": ["python"],
            "type": "text_based",
            "options": [],
            "correct_options": []
        },
        {
            "id": str(uuid.uuid4()),
            "text": "Which of the following is a mutable data type in Python?",
            "weight": 2,
            "skill_categories": ["python"],
            "type": "choose_one",
            "options": [
                {"text": "Tuple", "value": "a"},
                {"text": "String", "value": "b"},
                {"text": "List", "value": "c"},
                {"text": "Integer", "value": "d"}
            ],
            "correct_options": ["c"]
        },
        {
            "id": str(uuid.uuid4()),
            "text": "Which of the following are Python web frameworks?",
            "weight": 3,
            "skill_categories": ["python", "web-development"],
            "type": "choose_many",
            "options": [
                {"text": "Django", "value": "a"},
                {"text": "Express", "value": "b"},
                {"text": "Flask", "value": "c"},
                {"text": "Spring", "value": "d"}
            ],
            "correct_options": ["a", "c"]
        }
    ]

    assessments.append({
        'id': str(uuid.uuid4()),
        'job_id': job_mapping['Senior Python Developer'],
        'title': 'Python Programming Skills Assessment',
        'duration': 1800,  # 30 minutes
        'passing_score': 70,
        'questions': json.dumps(python_questions),
        'active': True
    })

    # Data Analyst Assessment
    data_analyst_questions = [
        {
            "id": str(uuid.uuid4()),
            "text": "What is the purpose of GROUP BY clause in SQL?",
            "weight": 3,
            "skill_categories": ["sql"],
            "type": "text_based",
            "options": [],
            "correct_options": []
        },
        {
            "id": str(uuid.uuid4()),
            "text": "Which of the following are data visualization tools?",
            "weight": 2,
            "skill_categories": ["data-visualization"],
            "type": "choose_many",
            "options": [
                {"text": "Tableau", "value": "a"},
                {"text": "Power BI", "value": "b"},
                {"text": "Excel", "value": "c"},
                {"text": "Notepad", "value": "d"}
            ],
            "correct_options": ["a", "b", "c"]
        },
        {
            "id": str(uuid.uuid4()),
            "text": "What does the acronym ETL stand for?",
            "weight": 2,
            "skill_categories": ["data-processing"],
            "type": "choose_one",
            "options": [
                {"text": "Extract, Transform, Load", "value": "a"},
                {"text": "Edit, Transfer, Link", "value": "b"},
                {"text": "Encode, Transmit, Log", "value": "c"},
                {"text": "Estimate, Test, Learn", "value": "d"}
            ],
            "correct_options": ["a"]
        }
    ]

    assessments.append({
        'id': str(uuid.uuid4()),
        'job_id': job_mapping['Junior Data Analyst'],
        'title': 'Data Analysis Skills Assessment',
        'duration': 2400,  # 40 minutes
        'passing_score': 65,
        'questions': json.dumps(data_analyst_questions),
        'active': True
    })

    # Software Engineer Assessment
    software_eng_questions = [
        {
            "id": str(uuid.uuid4()),
            "text": "Explain the difference between REST and GraphQL APIs.",
            "weight": 4,
            "skill_categories": ["api-design"],
            "type": "text_based",
            "options": [],
            "correct_options": []
        },
        {
            "id": str(uuid.uuid4()),
            "text": "Which HTTP status code indicates a successful request?",
            "weight": 1,
            "skill_categories": ["web-development"],
            "type": "choose_one",
            "options": [
                {"text": "200", "value": "a"},
                {"text": "404", "value": "b"},
                {"text": "500", "value": "c"},
                {"text": "301", "value": "d"}
            ],
            "correct_options": ["a"]
        },
        {
            "id": str(uuid.uuid4()),
            "text": "Which of the following are version control systems?",
            "weight": 2,
            "skill_categories": ["development-tools"],
            "type": "choose_many",
            "options": [
                {"text": "Git", "value": "a"},
                {"text": "SVN", "value": "b"},
                {"text": "Mercurial", "value": "c"},
                {"text": "Docker", "value": "d"}
            ],
            "correct_options": ["a", "b", "c"]
        }
    ]

    assessments.append({
        'id': str(uuid.uuid4()),
        'job_id': job_mapping['Mid-Level Software Engineer'],
        'title': 'Software Engineering Fundamentals Assessment',
        'duration': 1800,  # 30 minutes
        'passing_score': 75,
        'questions': json.dumps(software_eng_questions),
        'active': True
    })

    # DevOps Assessment
    devops_questions = [
        {
            "id": str(uuid.uuid4()),
            "text": "What is the main purpose of Docker containers?",
            "weight": 3,
            "skill_categories": ["containerization"],
            "type": "text_based",
            "options": [],
            "correct_options": []
        },
        {
            "id": str(uuid.uuid4()),
            "text": "Which of the following are container orchestration platforms?",
            "weight": 3,
            "skill_categories": ["orchestration"],
            "type": "choose_many",
            "options": [
                {"text": "Kubernetes", "value": "a"},
                {"text": "Docker Swarm", "value": "b"},
                {"text": "Apache Mesos", "value": "c"},
                {"text": "Jenkins", "value": "d"}
            ],
            "correct_options": ["a", "b", "c"]
        },
        {
            "id": str(uuid.uuid4()),
            "text": "What does CI/CD stand for?",
            "weight": 1,
            "skill_categories": ["development-process"],
            "type": "choose_one",
            "options": [
                {"text": "Continuous Integration/Continuous Deployment", "value": "a"},
                {"text": "Computer Integrated Design", "value": "b"},
                {"text": "Customer Identity and Data", "value": "c"},
                {"text": "Cloud Infrastructure Development", "value": "d"}
            ],
            "correct_options": ["a"]
        }
    ]

    assessments.append({
        'id': str(uuid.uuid4()),
        'job_id': job_mapping['DevOps Engineer'],
        'title': 'DevOps Practices Assessment',
        'duration': 2100,  # 35 minutes
        'passing_score': 70,
        'questions': json.dumps(devops_questions),
        'active': True
    })

    # Insert assessments
    op.bulk_insert(assessments_table, assessments)


def downgrade() -> None:
    """Downgrade schema - remove demo data."""
    # Delete all records from the tables
    op.execute("DELETE FROM applications")
    op.execute("DELETE FROM assessments")
    op.execute("DELETE FROM jobs")
    op.execute("DELETE FROM users")
