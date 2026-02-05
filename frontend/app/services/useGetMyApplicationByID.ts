import { useQuery } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";
import type { User } from "./useGetMyUser";

export const GET_JOB_ASSESSMENT_APPLICATION_BY_ID_KEY = "job-assessment-application-by-id";

export type DetailedMyApplication = {
    id: string;
    job_id: string;
    assessment_id: string;
    user_id: string;
    answers: Array<{
        question_id: string;
        text: string;
        options: Array<string>;
        question_text: string;
        weight: number;
        skill_categories: Array<string>;
        type: "text_based" | "choose_one" | "choose_many";
        question_options: Array<{ text: string; value: string }>;
        correct_options: Array<string>;
        rationale: string;
    }>;
    assessment_details: {
        id: string;
        title: string;
        passing_score: number;
        created_at: string | null;
    };
    score: number;
    passing_score: number;
    user: User;
};

export const useGetMyApplicationByID = ({ id }: { id: string }) =>
    useQuery({
        queryKey: [GET_JOB_ASSESSMENT_APPLICATION_BY_ID_KEY, id],
        queryFn: async () =>
            HTTPManager.get<DetailedMyApplication>(`/applications/my-applications/${id}`).then((response) => response.data),
    });
