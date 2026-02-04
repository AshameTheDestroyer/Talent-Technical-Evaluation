import {
    Meta,
    Links,
    Outlet,
    Scripts,
    useLocation,
    ScrollRestoration,
    isRouteErrorResponse,
} from "react-router";
import { Avatar } from "radix-ui";
import type { Route } from "./+types/root";
import { Header } from "./components/header";
import { ToastContainer } from "react-toastify";
import { ThemeToggle } from "./components/theme-toggle";
import { SidebarProvider } from "./components/sidebar-provider";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import "./app.css";

export const queryClient = new QueryClient();

export function Layout({ children }: { children: React.ReactNode }) {
    const { pathname } = useLocation();

    if (!pathname.startsWith("/registration") && typeof window !== "undefined" && localStorage.getItem("token") === null) {
        window.location.replace("/registration");
    }

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
                <QueryClientProvider client={queryClient}>
                    {pathname.startsWith("/registration") ? (
                        <>
                            <header className="flex flex-row-reverse place-content-between p-4">
                                <ThemeToggle />
                            </header>
                            <main>{children}</main>
                        </>
                    ) : (
                        <SidebarProvider>
                            <Header />
                            <main>{children}</main>
                        </SidebarProvider>
                    )}
                </QueryClientProvider>
                <ToastContainer />
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
