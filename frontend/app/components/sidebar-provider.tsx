import { Avatar } from "radix-ui";
import { Link, useLocation } from "react-router";
import { Building2Icon, LayoutDashboardIcon } from "lucide-react";
import { Sidebar, SidebarContent, SidebarFooter, SidebarHeader, SidebarInset, SidebarProvider as SidebarProvider_ } from "./ui/sidebar";

const LINKS = [
    { title: "Jobs", to: "/", icon: Building2Icon },
    { title: "Dashboard", to: "/dashboard", icon: LayoutDashboardIcon },
]

export function SidebarProvider({ children }: { children: React.ReactNode }) {
    const { pathname } = useLocation();
    return (
        <SidebarProvider_>
            <Sidebar collapsible="icon" className="p-4  bg-indigo-100 dark:bg-slate-950">
                <SidebarHeader className="mb-4 group-data-[collapsible=icon]:hidden border-b-2 border-indigo-300 dark:border-slate-700 pb-4">
                    <h1 className="font-bold text-ellipsis overflow-hidden whitespace-nowrap">Talent Technical Evaluation</h1>
                </SidebarHeader>
                <SidebarContent>
                    {LINKS.map(({title,to,icon: Icon}, i) => (
                        <Link
                            key={i}
                            to={to}
                            title={title}
                            className={`flex place-items-center group-data-[collapsible=icon]:place-content-center gap-2 px-4 py-2 group-data-[collapsible=icon]:p-0 group-data-[collapsible=icon]:size-8 group-data-[collapsible=icon]:-mx-2 hover:bg-indigo-200 dark:hover:bg-slate-800 rounded-md ${pathname === to ? "bg-indigo-300 dark:bg-slate-700" : ""}`}
                        >
                            <Icon />{" "}
                            <span className="group-data-[collapsible=icon]:hidden">{title}</span>
                        </Link>
                    ))}
                </SidebarContent>
                <SidebarFooter>
                    <div className="group-data-[collapsible=icon]:-mx-4 flex gap-2">
                        <Avatar.Avatar className="shrink-0">
                            <Avatar.AvatarImage
                                src="https://github.com/ashamethedestroyer.png"
                                alt="@ashamethedestroyer"
                                className="size-10 rounded-full group-data-[collapsible=icon]:size-8"
                            />
                            <Avatar.AvatarFallback className="rounded-full bg-gray-200 dark:bg-gray-800 size-10 group-data-[collapsible=icon]:size-8 flex items-center justify-center">
                                A
                            </Avatar.AvatarFallback>
                        </Avatar.Avatar>
                        <div className="overflow-hidden group-data-[collapsible=icon]:hidden">
                            <p className="font-bold whitespace-nowrap text-ellipsis overflow-hidden">
                                Hashem Wannous
                            </p>
                            <p className="whitespace-nowrap text-ellipsis overflow-hidden">
                                @ashamethedestroyer
                            </p>
                        </div>
                    </div>
                </SidebarFooter>
            </Sidebar>
            <SidebarInset className="flex flex-col h-screen">
                {children}
            </SidebarInset>
        </SidebarProvider_>
    );
}
