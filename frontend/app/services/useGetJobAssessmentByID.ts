import { useQuery } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";
import type { Assessment } from "./useGetJobAssessments";

export const GET_JOB_ASSESSMENT_BY_ID_KEY = "job-assessments-by-id";

export const useGetJobAssessmentByID = ({ jid, id }: { jid: string, id: string }) => {
    return useQuery({
        queryKey: [GET_JOB_ASSESSMENT_BY_ID_KEY, jid, id],
        queryFn: async () => HTTPManager.get<Assessment>(`/assessments/jobs/${jid}/${id}`).then(response => response.data),
    });
}