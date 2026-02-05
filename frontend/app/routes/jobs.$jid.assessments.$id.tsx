import { toast } from "react-toastify";
import { Link, useParams } from "react-router";
import { ExternalLinkIcon, Loader2Icon } from "lucide-react";
import { useEffect, useState } from "react";
import { Label, RadioGroup } from "radix-ui";
import { Button } from "~/components/ui/button";
import { Textarea } from "~/components/ui/textarea";
import { Checkbox } from "~/components/ui/checkbox";
import { useGetMyUser } from "~/services/useGetMyUser";
import { RadioGroupItem } from "~/components/ui/radio-group";
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
                    <p>Loading job...</p>
                </div>
            </main>
        );
    }

    if (isError || isMyUserError) {
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

    const totalWeights = assessment.questions.reduce((weights, question) => weights + question.weight, 0);

    function handleSubmit() {
        submitAnswers({
            job_id: jid || "",
            assessment_id: id || "",
            user_id: myUser!.id,
            answers: Object.entries(answers).map(([question_id, answer]) => ({
                question_id,
                [typeof answer == "string" ? "text" : "options"]: typeof answer == "string" ? answer : Array.isArray(answer) ? answer : [answer],
            })),
        })
        .then(() => toast.success("Assessment submitted successfully"))
        .catch(error => toast.error(`Failed to submit assessment: ${error.message}`));
    }

    return (
        <main className="container mx-auto p-4 flex flex-col gap-8">
            <AssessmentCard jid={jid || ""} assessment={assessment} isStatic />
            <Link to={`/jobs/${jid}/assessment/${id}/applications`} className="text-indigo-600 hover:underline">
                View Applications for this Assessment
                <ExternalLinkIcon className="inline -translate-y-1 mx-2" />
            </Link>
            <section className="flex flex-col gap-4">
                <h3 className="text-xl font-semibold">Assessment's Questions</h3>
                <div className="flex flex-col gap-4">
                    {assessment.questions.map((question) => (
                        <div key={question.id} className="border p-4 flex flex-col gap-2 rounded bg-indigo-100 dark:bg-gray-800">
                            <header className="flex place-content-between gap-4 place-items-start">
                                <h4 className="font-semibold mb-2">{question.text}</h4>
                                <span className="inline-flex gap-2 place-items-center px-3 py-1.5 rounded-xl bg-indigo-50 dark:bg-gray-700">
                                    {totalWeights > 0 ? `~${Math.floor((question.weight / totalWeights) * 100) / 100}` : "0"}
                                </span>
                            </header>
                            {{
                                "text_based": <Textarea className="w-full resize-none" placeholder="Answer goes here..." value={answers[question.id]} onChange={e => setAnswers(prev => ({ ...prev, [question.id]: e.target.value }))} />,
                                "choose_one": (
                                    <RadioGroup.RadioGroup value={answers[question.id]} onValueChange={value => setAnswers(prev => ({ ...prev, [question.id]: value }))}>
                                        {question.options.map((option, i) => (
                                            <div key={i} className="flex items-center gap-3">
                                                <RadioGroupItem value={option.value} id={`${question.id}-option-${i}`} className="cursor-pointer" />
                                                <Label.Label htmlFor={`${question.id}-option-${i}`} className="cursor-pointer">{option.text}</Label.Label>
                                            </div>
                                        ))}
                                    </RadioGroup.RadioGroup>
                                ),
                                "choose_many": (
                                    <div>
                                        {question.options.map((option, i) => (
                                            <div key={i} className="flex items-center gap-3">
                                                <Checkbox id={`${question.id}-option-${i}`} className="cursor-pointer" value={answers[question.id]?.includes(option.value)}
                                                    onCheckedChange={checked => {
                                                        setAnswers(prev => {
                                                            const currentSelections = prev[question.id] || [];
                                                            if (checked) {
                                                                return { ...prev, [question.id]: [...currentSelections, option.value] };
                                                            } else {
                                                                return { ...prev, [question.id]: currentSelections.filter((v: string) => v !== option.value) };
                                                            }
                                                        });
                                                    }}
                                                />
                                                <Label.Label htmlFor={`${question.id}-option-${i}`} className="cursor-pointer">{option.text}</Label.Label>
                                            </div>
                                        ))}
                                    </div>
                                ),
                            }[question.type]}
                            <footer className="flex flex-wrap gap-2">
                                {question.skill_categories.map((skill) => (
                                    <span key={skill} className="inline-block bg-indigo-300 px-3 py-1.5 rounded-xl dark:bg-gray-950">
                                        {skill}
                                    </span>
                                ))}
                            </footer>
                        </div>
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