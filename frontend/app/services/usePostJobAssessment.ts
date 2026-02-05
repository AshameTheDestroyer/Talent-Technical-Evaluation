import { useMutation } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";

export const POST_JOB_ASSESSMENT_KEY = "post-job-assessment"

export type PostJobAssessmentPayload = {
    jid: string;
    body: {
        title: string;
        passing_score: number;
        additional_note: string;
        questions_types: Array<"text_based" | "choose_one" | "choose_many">;
    };
};

export const usePostJobAssessment = () => useMutation({
    mutationKey: [POST_JOB_ASSESSMENT_KEY],
    mutationFn: async (payload: PostJobAssessmentPayload) =>
        HTTPManager.post(`/assessments/jobs/${payload.jid}`, payload.body).then(response => response.data),
});