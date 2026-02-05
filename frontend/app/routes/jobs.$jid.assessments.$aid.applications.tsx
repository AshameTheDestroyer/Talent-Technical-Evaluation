import { useParams } from "react-router";
import { Loader2Icon } from "lucide-react";
import { JobCard } from "~/components/job-card";
import { Paginator } from "~/components/paginator";
import { useGetJobByID } from "~/services/useGetJobsByID";
import { AssessmentCard } from "~/components/assessment-card";
import { ApplicationCard } from "~/components/application-card";
import { useGetJobAssessmentByID } from "~/services/useGetJobAssessmentByID";
import type { Route } from "./+types/jobs.$jid.assessments.$aid.applications";
import { useGetJobAssessmentApplications } from "~/services/useGetJobAssessmentApplications";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Assessments Applications" },
        {
            name: "description",
            content: "View applications for the selected job assessment.",
        },
    ];
}

export default function AssessmentDetailRoute() {
    const { jid, aid } = useParams();
    const { data: job, isLoading: isJobLoading, isError: isJobError, refetch: refetchJob } = useGetJobByID({ id: jid || "" });
    const { data: jobAssessment, isLoading: isJobAssessmentLoading, isError: isJobAssessmentError, refetch: refetchJobAssessment } = useGetJobAssessmentByID({ jid: jid || "", id: aid || "" });
    const { data: { data: applications, total } = { data: [] }, isLoading: isApplicationsLoading, isError: isApplicationsError, refetch: refetchApplications } = useGetJobAssessmentApplications({ jid: jid || "", aid: aid || "" });

    const isError = isJobError || isJobAssessmentError || isApplicationsError;
    const isLoading = isJobLoading || isJobAssessmentLoading || isApplicationsLoading;
    const refetch = () => (refetchJob(), refetchJobAssessment(), refetchApplications());

    if (isLoading) {
        return (
            <main className="container mx-auto p-4 flex flex-col gap-2 place-items-center">
                <div className="flex flex-col gap-2 place-items-center">
                    <Loader2Icon className="animate-spin" />
                    <p>Loading Applications...</p>
                </div>
            </main>
        );
    }

    if (isError) {
        return (
            <main className="container mx-auto p-4 flex flex-col gap-2">
                <div className="bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-100 p-4 rounded flex flex-col gap-2 place-items-center">
                    <p className="text-center">Failed to load applications<br />Please try again</p>
                    <button
                        onClick={() => refetch()}
                        className="ml-4 px-3 py-1 cursor-pointer bg-red-500 text-white dark:bg-red-200 dark:text-red-700 rounded"
                    >
                        Retry
                    </button>
                </div>
            </main>
        );
    }

    return (
        <main className="container mx-auto p-4 flex flex-col gap-8">
            <JobCard job={job} isStatic />
            <AssessmentCard jid={jid || ""} assessment={jobAssessment} isStatic />
            <section className="flex flex-col gap-4">
                <h3 className="text-xl font-semibold">Assessment's Applications</h3>
                <div className="grid grid-cols-[repeat(auto-fill,minmax(400px,1fr))] gap-4">
                    {applications.length === 0 ? (
                        <p>No applications found for this assessment.</p>
                    ) : applications.map(application => (
                        <ApplicationCard key={application.id} application={application} jid={jid || ""} aid={aid || ""} />
                    ))}
                </div>
                {total != null && total > 0 && <Paginator total={total} />}
            </section>
        </main>
    );
}