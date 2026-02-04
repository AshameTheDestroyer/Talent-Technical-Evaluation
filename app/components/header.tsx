"use client"

import { Button } from "./ui/button";
import { useSidebar } from "./ui/sidebar";
import { useState, useEffect } from "react";
import { MoonIcon, SidebarCloseIcon, SidebarOpenIcon, SunIcon } from "lucide-react";

export function Header() {
    const { state, toggleSidebar } = useSidebar();

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
        <header className="flex place-content-between p-4">
            <Button onClick={() => toggleSidebar()} variant="ghost" size="icon">
                {state == "collapsed" ? <SidebarOpenIcon /> : <SidebarCloseIcon />}
            </Button>
            <Button
                onClick={() => setDarkMode((v) => !v)}
                variant="ghost" size="icon" aria-pressed={darkMode}
            >
                {darkMode ? <SunIcon /> : <MoonIcon />}
            </Button>
        </header>
    );
}
