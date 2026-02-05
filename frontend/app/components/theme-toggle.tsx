import { Button } from "./ui/button";
import { useEffect, useState } from "react";
import { MoonIcon, SunIcon } from "lucide-react";

export function ThemeToggle() {
    const [darkMode, setDarkMode] = useState<boolean>(() => {
        try {
            const stored = localStorage.getItem("theme");
            if (stored) return stored === "dark";
            return (
                typeof window !== "undefined" &&
                window.matchMedia?.("(prefers-color-scheme: dark)")?.matches
            );
        } catch {
            return false;
        }
    });

    useEffect(() => {
        try {
            const root = document.documentElement;
            if (darkMode) root.classList.add("dark");
            else root.classList.remove("dark");
            localStorage.setItem("theme", darkMode ? "dark" : "light");
        } catch {}
    }, [darkMode]);

    return (
        <Button
            onClick={() => setDarkMode((v) => !v)}
            variant="ghost" size="icon" aria-pressed={darkMode}
        >
            {darkMode ? <SunIcon /> : <MoonIcon />}
        </Button>
    );
}