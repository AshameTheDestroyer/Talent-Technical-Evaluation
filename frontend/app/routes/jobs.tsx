import type { Route } from "./+types/jobs";
import { useNavigate } from "react-router";
import { JobCard } from "~/components/job-card";
import { Button } from "~/components/ui/button";
import { useGetJobs } from "~/services/useGetJobs";
import { Paginator } from "~/components/paginator";
import { Loader2Icon, PlusIcon } from "lucide-react";
import { useGetMyUser } from "~/services/useGetMyUser";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Jobs" },
        {
            name: "description",
            content: "Browse active job listings and find your next opportunity!",
        },
    ];
}

export default function JobsRoute() {
    const { data: { data: jobs, total } = { data: [] }, isLoading, isError, refetch } = useGetJobs();
    const { data: myUser } = useGetMyUser();
    const Navigate = useNavigate();

    return (
        <main className="container mx-auto p-4 flex flex-col gap-4">
            <header className="flex place-content-between gap-4 flex-wrap">
                <h1 className="font-bold text-4xl">Active Jobs</h1>
                <div className="flex flex-col gap-2 place-content-center">
                    {myUser?.role == "hr" && (
                        <Button className="mb-2 sm:mb-0" onClick={() => Navigate("/jobs/create")}>
                            <PlusIcon />
                            Create New Job
                        </Button>
                    )}
                    <p className="text-center">{total} jobs in total</p>
                </div>
            </header>

            <section className="grid grid-cols-[repeat(auto-fill,minmax(400px,1fr))] gap-4">
                {isLoading && (
                    <div className="flex flex-col gap-2 place-items-center">
                        <Loader2Icon className="animate-spin" />
                        <p>Loading jobs...</p>
                    </div>
                )}
                {isError && (
                    <div className="bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-100 p-4 rounded flex flex-col gap-2 place-items-center">
                        <p className="text-center">Failed to load jobs<br />Please try again</p>
                        <button
                            onClick={() => refetch()}
                            className="ml-4 px-3 py-1 cursor-pointer bg-red-500 text-white dark:bg-red-200 dark:text-red-700 rounded"
                        >
                            Retry
                        </button>
                    </div>
                )}
                {jobs?.map(job => <JobCard key={job.id} job={job} />)}
                {total != null && total > 0 && <Paginator total={total} />}
            </section>
        </main>
    );
}
