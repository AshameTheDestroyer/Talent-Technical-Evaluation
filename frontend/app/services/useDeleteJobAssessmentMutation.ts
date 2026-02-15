import { useMutation } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";

export const DELETE_JOB_ASSESSMENT_KEY = "delete-job-assessment";

export type DeleteJobAssessmentPayload = {
    jid: string;
    id: string;
};

export const useDeleteJobAssessmentMutation = () => useMutation({
    mutationKey: [DELETE_JOB_ASSESSMENT_KEY],
    mutationFn: async (payload: DeleteJobAssessmentPayload) =>
        HTTPManager.delete(`/assessments/jobs/${payload.jid}/${payload.id}`).then(response => response.data),
});
