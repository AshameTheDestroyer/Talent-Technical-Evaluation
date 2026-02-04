import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Talent Technical Evaluation" },
        { name: "description", content: "Welcome to Talent Technical Evaluation!" },
    ];
}

export default function Home() {
    return <main className="container mx-auto p-4">
        <h1 className="font-bold text-4xl">Talent Technical Evaluation</h1>
    </main>
}
