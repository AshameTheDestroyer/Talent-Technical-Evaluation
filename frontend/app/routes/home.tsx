import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Skill Sight" },
        {
            name: "description",
            content: "Welcome to Skill Sight!",
        },
    ];
}

export default function Home() {
    if (typeof window !== "undefined") {
        window.location.replace("/jobs");
    }
    return null;
}
