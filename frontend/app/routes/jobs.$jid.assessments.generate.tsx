import { Label } from "radix-ui";
import { toast } from "react-toastify";
import React, { useState } from "react";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { Checkbox } from "~/components/ui/checkbox";
import { Textarea } from "~/components/ui/textarea";
import { useNavigate, useParams } from "react-router";
import type { Route } from "./+types/jobs.$jid.assessments.generate";
import { usePostJobAssessment } from "~/services/usePostJobAssessment";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Generate New Assessment" },
        {
            name: "description",
            content: "Generate a new assessment for the job listing.",
        },
    ];
}

export default function AssessmentGenerateRoute() {
    const { jid } = useParams();
    const navigate = useNavigate();
    const mutation = usePostJobAssessment();

    const [form, setForm] = useState({
        title: "",
        passing_score: 70,
        additional_note: "",
        questions_types: [] as Array<
            "text_based" | "choose_one" | "choose_many"
        >,
    });

    function toggleType(t: "text_based" | "choose_one" | "choose_many") {
        setForm((s) => {
            const exists = s.questions_types.includes(t);
            return {
                ...s,
                questions_types: exists
                    ? s.questions_types.filter((x) => x !== t)
                    : [...s.questions_types, t],
            };
        });
    }

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (!jid) {
            toast.error("Missing job id");
            return;
        }
        if (!form.title.trim()) {
            toast.error("Title is required");
            return;
        }
        if (form.passing_score < 0 || form.passing_score > 100) {
            toast.error("Passing score must be between 0 and 100");
            return;
        }
        if (form.questions_types.length === 0) {
            toast.error("Select at least one question type");
            return;
        }

        try {
            await mutation.mutateAsync({
                jid,
                body: {
                    title: form.title.trim(),
                    passing_score: form.passing_score,
                    questions_types: form.questions_types,
                    additional_note: form.additional_note.trim(),
                },
            });
            toast.success("Assessment generated");
            navigate(`/jobs/${jid}`);
        } catch (err: any) {
            const message =
                err?.response?.data?.detail ||
                err?.message ||
                "Failed to generate assessment";
            toast.error(message);
        }
    }

    return (
        <div className="max-w-2xl mx-auto p-6">
            <h1 className="text-2xl font-semibold mb-4">Create Assessment</h1>

            <form
                onSubmit={handleSubmit}
                className="space-y-4 bg-white dark:bg-gray-800 p-6 rounded shadow"
            >
                <div>
                    <label className="text-sm text-gray-700 dark:text-gray-300">
                        Title
                    </label>
                    <Input
                        value={form.title}
                        onChange={(e) =>
                            setForm((s) => ({ ...s, title: e.target.value }))
                        }
                        placeholder="Technical Screening - Frontend"
                    />
                </div>

                <div>
                    <label className="text-sm text-gray-700 dark:text-gray-300">
                        Passing Score
                    </label>
                    <Input
                        type="number"
                        value={String(form.passing_score)}
                        onChange={(e) =>
                            setForm((s) => ({
                                ...s,
                                passing_score: Number(e.target.value || 0),
                            }))
                        }
                        placeholder="70"
                        min={0}
                        max={100}
                    />
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        Enter a number between 0 and 100.
                    </p>
                </div>

                <div>
                    <label className="text-sm text-gray-700 dark:text-gray-300">
                        Additional Note
                    </label>
                    <Textarea
                        value={form.additional_note}
                        onChange={(e) =>
                            setForm((s) => ({
                                ...s,
                                additional_note: e.target.value,
                            }))
                        }
                        placeholder="Optional note for candidates"
                    />
                </div>

                <div>
                    <label className="text-sm text-gray-700 dark:text-gray-300">
                        Question Types
                    </label>
                    <div className="flex gap-3 mt-2">
                        {[
                            { label: "Text Based", value: "text_based" },
                            { label: "Choose One", value: "choose_one" },
                            { label: "Choose Many", value: "choose_many" },
                        ].map((option, i) => (
                            <div key={i} className="flex items-center gap-3">
                                <Checkbox
                                    id={`${option.value}-option`}
                                    className="cursor-pointer"
                                    value={
                                        form.questions_types.includes(
                                            option.value as any,
                                        ) as any
                                    }
                                    onCheckedChange={() =>
                                        toggleType(option.value as any)
                                    }
                                />
                                <Label.Label
                                    htmlFor={`${option.value}-option`}
                                    className="cursor-pointer"
                                >
                                    {option.label}
                                </Label.Label>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="flex items-center gap-3 place-content-end">
                    <Button
                        variant="outline"
                        type="button"
                        onClick={() =>
                            setForm({
                                title: "",
                                passing_score: 70,
                                additional_note: "",
                                questions_types: [],
                            })
                        }
                    >
                        Clear
                    </Button>
                    <Button type="submit" disabled={mutation.isPending}>
                        {mutation.isPending
                            ? "Creating…"
                            : "Generate Assessment"}
                    </Button>
                </div>

                {mutation.isError && (
                    <div className="text-sm text-red-500">
                        Error:{" "}
                        {(mutation.error as any)?.message ??
                            "An error occurred"}
                    </div>
                )}
            </form>
        </div>
    );
}
