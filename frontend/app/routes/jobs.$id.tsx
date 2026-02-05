import { useNavigate, useParams } from "react-router";
import {Loader2Icon, PlusIcon, } from "lucide-react";
import type { Route } from "./+types/jobs.$id";
import { JobCard } from "~/components/job-card";
import { Paginator } from "~/components/paginator";
import { useGetJobByID } from "~/services/useGetJobsByID";
import { AssessmentCard } from "~/components/assessment-card";
import { useGetJobAssessments } from "~/services/useGetJobAssessments";
import { Button } from "~/components/ui/button";
import { useGetMyUser } from "~/services/useGetMyUser";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Job Details" },
        {
            name: "description",
            content: "Detailed view of the selected job and its assessments.",
        },
    ];
}

export default function JobDetailRoute() {
    const { id } = useParams();
    const { data: job, isLoading: isJobLoading, isError: isJobError, refetch: refetchJob } = useGetJobByID({ id: id || "" });
    const { data: { data: assessments, total } = { data: [] }, isLoading: isAssessmentsLoading, isError: isAssessmentsError, refetch: refetchAssessments } = useGetJobAssessments({ jid: id || "" });
    const { data: myUser } = useGetMyUser();

    const isError = isJobError || isAssessmentsError;
    const isLoading = isJobLoading || isAssessmentsLoading;
    const refetch = () => (refetchJob(), refetchAssessments());

    const Navigate = useNavigate();

    if (isLoading) {
        return (
            <main className="container mx-auto p-4 flex flex-col gap-2 place-items-center">
                <div className="flex flex-col gap-2 place-items-center">
                    <Loader2Icon className="animate-spin" />
                    <p>Loading job...</p>
                </div>
            </main>
        );
    }

    if (isError) {
        return (
            <main className="container mx-auto p-4 flex flex-col gap-2">
                <div className="bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-100 p-4 rounded flex flex-col gap-2 place-items-center">
                    <p className="text-center">Failed to load job<br />Please try again</p>
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
            <section className="flex flex-col gap-4">
                 <div className="flex gap-2 place-content-between flex-wrap">
                    <h3 className="text-xl font-semibold">Job's Assessments</h3>
                    {myUser?.role == "hr" && (
                        <Button className="mb-2 sm:mb-0" onClick={() => Navigate(`/jobs/${id}/assessments/generate`)}>
                            <PlusIcon />
                            Generate New Assessment
                        </Button>
                    )}
                </div>
                {assessments.length === 0 && (
                    <p className="text-center text-gray-600 dark:text-gray-300">No assessments found for this job.</p>
                )}
                {assessments?.map(assessment => <AssessmentCard key={assessment.id} assessment={assessment} jid={job.id} />)}
                {total != null && total > 0 && <Paginator total={total} />}
            </section>
        </main>
    );
}
