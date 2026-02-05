import { XIcon } from "lucide-react";
import { toast } from "react-toastify";
import React, { useState } from "react";
import { useNavigate } from "react-router";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import type { Route } from "./+types/jobs.create";
import { Textarea } from "~/components/ui/textarea";
import { usePostJob, type PostJobPayload } from "~/services/usePostJob";
import { Combobox, ComboboxContent, ComboboxEmpty, ComboboxInput, ComboboxItem, ComboboxList } from "~/components/ui/combobox";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Create New Job" },
        {
            name: "description",
            content: "Create a new job listing and find the perfect candidate!",
        },
    ];
}

export default function JobsCreateRoute() {
    const navigate = useNavigate();
    const mutation = usePostJob();

    const [form, setForm] = useState<PostJobPayload & { skill_categories_raw: string }>({
        title: "",
        description: "",
        seniority: "intern",
        skill_categories: [],
        skill_categories_raw: "",
    } as any);

    function update<K extends keyof typeof form>(k: K, v: typeof form[K]) {
        setForm((s) => ({ ...s, [k]: v }));
    }

    async function handleSubmit(e: React.SubmitEvent) {
        e.preventDefault();

        if (!form.title.trim()) {
            toast.error("Title is required");
            return;
        }
        if (!form.description.trim()) {
            toast.error("Description is required");
            return;
        }

        const payload: PostJobPayload = {
            title: form.title.trim(),
            description: form.description.trim(),
            seniority: form.seniority,
            skill_categories: form.skill_categories_raw
                .split(",")
                .map((s) => s.trim())
                .filter(Boolean),
        };

        try {
            await mutation.mutateAsync(payload);
            toast.success("Job created");
            navigate("/jobs");
        } catch (err: any) {
            const message = err?.response?.data?.detail || err?.message || "Failed to create job";
            toast.error(message);
        }
    }

    return (
        <div className="max-w-3xl mx-auto p-6">
            <h1 className="text-2xl font-semibold mb-4">Create New Job</h1>

            <form onSubmit={handleSubmit} className="space-y-4 bg-white dark:bg-gray-800 p-6 rounded shadow">
                <div className="flex flex-col gap-2">
                    <label className="text-gray-700 dark:text-gray-300">Title</label>
                    <Input value={form.title} onChange={(e) => update("title", e.target.value)} placeholder="Senior Frontend Engineer" />
                </div>

                <div className="flex flex-col gap-2">
                    <label className="text-gray-700 dark:text-gray-300">Description</label>
                    <Textarea value={form.description} onChange={(e) => update("description", e.target.value)} placeholder="Describe the role, responsibilities and expectations" />
                </div>

                <div className="flex flex-col gap-2">
                    <label className="text-gray-700 dark:text-gray-300">Seniority</label>
                    <Combobox items={["intern", "junior", "mid", "senior"]} value={form.seniority} onValueChange={(value) => update("seniority", value as any)}>
                        <ComboboxInput placeholder="Choose value" />
                        <ComboboxContent>
                            <ComboboxEmpty>No items found.</ComboboxEmpty>
                            <ComboboxList>
                                {(item) => (
                                    <ComboboxItem key={item} value={item}>
                                        {item}
                                    </ComboboxItem>
                                )}
                            </ComboboxList>
                        </ComboboxContent>
                    </Combobox>
                </div>

                <div className="flex flex-col gap-2">
                    <label className="text-gray-700 dark:text-gray-300">Skill categories (comma separated)</label>
                    <div className="flex flex-wrap gap-2">
                        {form.skill_categories.map((skill) => (
                            <span
                                key={skill}
                                className="inline-flex items-center gap-2 px-3 py-1.5 bg-gray-100 dark:bg-gray-700 text-sm rounded-full"
                            >
                                <span>{skill}</span>
                                <Button
                                    type="button"
                                    variant="ghost"
                                    className="text-xs h-6 w-6 text-gray-600 dark:text-gray-300 hover:text-red-500 dark:hover:text-red-500"
                                    onClick={() => {
                                        const next = form.skill_categories.filter((s) => s !== skill);
                                        update("skill_categories", next as any);
                                        update("skill_categories_raw", next.join(", ") as any);
                                    }}
                                >
                                    <XIcon className="size-4" />
                                </Button>
                            </span>
                        ))}
                    </div>
                    <SkillInput form={form} update={update} />
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Enter skills separated by commas; they will be saved as an array.</p>
                </div>

                <div className="flex items-center gap-3 place-content-end">
                    <Button variant="outline" type="button" onClick={() => {
                        setForm({ title: "", description: "", seniority: "junior", skill_categories: [], skill_categories_raw: "" } as any);
                    }}>
                        Clear
                    </Button>
                    <Button type="submit" disabled={mutation.isPending}>
                        {mutation.isPending ? "Creating…" : "Create Job"}
                    </Button>
                </div>

                {mutation.isError && <div className="text-sm text-red-500">Error: {(mutation.error as any)?.message ?? "An error occurred"}</div>}
            </form>
        </div>
    );
}

function SkillInput({ form, update } : { form: PostJobPayload & { skill_categories_raw: string; }, update: <K extends keyof PostJobPayload | "skill_categories_raw">(k: K, v: (PostJobPayload & { skill_categories_raw: string; })[K]) => void }) {
    const [skillInput, setSkillInput] = useState("");

    function addFromInput(raw: string) {
        const parts = raw
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean);
        if (parts.length === 0) return;
        const next = Array.from(new Set([...form.skill_categories, ...parts]));
        update("skill_categories", next as any);
        update("skill_categories_raw", next.join(", ") as any);
        setSkillInput("");
    }

    return (
        <Input
            className="w-full border rounded px-3 py-2 bg-white dark:bg-gray-800"
            placeholder="Add a skill and press Enter (or type comma)"
            value={skillInput}
            onChange={(e) => setSkillInput(e.target.value)}
            onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === ",") {
                    e.preventDefault();
                    addFromInput(skillInput);
                } else if (e.key === "Backspace" && !skillInput && form.skill_categories.length) {
                    const next = form.skill_categories.slice(0, -1);
                    update("skill_categories", next as any);
                    update("skill_categories_raw", next.join(", ") as any);
                }
            } }
            onBlur={() => {
                if (skillInput.trim()) addFromInput(skillInput);
            } } />
    );
}