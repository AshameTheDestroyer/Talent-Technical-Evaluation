import { useParams } from "react-router";
import { Loader2Icon } from "lucide-react";
import type { Route } from "./+types/jobs.$jid.assessments.$aid.applications.$id";
import { useGetJobAssessmentApplicationByID, type DetailedApplication } from "~/services/useGetJobAssessmentApplicationByID";
import { ApplicationCard } from "~/components/application-card";
import { QuestionCard } from "~/components/question-card";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Application Details" },
        {
            name: "description",
            content: "Detailed view of the selected application, including candidate information and assessment results.",
        },
    ];
}

export default function ApplicationDetailsRoute() {
    const { jid, aid, id } = useParams();
    const { data: application, isLoading, isError, refetch } = useGetJobAssessmentApplicationByID({ jid: jid || "", aid: aid || "", id: id || "" });

    if (isLoading) {
        return (
            <main className="container mx-auto p-4 flex flex-col gap-2 place-items-center">
                <div className="flex flex-col gap-2 place-items-center">
                    <Loader2Icon className="animate-spin" />
                    <p>Loading application...</p>
                </div>
            </main>
        );
    }

    if (isError) {
        return (
            <main className="container mx-auto p-4 flex flex-col gap-2">
                <div className="bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-100 p-4 rounded flex flex-col gap-2 place-items-center">
                    <p className="text-center">Failed to load application<br />Please try again</p>
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

    const totalWeights = application.answers.reduce((weights, answer) => weights + answer.weight, 0);

    console.log(application)

    return (
        <main className="container mx-auto p-4 flex flex-col gap-2">
            <ApplicationCard application={application} aid={aid || ""} jid={jid || ""} isStatic />
            {application.answers.map((answer: DetailedApplication["answers"][number]) => (
                <QuestionCard
                    key={answer.question_id}
                    isStatic
                    question={{
                        type: answer.type,
                        weight: answer.weight,
                        id: answer.question_id,
                        text: answer.question_text,
                        options: answer.question_options,
                        correct_options: answer.correct_options,
                        skill_categories: answer.skill_categories,
                    }}
                    answers={application.answers.reduce((accumulator, current) => ({
                        ...accumulator,
                        [current.question_id]: current.type == "text_based" ? current.text : current.type == "choose_one" ? current.options : current.options,
                    }), {})}
                    setAnswers={() => {}}
                    totalWeights={totalWeights}
                    rationale={answer.rationale}
                />
            ))}
        </main>
    )
}