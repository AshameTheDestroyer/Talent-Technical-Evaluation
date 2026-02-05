import type { Job } from "./useGetJobs";
import { useQuery } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";

export const GET_JOB_BY_ID_KEY = "job-by-id";

export const useGetJobByID = ({ id }: { id: string }) => {
    return useQuery({
        queryKey: [GET_JOB_BY_ID_KEY, id],
        queryFn: async () => HTTPManager.get<Job>(`/jobs/${id}`).then(response => response.data),
    });
}