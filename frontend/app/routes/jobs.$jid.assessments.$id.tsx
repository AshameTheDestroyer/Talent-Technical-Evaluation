import { toast } from "react-toastify";
import { useEffect, useState } from "react";
import { Button } from "~/components/ui/button";
import { useGetMyUser } from "~/services/useGetMyUser";
import { QuestionCard } from "~/components/question-card";
import { Link, useNavigate, useParams } from "react-router";
import { ExternalLinkIcon, Loader2Icon } from "lucide-react";
import { AssessmentCard } from "~/components/assessment-card";
import type { Route } from "./+types/jobs.$jid.assessments.$id";
import { useGetJobAssessmentByID } from "~/services/useGetJobAssessmentByID";
import { usePostAssessmentApplication } from "~/services/usePostAssessmentApplication";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Assessment Details" },
        {
            name: "description",
            content: "Detailed view of the selected assessment.",
        },
    ];
}

export default function AssessmentDetailRoute() {
    const { jid, id } = useParams();
    const { data: assessment, isLoading, isError, refetch } = useGetJobAssessmentByID({ jid: jid || "", id: id || "" });
    const [answers, setAnswers] = useState({} as Record<string, any>);

    const Navigate = useNavigate();
    const { mutateAsync: submitAnswers, isPending: isSubmittingLoading } = usePostAssessmentApplication();
    const { data: myUser, isLoading: isMyUserLoading, isError: isMyUserError } = useGetMyUser();

    useEffect(() => {
        if (assessment == null) { return }

        setAnswers(assessment.questions.reduce((accumulator, question) => {
            accumulator[question.id] = question.type === "choose_many" ? [] : "";
            return accumulator;
        }, {} as Record<string, any>));
    }, [assessment]);

    if (isLoading || isMyUserLoading) {
        return (
            <main className="container mx-auto p-4 flex flex-col gap-2 place-items-center">
                <div className="flex flex-col gap-2 place-items-center">
                    <Loader2Icon className="animate-spin" />
                    <p>Loading assessment...</p>
                </div>
            </main>
        );
    }

    if (isError || isMyUserError) {
        return (
            <main className="container mx-auto p-4 flex flex-col gap-2">
                <div className="bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-100 p-4 rounded flex flex-col gap-2 place-items-center">
                    <p className="text-center">Failed to load assessment<br />Please try again</p>
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

    useEffect(() => {
        if (assessment == null) { return }

        setAnswers(assessment.questions.reduce((accumulator, question) => {
            accumulator[question.id] = question.type === "choose_many" ? [] : "";
            return accumulator;
        }, {} as Record<string, any>));
    }, [assessment]);

    const totalWeights = assessment.questions.reduce((weights, question) => weights + question.weight, 0);

    function handleSubmit() {
        submitAnswers({
            job_id: jid || "",
            assessment_id: id || "",
            user_id: myUser!.id,
            answers: Object.entries(answers).map(([question_id, answer]) => {
                const isTextBased = assessment?.questions.find(q => q.id === question_id)?.type === "text_based";
                return {
                    question_id,
                    [isTextBased ? "text" : "options"]: isTextBased ? answer : Array.isArray(answer) ? answer : [answer],
                };
            })
        })
        .then(({id:appId}) => {
            toast.success("Assessment submitted successfully")
            Navigate(`/jobs/${jid}/assessments/${id}/applications/${appId}`);
        })
        .catch(error => toast.error(`Failed to submit assessment: ${error.message}`));
    }

    return (
        <main className="container mx-auto p-4 flex flex-col gap-8">
            <AssessmentCard jid={jid || ""} assessment={assessment} isStatic />
            {myUser.role == "hr" && (
                <Link to={`/jobs/${jid}/assessment/${id}/applications`} className="text-indigo-600 hover:underline">
                    View Applications for this Assessment
                    <ExternalLinkIcon className="inline -translate-y-1 mx-2" />
                </Link>
            )}
            <section className="flex flex-col gap-4">
                <h3 className="text-xl font-semibold">Assessment's Questions</h3>
                <div className="flex flex-col gap-4">
                    {assessment.questions.map((question) => (
                        <QuestionCard key={question.id} question={question} totalWeights={totalWeights} answers={answers} setAnswers={setAnswers} isStatic={myUser.role == "hr"} />
                    ))}
                </div>
            </section>
            <footer className="mx-auto py-4">
                {myUser.role === "applicant" && (
                    <Button
                        disabled={isSubmittingLoading}
                        className="bg-indigo-600 text-white hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 disabled:opacity-50"
                        onClick={handleSubmit}
                    >
                        Submit Answers
                    </Button>
                )}
            </footer>
        </main>
    );
}