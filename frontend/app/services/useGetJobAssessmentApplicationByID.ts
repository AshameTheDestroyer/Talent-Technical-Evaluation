import type { User } from "./useGetMyUser";
import { useQuery } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";

export const GET_JOB_ASSESSMENT_APPLICATION_BY_ID_KEY = "job-assessment-application-by-id";

export type DetailedApplication = {
    id: string;
    job_id: string;
    assessment_id: string;
    user_id: string;
    answers: Array<{
        question_id: string;
        text: string;
        question_text: string;
        weight: number;
        skill_categories: Array<string>;
        type: "text_based" | "choose_one" | "choose_many";
        question_options: Array<{ text: string; value: string }>;
        correct_options: Array<string>;
        options: Array<string>;
        rationale: string;
    }>;
    assessment_details: {
        id: string;
        title: string;
        passing_score: number;
    };
    user: User;
    score: number;
    passing_score: number;
};

export const useGetJobAssessmentApplicationByID = ({ jid, aid, id }: { jid: string, aid: string, id: string }) => useQuery({
    queryKey: [GET_JOB_ASSESSMENT_APPLICATION_BY_ID_KEY, jid, id],
    queryFn: async () =>
        HTTPManager.get<DetailedApplication>(
            `/applications/jobs/${jid}/assessment_id/${aid}/applications/${id}`,
        ).then((response) => response.data),
});
