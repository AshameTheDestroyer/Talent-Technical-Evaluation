import { useQuery } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";
import type { Pagination } from "~/types/pagination";
import { usePagination } from "~/hooks/use-pagination";

export const GET_JOB_ASSESSMENT_KEY = "job-assessments";

export type Assessment = {
    id: string;
    title: string;
    active: boolean;
    duration: number;
    passing_score: number;
    questions_count: number;
    questions: Array<{
        id: string;
        text: string;
        weight: number;
        correct_options: Array<string>;
        skill_categories: Array<string>;
        options: Array<{ text: string; value: string }>;
        type: "text_based" | "choose_one" | "choose_many";
    }>;
};

export const useGetJobAssessments = ({ jid }: { jid: string }) => {
    const { page, limit } = usePagination();
    const searchParams = new URLSearchParams({ page: String(page), limit: String(limit) });
    return useQuery({
        queryKey: [GET_JOB_ASSESSMENT_KEY, page, limit],
        queryFn: async () => HTTPManager.get<Pagination<Assessment>>(`/assessments/jobs/${jid}?` + searchParams.toString()).then(response => response.data),
    });
}