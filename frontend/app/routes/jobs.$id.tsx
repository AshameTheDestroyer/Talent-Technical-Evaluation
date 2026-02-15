import { useNavigate, useParams } from "react-router";
import { toast } from "react-toastify";
import { Loader2Icon, PlusIcon } from "lucide-react";
import type { Route } from "./+types/jobs.$id";
import { JobCard } from "~/components/job-card";
import { Paginator } from "~/components/paginator";
import { useGetJobByID } from "~/services/useGetJobsByID";
import { AssessmentCard } from "~/components/assessment-card";
import { useGetJobAssessments } from "~/services/useGetJobAssessments";
import { Button } from "~/components/ui/button";
import { useGetMyUser } from "~/services/useGetMyUser";
import { useDeleteJobMutation } from "~/services/useDeleteJobMutation";
import { useState } from "react";

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
    const {
        data: job,
        isLoading: isJobLoading,
        isError: isJobError,
        refetch: refetchJob,
    } = useGetJobByID({ id: id || "" });
    const {
        data: { data: assessments, total } = { data: [] },
        isLoading: isAssessmentsLoading,
        isError: isAssessmentsError,
        refetch: refetchAssessments,
    } = useGetJobAssessments({ jid: id || "" });
    const { data: myUser } = useGetMyUser();
    const { mutateAsync: deleteJob, isPending: isDeletingJob } =
        useDeleteJobMutation();
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

    const isError = isJobError || isAssessmentsError;
    const isLoading = isJobLoading || isAssessmentsLoading;
    const refetch = () => (refetchJob(), refetchAssessments());

    const Navigate = useNavigate();

    async function handleDeleteJob() {
        if (!job?.id) return;

        try {
            await deleteJob({ id: job.id });
            toast.success("Job deleted successfully");
            Navigate("/jobs");
        } catch (error: any) {
            toast.error(`Failed to delete job: ${error?.message || error}`);
        }
    }

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
                    <p className="text-center">
                        Failed to load job
                        <br />
                        Please try again
                    </p>
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
                        <div className="flex flex-wrap gap-2 mb-2 sm:mb-0">
                            <Button
                                onClick={() =>
                                    Navigate(`/jobs/${id}/assessments/generate`)
                                }
                            >
                                <PlusIcon />
                                Generate New Assessment
                            </Button>
                            <Button
                                className="bg-red-600 text-white hover:bg-red-700"
                                disabled={isDeletingJob}
                                onClick={() => setIsDeleteModalOpen(true)}
                            >
                                {isDeletingJob ? "Deleting…" : "Delete Job"}
                            </Button>
                        </div>
                    )}
                </div>
                {isDeleteModalOpen && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
                        <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-lg dark:bg-gray-800">
                            <h4 className="text-lg font-semibold">
                                Delete Job
                            </h4>
                            <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">
                                Are you sure you want to delete this job? This
                                action cannot be undone.
                            </p>
                            <div className="mt-6 flex justify-end gap-3">
                                <Button
                                    variant="outline"
                                    onClick={() => setIsDeleteModalOpen(false)}
                                >
                                    Cancel
                                </Button>
                                <Button
                                    className="bg-red-600 text-white hover:bg-red-700"
                                    disabled={isDeletingJob}
                                    onClick={() => void handleDeleteJob()}
                                >
                                    {isDeletingJob ? "Deleting…" : "Delete"}
                                </Button>
                            </div>
                        </div>
                    </div>
                )}
                {assessments.length === 0 && (
                    <p className="text-center text-gray-600 dark:text-gray-300">
                        No assessments found for this job.
                    </p>
                )}
                {assessments?.map((assessment) => (
                    <AssessmentCard
                        key={assessment.id}
                        assessment={assessment}
                        jid={job.id}
                    />
                ))}
                {total != null && total > 0 && <Paginator total={total} />}
            </section>
        </main>
    );
}
