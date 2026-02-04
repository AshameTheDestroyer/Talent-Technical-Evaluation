# Back-end:
> Registration:
    - /registration/signup POST({
        first_name: string,
        last_name: string,
        email: string,
        password: string,
        role: enum(hr, applicant),
    }) => {
        token: string,
    }
    - /registration/login POST({
        email: string,
        password: string,
    }) => {
        token: string,
    }
    - /registration/logout POST({}) => {}
> User:
    - /users/:id GET({}) => {
        id: string,
        first_name: string,
        last_name: string,
        email: string,
        role: enum(hr, applicant),
    }
> Jobs:
    - /jobs GET({
        page: number,
        limit: number,
    }) => {
        count: number,
        total: number,
        data: array({
            id: string,
            title: string,
            seniority: enum(intern, junior, mid, senior),
            applicants_count: number,
            active: boolean,
        }),
    }
    - /jobs/:id GET() => {
        id: string,
        title: string,
        seniority: enum(intern, junior, mid, senior),
        description: string,
        skill_categories: array(string),
        active: boolean,
    }
    - /jobs POST({
        title: string,
        seniority: enum(intern, junior, mid, senior),
        description: string,
    }) => {
        id: string,
    }
    - /jobs/:id PATCH({
        title?: string,
        seniority?: enum(intern, junior, mid, senior),
        description?: string,
        skill_categories?: array(string),
        active?: boolean,
    }) => {}
    - /jobs/:id DELETE({}) => {}
> Assessments:
    - jobs/:id/assessments GET({
        page: number,
        limit: number,
    }) => {
        count: number,
        total: number,
        data: array({
            id: string,
            title: string,
            duration: number,
            questions_count: number,
            active: boolean,
        }),
    }
    - /jobs/:jid/assessments/:aid GET({}) => {
        id: string,
        title: string,
        duration: number,
        passing_score: number,
        questions: array({
            id: string,
            text: string,
            weight: number,
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
    - /jobs/:id/assessments POST({
        title: string,
        passing_score: number.int.range(20, 80),
        questions_types: array(enum(choose_one, choose_many, text_based)),
        additional_note?: string,
    }) => {
        id: string,
    }
    - /jobs/:jid/assessments/:aid/regenerate PATCH({
        questions_types?: array(enum(choose_one, choose_many, text_based)),
        additional_note?: string,
    }) => {}
    - /jobs/:jid/assessments/:aid PATCH({
        title?: string,
        duration?: number,
        passing_score?: number.int.range(20, 80),
        questions?: array({
            text: string,
            weight: number.int.min(1, 5),
            skill_categories: array(string),
            type: enum(choose_one, choose_many, text_based),
            options?: array({
                text: string,
                value: string,
            }),
            correct_options?: array(string),
        }),
        active?: boolean,
    })
    - /jobs/:jid/assessments/:aid DELETE({}) => {}
> Application:
    - /jobs/:jid/assessments/:aid/applications GET({
        page: number,
        limit: number,
    }) => {
        count: number,
        total: number,
        data: array({
            id: string,
            user: {
                id: string,
                first_name: string,
                last_name: string,
                email: string,
            },
            score: number,
            passing_score: number,
        }),
    }
    - /jobs/:jid/assessment_id/:aid/applications/:id GET({}) => {
        id: string,
        user: {
            id: string,
            first_name: string,
            last_name: string,
            email: string,
        },
        score: number,
        passing_score: number,
        answers: array({
            question_id: string,
            text?: string,
            options?: array(string),
            question_text: string,
            weight: number,
            skill_categories: array(string),
            type: enum(choose_one, choose_many, text_based),
            options?: array({
                text: string,
                value: string,
            }),
            correct_options?: array(string),
            rationale: string,
        }),
    }
    - /jobs/:jid/assessments/:aid/applications POST({
        user_id: string,
        answers: array({
            question_id: string,
            text?: string,
            options?: array(string),
        }),
    }) => {
        id: string,
    }
> Dashboard:
    - /dashboard/applications/scores GET({
        count: number.int.range(1, 10),
        sort_by?: enum(min, max, created_at),
    }) => {
        data: array({
            user: {
                id: string,
                first_name: string,
                last_name: string,
                email: string,
            },
            score: number,
            passing_score: number,
        }),
    }
