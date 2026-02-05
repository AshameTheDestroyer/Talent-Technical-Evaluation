"use client"

import { Button } from "./ui/button";
import { useSidebar } from "./ui/sidebar";
import { ThemeToggle } from "./theme-toggle";
import { SidebarCloseIcon, SidebarOpenIcon } from "lucide-react";

export function Header() {
    const { state, toggleSidebar } = useSidebar();

    return (
        <header className="flex place-content-between p-4">
            <Button onClick={() => toggleSidebar()} variant="ghost" size="icon">
                {state == "collapsed" ? <SidebarOpenIcon /> : <SidebarCloseIcon />}
            </Button>
            <ThemeToggle />
        </header>
    );
}
