import { cn } from "~/lib/utils";
import { User2Icon } from "lucide-react";
import { useNavigate } from "react-router";
import type { Job } from "~/services/useGetJobs";

export function JobCard({ job, isStatic = false }: { job: Job, isStatic?: boolean }) {
    const Navigate = useNavigate();

    return (
        <div
            tabIndex={isStatic ? -1 : 0}
            className={cn("flex flex-col gap-2", isStatic ? "" : "border p-4 rounded mb-4 bg-indigo-100 dark:bg-gray-800 [:is(:hover,:focus)]:shadow-lg [:is(:hover,:focus)]:scale-101 transition-all cursor-pointer")}
            onClick={() => isStatic || Navigate(`/jobs/${job.id}`)}
        >
            <header className="flex flex-wrap place-content-between gap-4">
                <h2 className={cn("font-semibold", isStatic ? "text-4xl" : "text-2xl")}>{job.title}</h2>
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
    );
}