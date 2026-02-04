1. System Requirements — MVP for AI-Powered Hiring Assessment Platform
1.1 Overview
A platform for managing hiring assessments using AI, serving two primary user types: 1. HR (Human Resources) 2. Candidate
Goal: Enable HR to create smart assessments, manage them, and review results easily, while allowing candidates to take assessments and review their results.
1.2 Primary Users
1.2.1 HR
A user responsible for creating and managing assessments, questions, and reviewing candidate results.
1.2.2 Candidate
A user who takes assessments and reviews their previous results.
2. Functional Requirements — HR
2.1 Authentication and Account Management
•	HR login using email and password.
2.2 Job Roles and Assessment Management
•	Create a new assessment.
•	Enter assessment information:
1.	Job Title
2.	Experience Level
3.	Required Skills
4.	Job Description
5.	Number of Questions
6.	Assessment Description (optional) to be displayed to the candidate
2.3 Creating Questions Using AI
•	Create questions through AI chat based on job information.
•	Save questions in a question bank linked to the assessment.
•	Edit questions manually.
•	Edit a question using AI (rewording, difficulty adjustment, clarity improvement).
2.4 Managing Question Properties
•	Mark a question as:
1.	Failing Question / Knockout
•	Add tags to questions to be used as evaluation criteria (e.g., Python, Communication, SQL).
•	Set weight or importance for each question.
2.5 Assessment Evaluation and Review
•	Display assessment results in a table containing:
1.	Candidate Name
2.	Assessment Date
3.	Time Taken to Complete
4.	Final Numeric Score
5.	Pass/Fail status based on:
	Required level
	Knockout questions
6.	Candidate score per tag (Tag-based Scores)
•	Review a specific candidate’s answers for each question.
•	Display a summary view:
1.	Average Scores
2.	Pass Rate
3.	Key Strengths and Weaknesses (from AI)
•	Set a score/rating for each question manually or with AI assistance.
2.6 Retrieving and Managing Assessments
•	Retrieve specific assessment information (questions, settings, results).
•	HR can edit any question and use AI for assistance.
2.7 Sharing Assessments
•	Generate a unique link for the assessment.
•	Enable/disable the assessment link.
3. Functional Requirements — Candidate
3.1 Authentication and Account Management
•	Candidate login (email + password).
3.2 Taking the Assessment
•	Access the assessment via link.
•	Display assessment instructions.
•	Answer the questions.
•	Submit the assessment upon completion.
3.3 Reviewing Results
•	Display previous assessment results.
•	Show overall score.
•	Display general feedback (optional).
4. Evaluation
•	Each question has a maximum score.
•	Questions can be marked as Knockout.
•	For Knockout questions:
1.	Candidate must achieve ≥ 50% of the question score to pass the assessment.
•	Final score = sum of all question scores.
4.1 AI Evaluation
•	The system sends candidate answers to AI for evaluation.
•	AI returns:
1.	Suggested score for each question.
2.	Brief rationale/feedback (optional in MVP).
•	HR can:
1.	Modify any question score.
2.	Accept or ignore AI evaluation.
4.2 Language
•	The system interface and questions are in English only.
4.3 Single HR
•	Only one HR exists (no multi-company or multi-HR support in MVP).
5. MVP Core Requirements
5.1 Question Types
•	Text Answer questions
•	True / False questions
•	Multiple Choice questions
5.2 Evaluation
•	Support manual evaluation by HR.
•	Support AI evaluation suggestion (final decision by HR).
5.3 Permissions
•	HR can only see assessments they created.
•	Candidate can only see their own assessments.
6. MVP Assumptions
•	No multiple HR roles (each HR is independent).
•	No company/team system in the first version.
•	No advanced anti-cheating mechanisms (camera or tracking).
