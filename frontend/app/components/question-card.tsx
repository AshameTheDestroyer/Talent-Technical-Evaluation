import { Label } from "radix-ui";
import { Checkbox } from "./ui/checkbox";
import { Textarea } from "./ui/textarea";
import { RadioGroup, RadioGroupItem } from "./ui/radio-group";
import type { Assessment } from "~/services/useGetJobAssessments";
import { cn } from "~/lib/utils";

export function QuestionCard({
    answers,
    question,
    rationale,
    setAnswers,
    totalWeights,
    isStatic = false,
} : {
    isStatic?: boolean;
    rationale?: string;
    totalWeights: number;
    answers: Record<string, any>;
    question: Assessment["questions"][number];
    setAnswers: React.Dispatch<React.SetStateAction<Record<string, any>>>;
}) {
    console.log({answers})

    return (
        <div className="border p-4 flex flex-col gap-2 rounded bg-indigo-100 dark:bg-gray-800">
            <header className="flex place-content-between gap-4 place-items-start">
                <h4 className="font-semibold mb-2">{question.text}</h4>
                <span className="inline-flex gap-2 place-items-center px-3 py-1.5 rounded-xl bg-indigo-50 dark:bg-gray-700">
                    {totalWeights > 0 ? `~${Math.floor((question.weight / totalWeights) * 100) / 100}` : "0"}
                </span>
            </header>
            {{
                "text_based": (
                    <div className="flex flex-col gap-4">
                        <Textarea className="w-full resize-none" placeholder="Answer goes here..." value={answers[question.id]} onChange={e => setAnswers(prev => ({ ...prev, [question.id]: e.target.value }))} readOnly={isStatic} />
                        {rationale != null && <p className="text-sm text-gray-600 dark:text-gray-400">{rationale}</p>}
                    </div>
                ),
                "choose_one": (
                    <RadioGroup value={Array.isArray(answers[question.id]) ? answers[question.id][0] : answers[question.id]} onValueChange={value => setAnswers(prev => ({ ...prev, [question.id]: value }))} disabled={isStatic}>
                        {question.options.map((option, i) => (
                            <div key={i} className="flex items-center gap-3">
                                <RadioGroupItem value={option.value} id={`${question.id}-option-${i}`} className={cn(isStatic ? "" : "cursor-pointer")} />
                                <Label.Label htmlFor={`${question.id}-option-${i}`} className={cn(isStatic ? (
                                    answers[question.id]?.includes(option.value) ? (
                                        question.correct_options?.includes(option.value) ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"
                                    ) : ""
                                ) : "cursor-pointer")}>{option.text}</Label.Label>
                            </div>
                        ))}
                    </RadioGroup>
                ),
                "choose_many": (
                    <div>
                        {question.options.map((option, i) => (
                            <div key={i} className="flex items-center gap-3">
                                <Checkbox id={`${question.id}-option-${i}`} checked={answers[question.id]?.includes(option.value)} disabled={isStatic}
                                    onCheckedChange={checked =>
                                        setAnswers(prev => {
                                            const currentSelections = prev[question.id] || [];
                                            if (checked) {
                                                return { ...prev, [question.id]: [...currentSelections, option.value] };
                                            } else {
                                                return { ...prev, [question.id]: currentSelections.filter((v: string) => v !== option.value) };
                                            }
                                        })
                                    }
                                    className={cn(isStatic ? "" : "cursor-pointer")}
                                />
                                <Label.Label htmlFor={`${question.id}-option-${i}`} className={cn(isStatic ? (
                                    answers[question.id]?.includes(option.value) ? (
                                        question.correct_options?.includes(option.value) ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"
                                    ) : ""
                                ) : "cursor-pointer")}>{option.text}</Label.Label>
                            </div>
                        ))}
                        {isStatic && question.correct_options &&  question.correct_options.some(co => !(answers[question.id] || []).includes(co)) &&
                            <div className="text-red-600 dark:text-red-400 mt-2">(You did not select all correct answers)</div>}
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
    );
}
