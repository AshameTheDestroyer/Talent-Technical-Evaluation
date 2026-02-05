import { useNavigate } from "react-router";
import type { Route } from "./+types/home";
import { useGetJobs } from "~/services/useGetJobs";
import { Paginator } from "~/components/paginator";
import { Loader2Icon, User2Icon } from "lucide-react";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Talent Technical Evaluation" },
        {
            name: "description",
            content: "Welcome to Talent Technical Evaluation!",
        },
    ];
}

export default function Home() {
    if (typeof window !== "undefined") {
        window.location.replace("/jobs");
    }
    return null;
}
