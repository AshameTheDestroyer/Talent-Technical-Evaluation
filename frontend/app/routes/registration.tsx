import type { Route } from "./+types/registration";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Registration" },
        {
            name: "description",
            content: "Login to access your account or create a new one.",
        },
    ];
}

export default function Registration() {
}