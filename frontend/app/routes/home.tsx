import type { Route } from "./+types/home";

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
