import { Loader2Icon } from "lucide-react";
import { Paginator } from "~/components/paginator";
import type { Route } from "./+types/my-applications";
import { useGetMyUser } from "~/services/useGetMyUser";
import { ApplicationCard } from "~/components/application-card";
import { useGetMyApplications } from "~/services/useGetMyApplications";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "My Applications" },
        {
            name: "description",
            content: "View and manage your job applications, track their status, and review feedback from assessments.",
        },
    ];
}

export default function MyApplicationsRoute() {
    const { data: myUser, isLoading: isMyUserLoading, isError: isMyUserError, refetch: refetchMyUser } = useGetMyUser();
    const { data: { data: applications, total } = { data: [] }, isLoading: isApplicationsLoading, isError: isApplicationsError, refetch: refetchApplications } = useGetMyApplications();

    const isError = isMyUserError || isApplicationsError;
    const isLoading = isMyUserLoading || isApplicationsLoading;
    const refetch = () => (refetchMyUser(), refetchApplications());

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
            <section className="flex flex-col gap-4">
                <h3 className="text-xl font-semibold">Assessment's Applications</h3>
                <div className="grid grid-cols-[repeat(auto-fill,minmax(400px,1fr))] gap-4">
                    {applications.length === 0 ? (
                        <p>No applications found.<br/>Start applying now!</p>
                    ) : applications.map(application => (
                        <ApplicationCard key={application.id} application={{...application, user: myUser, passing_score: application.assessment.passing_score, assessment_details: application.assessment}} jid={application.job.id || ""} aid={application.assessment.id || ""} safeRoute />
                    ))}
                </div>
                {total != null && total > 0 && <Paginator total={total} />}
            </section>
        </main>
    );
}