import { useQuery } from "@tanstack/react-query";
import { HTTPManager } from "~/managers/HTTPManager";

export const GET_MY_USER_KEY = "my-user";

export type User = {
    "id": string;
    "email": string;
    "last_name": string;
    "first_name": string;
    "role": "hr" | "applicant";
}

export const useGetMyUser = () => useQuery({
    queryKey: [GET_MY_USER_KEY],
    queryFn: async () => HTTPManager.get<User>("/users/me").then(response => response.data),
})