import {
    Legend,
    Tooltip,
    BarElement,
    ArcElement,
    LinearScale,
    LineElement,
    PointElement,
    CategoryScale,
    Chart as ChartJS,
} from "chart.js";
import { Bar, Doughnut } from "react-chartjs-2";
import type { Job } from "~/services/useGetJobs";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Tooltip,
    Legend,
    ArcElement
);

export default function OverviewCharts({ jobs, loading }: { jobs: Job[]; loading?: boolean }) {
    const labels = jobs.map(j => (j.title.length > 20 ? j.title.slice(0, 20) + "…" : j.title));
    const applicantsData = jobs.map(j => j.applicants_count ?? 0);

    const seniorities = ["intern", "junior", "mid", "senior"];
    const seniorityCounts = seniorities.map(s => jobs.filter(j => j.seniority === s).length);

    const barData = {
        labels,
        datasets: [
            {
                label: "Applicants",
                data: applicantsData,
                backgroundColor: "rgba(137, 34, 197, 0.8)",
            },
        ],
    };

    const doughnutData = {
        labels: seniorities,
        datasets: [
            {
                data: seniorityCounts,
                backgroundColor: ["#60fa86", "#0babf5", "#fac18b", "#FB7185"],
            },
        ],
    };

    if (loading) {
        return <div className="h-64 flex items-center justify-center text-gray-500">Loading charts…</div>;
    }

    if (jobs.length === 0) {
        return <div className="h-64 flex items-center justify-center text-gray-500">No data to display.</div>;
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="h-64">
                <Bar data={barData} options={{ responsive: true, maintainAspectRatio: false }} />
            </div>
            <div className="h-64">
                <Doughnut data={doughnutData} options={{ responsive: true, maintainAspectRatio: false }} />
            </div>
        </div>
    );
}