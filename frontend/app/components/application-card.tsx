import { cn } from "~/lib/utils";
import { Avatar } from "radix-ui";
import { useNavigate } from "react-router";
import type { Application } from "~/services/useGetJobAssessmentApplications";

export function ApplicationCard({ application, aid, jid, isStatic = false } : { application: Application, jid: string, aid: string, isStatic?: boolean }) {
    const Navigate = useNavigate();

    return (
        <div
            tabIndex={isStatic ? -1 : 0}
            className={cn("p-4 flex flex-wrap justify-evenly gap-4 place-items-center", isStatic ? "" : "border rounded bg-indigo-100 dark:bg-gray-700  [:is(:hover,:focus)]:shadow-lg [:is(:hover,:focus)]:scale-101 transition-all cursor-pointer")}
            onClick={() => isStatic || Navigate(`/jobs/${jid}/assessments/${aid}/applications/${application.id}`)}
        >
            <div className="group-data-[collapsible=icon]:-mx-4 flex gap-2">
                <Avatar.Avatar className="shrink-0 cursor-pointer" tabIndex={0}>
                    <Avatar.AvatarFallback className="rounded-full bg-indigo-200 dark:bg-gray-800 size-10 group-data-[collapsible=icon]:size-8 flex items-center justify-center">
                        {application.user ? `${application.user.first_name[0]}${application.user.last_name[0]}` : "U"}
                    </Avatar.AvatarFallback>
                </Avatar.Avatar>
                <div className="overflow-hidden group-data-[collapsible=icon]:hidden">
                    <p className="font-bold whitespace-nowrap text-ellipsis overflow-hidden text-start">
                        {application.user.first_name} {application.user.last_name}
                    </p>
                    <p className="whitespace-nowrap text-ellipsis overflow-hidden">
                        {application.user.email}
                    </p>
                </div>
            </div>
            <div className={cn("flex flex-col place-items-end rounded-md p-1", application.score >= application.passing_score ? "bg-green-600 dark:bg-green-700" : "bg-red-600 dark:bg-red-700")}>
                <p>Score: {application.score}%</p>
                <p>({application.passing_score}% to pass)</p>
            </div>
        </div>
    );
}
