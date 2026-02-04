import sqlite3
import json

def verify_seeded_data():
    """Verify that the demo data was correctly seeded in the database."""
    conn = sqlite3.connect('assessment_platform.db')
    cursor = conn.cursor()
    
    print("=== Verifying Seeded Data ===\n")
    
    # Check HR users
    cursor.execute("SELECT first_name, last_name, email FROM users WHERE role='hr'")
    hr_users = cursor.fetchall()
    print(f"HR Users Found: {len(hr_users)}")
    for user in hr_users:
        print(f"  - {user[0]} {user[1]} ({user[2]})")
    print()
    
    # Check Candidate users
    cursor.execute("SELECT first_name, last_name, email FROM users WHERE role='applicant'")
    candidate_users = cursor.fetchall()
    print(f"Candidate Users Found: {len(candidate_users)}")
    for user in candidate_users:
        print(f"  - {user[0]} {user[1]} ({user[2]})")
    print()
    
    # Check Jobs
    cursor.execute("SELECT title, seniority, description FROM jobs")
    jobs = cursor.fetchall()
    print(f"Jobs Found: {len(jobs)}")
    for job in jobs:
        print(f"  - {job[0]} ({job[1]})")
    print()
    
    # Check Assessments
    cursor.execute("SELECT title, job_id FROM assessments")
    assessments = cursor.fetchall()
    print(f"Assessments Found: {len(assessments)}")
    for assessment in assessments:
        print(f"  - {assessment[0]} (Job ID: {assessment[1][:8]}...)")
    print()
    
    # Check a sample assessment's questions
    if assessments:
        cursor.execute("SELECT title, questions FROM assessments LIMIT 1")
        assessment = cursor.fetchone()
        if assessment:
            print(f"Sample Assessment: {assessment[0]}")
            try:
                questions = json.loads(assessment[1])
                print(f"Number of questions: {len(questions)}")
                for i, q in enumerate(questions[:2]):  # Show first 2 questions
                    print(f"  Q{i+1}: {q['text'][:60]}...")
            except json.JSONDecodeError:
                print("Could not decode questions JSON")
    print()
    
    # Verify specific demo users exist
    demo_hr_emails = [
        'sarah.johnson@demo.com',
        'michael.chen@demo.com', 
        'emma.rodriguez@demo.com',
        'david.wilson@demo.com'
    ]
    
    demo_candidate_emails = [
        'alex.thompson@demo.com',
        'jessica.lee@demo.com',
        'ryan.patel@demo.com',
        'olivia.kim@demo.com'
    ]
    
    print("=== Verification Results ===")
    
    # Check if demo HR users exist
    for email in demo_hr_emails:
        cursor.execute("SELECT COUNT(*) FROM users WHERE email=?", (email,))
        count = cursor.fetchone()[0]
        status = "[PASS]" if count > 0 else "[FAIL]"
        print(f"{status} HR User {email}: {'Found' if count > 0 else 'Not Found'}")

    print()

    # Check if demo candidate users exist
    for email in demo_candidate_emails:
        cursor.execute("SELECT COUNT(*) FROM users WHERE email=?", (email,))
        count = cursor.fetchone()[0]
        status = "[PASS]" if count > 0 else "[FAIL]"
        print(f"{status} Candidate User {email}: {'Found' if count > 0 else 'Not Found'}")
    
    conn.close()

if __name__ == "__main__":
    verify_seeded_data()