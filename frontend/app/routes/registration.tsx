import type { Route } from "./+types/registration";
import React, { useState } from "react";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import { HTTPManager } from "~/managers/HTTPManager";
import { useNavigate } from "react-router";
import { toast } from "react-toastify";
import { Combobox, ComboboxContent, ComboboxEmpty, ComboboxInput, ComboboxItem, ComboboxList } from "~/components/ui/combobox";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Registration" },
    {
      name: "description",
      content: "Login to access your account or create a new one.",
    },
  ];
}

export default function Registration() {
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    role: "hr",
    password: "",
  });

  const navigate = useNavigate();

  function update<K extends keyof typeof form>(k: K, v: typeof form[K]) {
    setForm((s) => ({ ...s, [k]: v }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      if (mode === "login") {
        const resp = await HTTPManager.post("/users/registration/login", {
          email: form.email,
          password: form.password,
        });
        const token = resp?.data?.token;
        if (token) {
          localStorage.setItem("token", token);
          toast.success("Logged in");
          navigate("/dashboard");
        } else {
          toast.error("Login succeeded but no token returned");
        }
      } else {
        const payload = {
          first_name: form.first_name,
          last_name: form.last_name,
          email: form.email,
          role: form.role,
          password: form.password,
        };
        const resp = await HTTPManager.post("/users/registration/signup", payload);
        const token = resp?.data?.token;
        if (token) {
          localStorage.setItem("token", token);
          toast.success("Account created");
          navigate("/dashboard");
        } else {
          toast.error("Signup succeeded but no token returned");
        }
      }
    } catch (err: any) {
      const message =
        err?.response?.data?.detail || err?.message || "Request failed";
      toast.error(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Welcome</h1>

      <div className="flex gap-2 mb-6">
        <Button variant={mode === "login" ? "default" : "outline"} onClick={() => setMode("login")}>Login</Button>
        <Button variant={mode === "signup" ? "default" : "outline"} onClick={() => setMode("signup")}>Sign up</Button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 bg-white dark:bg-gray-800 p-6 rounded shadow">
        {mode === "signup" && (
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm text-gray-700 dark:text-gray-300">First name</label>
              <Input value={form.first_name} onChange={(e) => update("first_name", e.target.value)} />
            </div>
            <div>
              <label className="text-sm text-gray-700 dark:text-gray-300">Last name</label>
              <Input value={form.last_name} onChange={(e) => update("last_name", e.target.value)} />
            </div>
          </div>
        )}

        <div>
          <label className="text-sm text-gray-700 dark:text-gray-300">Email</label>
          <Input type="email" value={form.email} onChange={(e) => update("email", e.target.value)} />
        </div>

        <div>
          <label className="text-sm text-gray-700 dark:text-gray-300">Password</label>
          <Input type="password" value={form.password} onChange={(e) => update("password", e.target.value)} />
        </div>

        {mode === "signup" && (
          <div>
            <label className="text-sm text-gray-700 dark:text-gray-300">Role</label>
            <Combobox items={["hr", "applicant"]} value={form.role} onValueChange={(value) => setForm((s) => ({ ...s, role: value as "hr" | "applicant" }))}>
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
            <select
              value={form.role}
              onChange={(e) => update("role", e.target.value as "hr" | "applicant")}
              className="mt-1 block w-full rounded-md border px-3 py-2"
            >
              <option value="hr">HR</option>
              <option value="applicant">Candidate</option>
            </select>
          </div>
        )}

        <div className="flex items-center justify-between gap-4">
          <Button variant="ghost" type="button" onClick={() => {
            setForm({ first_name: "", last_name: "", email: "", role: "hr", password: "" });
          }}>
            Clear
          </Button>
          <Button type="submit" disabled={loading}>
            {loading ? "Working…" : mode === "login" ? "Login" : "Create account"}
          </Button>
        </div>
      </form>
    </div>
  );
}