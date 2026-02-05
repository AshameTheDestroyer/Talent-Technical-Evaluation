import { useQuery } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";
import type { MyApplication } from "./useGetMyApplications";
import type { DetailedApplication } from "./useGetJobAssessmentApplicationByID";

export const GET_JOB_ASSESSMENT_APPLICATION_BY_ID_KEY = "job-assessment-application-by-id";

export type DetailedMyApplication = MyApplication & DetailedApplication;

export const useGetMyApplicationByID = ({ id }: { id: string }) => useQuery({
    queryKey: [GET_JOB_ASSESSMENT_APPLICATION_BY_ID_KEY, id],
    queryFn: async () =>
        HTTPManager.get<DetailedMyApplication>(`/applications/my-applications/${id}`).then((response) => response.data),
});
