import { useMutation } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";

export const DELETE_JOB_KEY = "delete-job";

export type DeleteJobPayload = {
    id: string;
};

export const useDeleteJobMutation = () =>
    useMutation({
        mutationKey: [DELETE_JOB_KEY],
        mutationFn: async (payload: DeleteJobPayload) =>
            HTTPManager.delete(`/jobs/${payload.id}`).then(
                (response) => response.data,
            ),
    });
