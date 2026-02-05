import type { Route } from "./+types/jobs";
import { useNavigate } from "react-router";
import { useGetJobs } from "~/services/useGetJobs";
import { Paginator } from "~/components/paginator";
import { Loader2Icon, User2Icon } from "lucide-react";

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
    const Navigate = useNavigate();

    return (
        <main className="container mx-auto p-4 flex flex-col gap-4">
            <header className="flex place-content-between gap-4 flex-wrap">
                <h1 className="font-bold text-4xl">Active Jobs</h1>
                <p>{total} jobs in total</p>
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
                {jobs?.map(job =>
                    <div
                        key={job.id}
                        tabIndex={0}
                        className="border p-4 flex flex-col gap-2 rounded mb-4 bg-indigo-100 dark:bg-gray-800 [:is(:hover,:focus)]:shadow-lg [:is(:hover,:focus)]:scale-101  transition-all cursor-pointer"
                        onClick={() => Navigate(`/jobs/${job.id}`)}
                    >
                        <header className="flex flex-wrap place-content-between gap-4">
                            <h2 className="font-semibold text-2xl">{job.title}</h2>
                            <span className={"px-3 py-1.5 rounded-xl " + {
                                "intern": "bg-green-300 dark:bg-green-800",
                                "junior": "bg-blue-300 dark:bg-blue-800",
                                "mid": "bg-yellow-300 dark:bg-yellow-800",
                                "senior": "bg-red-300 dark:bg-red-800",
                            }[job.seniority]}>{job.seniority[0].toUpperCase()}{job.seniority.slice(1)}</span>
                        </header>
                        <p className="line-clamp-2">{job.description}</p>
                        <footer className="flex gap-2 mt-auto place-content-between">
                            <div className="flex flex-wrap gap-2">
                                {job.skill_categories.map((skill) => (
                                    <span key={skill} className="inline-block bg-indigo-300 px-3 py-1.5 rounded-xl dark:bg-gray-950">
                                        {skill}
                                    </span>
                                ))}
                            </div>
                            <span className="place-self-end flex gap-2 place-items-center px-3 py-1.5 rounded-xl bg-indigo-50 dark:bg-gray-700">
                                <User2Icon />
                                <p>{job.applicants_count}</p>
                            </span>
                        </footer>
                    </div>
                )}
                {total && <Paginator total={total} />}
            </section>
        </main>
    );
}
