import type { User } from "./useGetMyUser";
import { useQuery } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";
import type { Pagination } from "~/types/pagination";
import { usePagination } from "~/hooks/use-pagination";

export const GET_JOB_ASSESSMENT_APPLICATION_KEY = "job-assessments-application";

export type Application = {
    id: string;
    user: User;
    score: number;
    passing_score: number;
};

export const useGetJobAssessmentApplications = ({ jid, aid }: { jid: string, aid: string }) => {
    const { page, limit } = usePagination();
    const searchParams = new URLSearchParams({ page: String(page), limit: String(limit) });
    return useQuery({
        queryKey: [GET_JOB_ASSESSMENT_APPLICATION_KEY, page, limit],
        queryFn: async () => HTTPManager.get<Pagination<Application>>(`/applications/jobs/${jid}/assessments/${aid}?` + searchParams.toString()).then(response => response.data),
    });
}