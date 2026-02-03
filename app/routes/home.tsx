import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Talent Technical Evaluation" },
        { name: "description", content: "Welcome to Talent Technical Evaluation!" },
    ];
}

export default function Home() {
    return <Welcome />;
}
