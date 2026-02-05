import { useMutation } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";

export const POST_ASSESSMENT_APPLICATION_KEY = "post-assessment-application";

export type PostAssessmentApplicationPayload = {
    job_id: string;
    user_id: string;
    assessment_id: string;
    answers: Array<{
        question_id: string;
        text?: string;
        options?: Array<string>;
    }>;
};

export const usePostAssessmentApplication = () => useMutation({
    mutationKey: [POST_ASSESSMENT_APPLICATION_KEY],
    mutationFn: async (payload: PostAssessmentApplicationPayload) =>
        HTTPManager.post(`/applications/jobs/${payload.job_id}/assessments/${payload.assessment_id}`, payload).then(response => response.data),
});