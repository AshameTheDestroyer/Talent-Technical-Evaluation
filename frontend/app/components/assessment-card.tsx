import { cn } from "~/lib/utils";
import { useNavigate } from "react-router";
import type { Assessment } from "~/services/useGetJobAssessments";
import { BadgeQuestionMarkIcon, CircleCheckIcon, CircleDotIcon, HourglassIcon, PercentIcon, TextInitialIcon } from "lucide-react";

export function AssessmentCard({ jid, assessment, isStatic = false }: { jid: string, assessment: Assessment, isStatic?: boolean }) {
    const Navigate = useNavigate();

    return (
        <div
            tabIndex={isStatic ? -1 : 0}
            className={cn("flex flex-col gap-4", isStatic ? "" : "border p-4 rounded bg-indigo-100 dark:bg-gray-800 [:is(:hover,:focus)]:shadow-lg [:is(:hover,:focus)]:scale-101 transition-all cursor-pointer")}
            onClick={() => isStatic || Navigate(`/jobs/${jid}/assessments/${assessment.id}`)}
        >
            <h4 className={cn("font-semibold", isStatic ? "text-4xl" : "text-2xl")}>{assessment.title}</h4>
            <footer className="flex flex-col gap-2">
                <div className="grow flex flex-col gap-2 mt-2">
                    <h5 className="font-semibold">Question Types</h5>
                    <div className="grow flex flex-wrap gap-2">
                        {[...new Set(assessment.questions.map(question => question.type))].map((type, i) => (
                            <span key={i} className="inline-flex gap-2 place-items-center px-3 py-1.5 rounded-xl bg-indigo-50 dark:bg-gray-700">
                                {{
                                    "text_based": <TextInitialIcon />,
                                    "choose_one": <CircleDotIcon />,
                                    "choose_many": <CircleCheckIcon />,
                                }[type]}
                                <p>{type.replace("_", " ")}</p>
                            </span>
                        ))}
                    </div>
                </div>
                <div className="flex flex-col gap-2">
                    <h5 className="font-semibold">Assessment's Details</h5>
                    <div className="grow flex flex-wrap gap-2">
                        <span className="inline-flex gap-2 place-items-center px-3 py-1.5 rounded-xl bg-indigo-50 dark:bg-gray-700">
                            <HourglassIcon />
                            <p>{assessment.duration / 60} minutes</p>
                        </span>
                        <span className="inline-flex gap-2 place-items-center px-3 py-1.5 rounded-xl bg-indigo-50 dark:bg-gray-700">
                            <PercentIcon />
                            <p>{assessment.passing_score} passing score</p>
                        </span>
                        <span className="inline-flex gap-2 place-items-center px-3 py-1.5 rounded-xl bg-indigo-50 dark:bg-gray-700">
                            <BadgeQuestionMarkIcon />
                            <p>{assessment.questions_count} questions</p>
                        </span>
                    </div>
                </div>
            </footer>
        </div>
    );
}