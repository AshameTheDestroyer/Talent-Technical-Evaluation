import { cn } from "~/lib/utils";
import { HomeIcon } from "lucide-react";

export function Breadcrumbs() {
    const pathname =
        typeof window !== "undefined" ? window.location.pathname : "/";

    const segments = pathname.split("/").filter(Boolean);
    const crumbs = [
        { name: "/", href: "/", isEllipsis: false },
        ...segments.map((seg, i) => {
            const href = "/" + segments.slice(0, i + 1).join("/");
            const name = decodeURIComponent(seg)
                .replace(/-/g, " ")
                .replace(/\b\w/g, (c) => c.toUpperCase());
            return { name, href, isEllipsis: false };
        }),
    ];

    const displayCrumbs =
        crumbs.length > 4
            ? [
                  crumbs[0],
                  { name: "...", href: null, isEllipsis: true },
                  crumbs[crumbs.length - 2],
                  crumbs[crumbs.length - 1],
              ]
            : crumbs;

    return (
        <nav aria-label="Breadcrumb" className="flex items-center">
            <ol className="flex items-center gap-2 text-sm">
                {displayCrumbs.map((c, i, array) => (
                    <li
                        key={c.href ?? `ellipsis-${i}`}
                        className="flex items-center gap-2"
                    >
                        {c.isEllipsis ? (
                            <span className="text-muted-foreground">...</span>
                        ) : (
                            <a
                                href={i == 0 || i == array.length -1 ? undefined : c.href!}
                                className={cn(
                                    "text-ellipsis overflow-hidden whitespace-nowrap max-w-36",
                                    i > 0 && i < array.length - 1
                                        ? "font-medium hover:underline"
                                        : "text-muted-foreground"
                                )}
                                aria-current={
                                    i > 0 && i < array.length - 1
                                        ? "page"
                                        : undefined
                                }
                            >
                                {c.name == "/" ? <HomeIcon className="size-4" /> : c.name}
                            </a>
                        )}
                        {i < displayCrumbs.length - 1 && (
                            <span className="text-muted-foreground">/</span>
                        )}
                    </li>
                ))}
            </ol>
        </nav>
    );
}
