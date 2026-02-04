import {
    Link,
    Meta,
    Links,
    Outlet,
    Scripts,
    ScrollRestoration,
    isRouteErrorResponse,
} from "react-router";
import { Avatar } from "radix-ui";
import type { Route } from "./+types/root";
import { Header } from "./components/header";
import { Building2Icon, LayoutDashboardIcon } from "lucide-react";
import { Sidebar, SidebarContent, SidebarFooter, SidebarInset, SidebarProvider } from "./components/ui/sidebar";

import "./app.css";

export function Layout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <head>
                <meta charSet="utf-8" />
                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1"
                />
                <link rel="icon" href="/favicon.png" />
                <Meta />
                <Links />
            </head>
            <body>
                <SidebarProvider>
                    <Sidebar collapsible="icon">
                        <SidebarContent className="p-4">
                            <Link to="/" title="Jobs" className="flex place-items-center group-data-[collapsible=icon]:place-content-center gap-2 px-4 py-2 group-data-[collapsible=icon]:p-0 group-data-[collapsible=icon]:size-8 group-data-[collapsible=icon]:-mx-2 hover:bg-gray-200 dark:hover:bg-gray-800 rounded-md">
                                <Building2Icon /> <span className="group-data-[collapsible=icon]:hidden">Jobs</span>
                            </Link>
                            <Link to="/dashboard" title="Dashboard" className="flex place-items-center group-data-[collapsible=icon]:place-content-center gap-2 px-4 py-2 group-data-[collapsible=icon]:p-0 group-data-[collapsible=icon]:size-8 group-data-[collapsible=icon]:-mx-2 hover:bg-gray-200 dark:hover:bg-gray-800 rounded-md">
                                <LayoutDashboardIcon /> <span className="group-data-[collapsible=icon]:hidden">Dashboard</span>
                            </Link>
                        </SidebarContent>
                        <SidebarFooter className="p-4">
                            <div className="group-data-[collapsible=icon]:-mx-2 flex gap-2">
                               <Avatar.Avatar className="shrink-0">
                                    <Avatar.AvatarImage
                                        src="https://github.com/ashamethedestroyer.png"
                                        alt="@ashamethedestroyer"
                                        className="size-10 rounded-full group-data-[collapsible=icon]:size-8"
                                    />
                                    <Avatar.AvatarFallback className="rounded-full bg-gray-200 dark:bg-gray-800 size-10 group-data-[collapsible=icon]:size-8 flex items-center justify-center">A</Avatar.AvatarFallback>
                                </Avatar.Avatar>
                                <div className="overflow-hidden group-data-[collapsible=icon]:hidden">
                                    <p className="font-bold whitespace-nowrap text-ellipsis overflow-hidden">Hashem Wannous</p>
                                    <p className="whitespace-nowrap text-ellipsis overflow-hidden">@ashamethedestroyer</p>
                                </div>
                            </div>
                        </SidebarFooter>
                    </Sidebar>
                    <SidebarInset className="flex flex-col h-screen">
                        <Header />
                        <main>{children}</main>
                    </SidebarInset>
                </SidebarProvider>
                <ScrollRestoration />
                <Scripts />
            </body>
        </html>
    );
}

export default function App() {
    return <Outlet />;
}

export function ErrorBoundary({ error }: Route.ErrorBoundaryProps) {
    let message = "Oops!";
    let details = "An unexpected error occurred.";
    let stack: string | undefined;

    if (isRouteErrorResponse(error)) {
        message = error.status === 404 ? "404" : "Error";
        details =
            error.status === 404
                ? "The requested page could not be found."
                : error.statusText || details;
    } else if (import.meta.env.DEV && error && error instanceof Error) {
        details = error.message;
        stack = error.stack;
    }

    return (
        <main className="flex flex-col items-center justify-center p-8">
            <h1>{message}</h1>
            <p>{details}</p>
            {stack && (
                <pre className="w-full p-4 overflow-x-auto">
                    <code>{stack}</code>
                </pre>
            )}
        </main>
    );
}
