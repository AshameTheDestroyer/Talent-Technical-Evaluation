import { useQuery } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";
import type { Pagination } from "~/types/pagination";
import { usePagination } from "~/hooks/use-pagination";

export const GET_MY_APPLICATIONS_KEY = "job-my-applications";

export type MyApplication = {
    id: string;
    score: number;
    job: {
        id: string;
        title: string;
        description: string;
        seniority: "intern" | "junior" | "mid" | "senior";
    };
    assessment: {
        id: string;
        title: string;
        passing_score: number;
    };
}

export const useGetMyApplications = () => {
    const { page, limit } = usePagination();
    const searchParams = new URLSearchParams({ page: String(page), limit: String(limit) });
    return useQuery({
        queryKey: [GET_MY_APPLICATIONS_KEY, page, limit],
        queryFn: async () => HTTPManager.get<Pagination<MyApplication>>(`/applications/my-applications?` + searchParams.toString()).then(response => response.data),
    });
}