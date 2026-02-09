import { cn } from "~/lib/utils";
import { useNavigate } from "react-router";
import { Avatar, AvatarFallback } from "@radix-ui/react-avatar";
import type { MyApplication } from "~/services/useGetMyApplications";
import type { Application } from "~/services/useGetJobAssessmentApplications";

export function ApplicationCard({ application, aid, jid, isStatic = false, safeRoute = false } : { application: Application & { job?: MyApplication["job"] }, jid: string, aid: string, isStatic?: boolean, safeRoute?: boolean }) {
    const Navigate = useNavigate();

    return (
        <div
            tabIndex={isStatic ? -1 : 0}
            className={cn("p-4 flex flex-wrap justify-between gap-4 place-items-center", isStatic ? "" : "border rounded bg-indigo-100 dark:bg-gray-700  [:is(:hover,:focus)]:shadow-lg [:is(:hover,:focus)]:scale-101 transition-all cursor-pointer")}
            onClick={() => isStatic || Navigate(safeRoute ? `/my-applications/${application.id}` : `/jobs/${jid}/assessments/${aid}/applications/${application.id}`)}
        >
            <header className="flex flex-col gap-2 w-full grow">
                <h1 className={cn("font-bold", isStatic ? "text-3xl" : "text-xl")}>{application.assessment_details.title}</h1>
                {application.job && <p className="text-gray-500 dark:text-gray-200">{application.job.title}</p>}
            </header>
            <div className="group-data-[collapsible=icon]:-mx-4 flex gap-2">
                <Avatar className="shrink-0 cursor-pointer" tabIndex={0}>
                    <AvatarFallback className="rounded-full bg-indigo-200 dark:bg-gray-800 size-10 group-data-[collapsible=icon]:size-8 flex items-center justify-center">
                        {application.user ? `${application.user.first_name[0]}${application.user.last_name[0]}` : "U"}
                    </AvatarFallback>
                </Avatar>
                <div className="overflow-hidden group-data-[collapsible=icon]:hidden">
                    <p className="font-bold whitespace-nowrap text-ellipsis overflow-hidden text-start">
                        {application.user.first_name} {application.user.last_name}
                    </p>
                    <p className="whitespace-nowrap text-ellipsis overflow-hidden">
                        {application.user.email}
                    </p>
                </div>
            </div>
            <div className={cn("flex flex-col place-items-end rounded-md p-1", application.score >= application.passing_score ? "bg-green-600 text-green-100 dark:bg-green-700 dark:text-green-300" : "bg-red-600 text-red-100 dark:bg-red-700 dark:text-red-300")}>
                <p>Score: {application.score}%</p>
                <p>({application.passing_score}% to pass)</p>
            </div>
        </div>
    );
}
