import { toast } from "react-toastify";
import { Button } from "~/components/ui/button";
import { useEffect, useState, useRef } from "react";
import { useGetMyUser } from "~/services/useGetMyUser";
import { QuestionCard } from "~/components/question-card";
import { Link, useNavigate, useParams } from "react-router";
import { AssessmentCard } from "~/components/assessment-card";
import type { Route } from "./+types/jobs.$jid.assessments.$id";
import { ExternalLinkIcon, HourglassIcon, Loader2Icon } from "lucide-react";
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

function formatTime(totalSeconds: number) {
    const seconds = Math.max(0, Math.floor(totalSeconds));
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export default function AssessmentDetailRoute() {
    const { jid, id } = useParams();
    const { data: assessment, isLoading, isError, refetch } = useGetJobAssessmentByID({ jid: jid || "", id: id || "" });
    const [answers, setAnswers] = useState({} as Record<string, any>);
    const answersRef = useRef<Record<string, any>>({});

    const Navigate = useNavigate();
    const { mutateAsync: submitAnswers, isPending: isSubmittingLoading } = usePostAssessmentApplication();
    const { data: myUser, isLoading: isMyUserLoading, isError: isMyUserError } = useGetMyUser();

    const [started, setStarted] = useState(false);
    const [remainingSeconds, setRemainingSeconds] = useState<number | null>(null);
    const [isSubmitted, setIsSubmitted] = useState(false);
    const timerRef = useRef<number | null>(null);
    const endAtRef = useRef<number | null>(null);

    const setAnswersAndRef: React.Dispatch<React.SetStateAction<Record<string, any>>> = (updater) => {
        setAnswers(prev => {
            const next = typeof updater === "function" ? (updater as (p: Record<string, any>) => Record<string, any>)(prev) : updater;
            answersRef.current = next;
            return next;
        });
    };

    useEffect(() => {
        if (assessment == null || Object.entries(answersRef.current).length > 0) { return; }

        const initial = assessment.questions.reduce((accumulator, question) => {
            accumulator[question.id] = question.type === "choose_many" ? [] : "";
            return accumulator;
        }, {} as Record<string, any>);

        answersRef.current = initial;
        setAnswers(initial);
    }, [assessment]);

    useEffect(() => {
        if (!started) {
            if (timerRef.current) {
                window.clearInterval(timerRef.current);
                timerRef.current = null;
            }
            return;
        }
        if (!assessment) return;

        const durationSec = Number(assessment.duration || 0);
        endAtRef.current = Date.now() + durationSec * 1000;
        setRemainingSeconds(Math.ceil((endAtRef.current - Date.now()) / 1000));

        timerRef.current = window.setInterval(() => {
            const rem = Math.max(0, Math.ceil(((endAtRef.current || 0) - Date.now()) / 1000));
            setRemainingSeconds(rem);

            if (rem <= 0) {
                if (timerRef.current) {
                    window.clearInterval(timerRef.current);
                    timerRef.current = null;
                }
                if (!isSubmitted) {
                    void handleSubmit(true);
                }
            }
        }, 1000);

        return () => {
            if (timerRef.current) {
                window.clearInterval(timerRef.current);
                timerRef.current = null;
            }
        };
    }, [started, assessment, isSubmitted]);

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

    if (!assessment || !myUser) return null;

    const totalWeights = assessment.questions.reduce((weights, question) => weights + question.weight, 0);

    async function handleSubmit(isAuto = false) {
        if (isSubmitted) return;
        setIsSubmitted(true);

        try {
            const payloadAnswers = Object.entries(answersRef.current).map(([question_id, answer]) => {
                const isTextBased = assessment?.questions.find(q => q.id === question_id)?.type === "text_based";
                return {
                    question_id,
                    [isTextBased ? "text" : "options"]: isTextBased ? answer : Array.isArray(answer) ? answer : [answer],
                };
            });

            const result = await submitAnswers({
                job_id: jid || "",
                assessment_id: id || "",
                user_id: myUser!.id,
                answers: payloadAnswers,
            });

            if (!isAuto) {
                toast.success("Assessment submitted successfully");
            } else {
                toast.info("Timer ended! Assessment auto-submitted");
            }

            Navigate(`/my-applications/${result.id}`);
        } catch (error: any) {
            setIsSubmitted(false);
            toast.error(`Failed to submit assessment: ${error?.message || error}`);
        }
    }

    return (
        <main className="container mx-auto p-4 flex flex-col gap-8">
            <AssessmentCard jid={jid || ""} assessment={assessment} isStatic />
            {myUser.role == "hr" && (
                <Link to={`/jobs/${jid}/assessments/${id}/applications`} className="text-indigo-600 hover:underline">
                    View Applications for this Assessment
                    <ExternalLinkIcon className="inline -translate-y-1 mx-2" />
                </Link>
            )}
            <section className="flex flex-col gap-6">
                <header className="flex gap-4 place-content-between flex-wrap items-center">
                    <h3 className="text-xl font-semibold">Assessment's Questions</h3>
                    <span className="flex gap-2 place-items-center px-3 py-1.5 rounded-xl bg-indigo-50 dark:bg-gray-700">
                        <HourglassIcon className={started ? "animate-spin" : ""} />
                        <p>{started ? formatTime(remainingSeconds ?? 0) : formatTime(Number(assessment.duration || 0))}</p>
                    </span>
                </header>

                <div className="relative">
                    <div className={`${!started && myUser.role === "applicant" ? "pointer-events-none select-none filter blur-sm min-h-[80vh]" : ""} transition-all`}>
                        <div className="flex flex-col gap-4">
                            {(!started && myUser.role === "applicant" ? assessment.questions.slice(0, 3) : assessment.questions).map((question) => (
                                <QuestionCard key={question.id} question={question} totalWeights={totalWeights} answers={answers} setAnswers={setAnswersAndRef} isStatic={myUser.role == "hr"} />
                            ))}
                        </div>
                    </div>

                    {!started && myUser.role === "applicant" && (
                        <div className="absolute inset-0 z-10 flex items-center justify-center scale-102">
                            <div className="w-full h-full bg-white/60 dark:bg-black/60 backdrop-blur-sm flex items-center justify-center">
                                <div className="text-center p-6 bg-white/90 dark:bg-gray-800 rounded shadow">
                                    <h4 className="text-lg font-semibold mb-2">Ready to start?</h4>
                                    <p className="text-sm text-gray-600 mb-4">When you start the assessment the timer will begin and questions will be revealed.</p>
                                    <div className="flex gap-3 justify-center">
                                        <Button variant="outline" onClick={() => Navigate(`/jobs/${jid}`)}>Cancel</Button>
                                        <Button onClick={() => setStarted(true)}>Start Assessment</Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </section>
            <footer className="mx-auto py-4">
                {myUser.role === "applicant" && (
                    <Button
                        disabled={!started || isSubmittingLoading || isSubmitted}
                        className="bg-indigo-600 text-white hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 disabled:opacity-50"
                        onClick={() => void handleSubmit(false)}
                    >
                        {isSubmitted ? "Submitting…" : "Submit Answers"}
                    </Button>
                )}
            </footer>
        </main>
    );
}