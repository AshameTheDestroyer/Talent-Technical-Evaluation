import { useParams } from "react-router";
import { Loader2Icon } from "lucide-react";
import { Label, RadioGroup } from "radix-ui";
import { Textarea } from "~/components/ui/textarea";
import { Checkbox } from "~/components/ui/checkbox";
import { RadioGroupItem } from "~/components/ui/radio-group";
import { AssessmentCard } from "~/components/assessment-card";
import type { Route } from "./+types/jobs.$jid.assessments.$id";
import { useGetJobAssessmentByID } from "~/services/useGetJobAssessmentByID";

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

    const totalWeights = assessment.questions.reduce((weights, question) => weights + question.weight, 0);

    return (
        <main className="container mx-auto p-4 flex flex-col gap-8">
            <AssessmentCard jid={jid || ""} assessment={assessment} isStatic />
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
                                "text_based": <Textarea className="w-full resize-none" placeholder="Answer goes here..." />,
                                "choose_one": (
                                    <RadioGroup.RadioGroup>
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
                                                <Checkbox id={`${question.id}-option-${i}`} className="cursor-pointer" />
                                                <Label.Label htmlFor={`${question.id}-option-${i}`} className="cursor-pointer">{option.text}</Label.Label>
                                            </div>
                                        ))}
                                    </div>
                                ),
                            }[question.type]}
                        </div>
                    ))}
                </div>
            </section>
        </main>
    );
}