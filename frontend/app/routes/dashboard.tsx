import { useMemo } from "react";
import type { Route } from "./+types/dashboard";
import { useGetJobs } from "~/services/useGetJobs";
import OverviewCharts from "~/components/overview-charts";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Dashboard" },
        {
            name: "description",
            content: "Overview of platform metrics and insights to track your hiring process.",
        },
    ];
}

export default function Dashboard() {
    const { data, isLoading, isError } = useGetJobs();
    const jobs = data?.data ?? [];

    const totals = useMemo(() => {
        const totalJobs = jobs.length;
        const totalApplicants = jobs.reduce((s, j) => s + (j.applicants_count ?? 0), 0);
        const activeJobs = jobs.filter(j => j.active).length;
        return { totalJobs, totalApplicants, activeJobs };
    }, [jobs]);

    return (
        <div className="p-6 space-y-6">
            <header className="flex items-center justify-between">
                <h1 className="text-2xl font-semibold">Dashboard</h1>
                <p className="text-sm text-muted-foreground">Overview and quick insights</p>
            </header>

            <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="p-4 bg-white dark:bg-gray-800 shadow rounded">
                    <div className="text-sm text-gray-500 dark:text-gray-200">Total Jobs</div>
                    <div className="mt-2 text-3xl font-bold">{isLoading ? "…" : totals.totalJobs}</div>
                </div>
                <div className="p-4 bg-white dark:bg-gray-800 shadow rounded">
                    <div className="text-sm text-gray-500 dark:text-gray-200">Total Applicants</div>
                    <div className="mt-2 text-3xl font-bold">{isLoading ? "…" : totals.totalApplicants}</div>
                </div>
                <div className="p-4 bg-white dark:bg-gray-800 shadow rounded">
                    <div className="text-sm text-gray-500 dark:text-gray-200">Active Jobs</div>
                    <div className="mt-2 text-3xl font-bold">{isLoading ? "…" : totals.activeJobs}</div>
                </div>
            </section>

            <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="p-4 bg-white dark:bg-gray-800 shadow rounded">
                    <h2 className="text-lg font-medium mb-4">Applicants Per Job</h2>
                    <OverviewCharts jobs={jobs} loading={isLoading} />
                </div>
                <div className="p-4 bg-white dark:bg-gray-800 shadow rounded">
                    <h2 className="text-lg font-medium mb-4">Quick Insights</h2>
                    {isError && <div className="text-red-500">Error loading data</div>}
                    {!isLoading && jobs.length === 0 && <div className="text-sm text-gray-600 dark:text-gray-200">No jobs yet.</div>}
                    {!isLoading && jobs.length > 0 && (
                        <ul className="space-y-3">
                            <li className="flex justify-between">
                                <span className="text-sm text-gray-700 dark:text-gray-200">Top job (by applicants)</span>
                                <span className="font-medium">
                                    {jobs.slice().sort((a,b) => (b.applicants_count||0)-(a.applicants_count||0))[0]?.title ?? "—"}
                                </span>
                            </li>
                            <li className="flex justify-between">
                                <span className="text-sm text-gray-700 dark:text-gray-200">Most common seniority</span>
                                <span className="font-medium">
                                    {(() => {
                                        const counts = jobs.reduce<Record<string,number>>((acc, j) => {
                                            acc[j.seniority] = (acc[j.seniority] || 0) + 1;
                                            return acc;
                                        }, {});
                                        const entries = Object.entries(counts);
                                        if (!entries.length) return "—";
                                        return entries.sort((a,b) => b[1]-a[1])[0][0];
                                    })()}
                                </span>
                            </li>
                            <li className="flex justify-between">
                                <span className="text-sm text-gray-700 dark:text-gray-200">Jobs with no applicants</span>
                                <span className="font-medium">{jobs.filter(j => !j.applicants_count).length}</span>
                            </li>
                        </ul>
                    )}
                </div>
            </section>
        </div>
    );
}