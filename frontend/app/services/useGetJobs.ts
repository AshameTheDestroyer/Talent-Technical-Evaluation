import { useQuery } from "@tanstack/react-query";
import { usePagination } from "~/hooks/use-pagination";
import { HTTPManager } from "~/managers/HTTPManager";
import type { Pagination } from "~/types/pagination";

export const GET_JOBS_KEY = "jobs";

export type Job = {
    id: string;
    title: string;
    active: boolean;
    description: string;
    applicants_count: number;
    skill_categories: Array<string>;
    seniority: "intern" | "junior" | "mid" | "senior";
};

export const useGetJobs = () => {
    const { page, limit } = usePagination();
    const searchParams = new URLSearchParams({ page: String(page), limit: String(limit) });
    return useQuery({
        queryKey: [GET_JOBS_KEY, page, limit],
        queryFn: async () => HTTPManager.get<Pagination<Job>>("/jobs?" + searchParams.toString()).then(response => response.data),
    });
}