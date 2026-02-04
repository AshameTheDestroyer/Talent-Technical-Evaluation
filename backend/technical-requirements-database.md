# Database:
> User: {
    id: string,
    first_name: string,
    last_name: string,
    email: string,
    password: string,
    role: enum(hr, applicant),
}
> Job: {
    id: string,
    title: string,
    seniority: enum(intern, junior, mid, senior),
    description: string,
    skill_categories: array(string),
    active: boolean,
}
> Assessment: {
    id: string,
    job_id: string,
    title: string,
    duration: number, // in seconds.
    passing_score: number.int.range(20, 80),
    questions: array({
        id: string,
        text: string,
        weight: number.int.range(1, 5),
        skill_categories: array(string),
        type: enum(choose_one, choose_many, text_based),
        options?: array({
            text: string,
            value: string,
        }),
        correct_options?: array(string),
    }),
    active: boolean,
}
> Application: {
    id: string,
    job_id: string,
    assessment_id; string,
    user_id: string,
    answers: array({
        question_id: string,
        text?: string,
        options?: array(string),
    }),
}
