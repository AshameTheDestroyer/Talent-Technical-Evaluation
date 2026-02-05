import { useMutation } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";

export const POST_JOB_KEY = "post-job"

export type PostJobPayload = {
    title: string;
    description: string;
    seniority: "internship" | "junior" | "mid" | "senior";
    skill_categories: Array<string>;
};

export const usePostJob = () => useMutation({
    mutationKey: [POST_JOB_KEY],
    mutationFn: async (payload: PostJobPayload) =>
        HTTPManager.post("/jobs", payload).then(response => response.data),
});