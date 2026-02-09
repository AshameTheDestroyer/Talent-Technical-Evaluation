import { Button } from "./ui/button";
import { useSidebar } from "./ui/sidebar";
import { Breadcrumbs } from "./breadcrumbs";
import { ThemeToggle } from "./theme-toggle";
import { SidebarCloseIcon, SidebarOpenIcon } from "lucide-react";

export function Header() {
    const { state, toggleSidebar } = useSidebar();

    return (
        <header className="flex place-content-between gap-2 p-4 [&>nav]:mr-auto place-items-center">
            <Button onClick={() => toggleSidebar()} variant="ghost" size="icon">
                {state == "collapsed" ? (
                    <SidebarOpenIcon />
                ) : (
                    <SidebarCloseIcon />
                )}
            </Button>
            <Breadcrumbs />
            <ThemeToggle />
        </header>
    );
}