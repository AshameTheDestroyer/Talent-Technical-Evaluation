import { useParams } from "react-router";

export default function JobDetailRoute() {
    const { id } = useParams();

    return (
        <main className="container mx-auto p-4">
            <h1 className="text-3xl font-bold">Job Details</h1>
            <p className="mt-2 text-muted-foreground">Placeholder content for job ID: {id}</p>
        </main>
    );
}
