import { Avatar } from "radix-ui";
import { Button } from "./ui/button";
import { toast } from "react-toastify";
import { Link, useLocation } from "react-router";
import { HTTPManager } from "~/managers/HTTPManager";
import { useGetMyUser } from "~/services/useGetMyUser";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";
import { Building2Icon, FilesIcon, LayoutDashboardIcon } from "lucide-react";
import { Sidebar, SidebarContent, SidebarFooter, SidebarHeader, SidebarInset, SidebarProvider as SidebarProvider_ } from "./ui/sidebar";

const LINKS = [
    { title: "Jobs", to: "/jobs", icon: Building2Icon },
    { title: "Dashboard", to: "/dashboard", icon: LayoutDashboardIcon, role: "hr" },
    { title: "My Applications", to: "/my-applications", icon: FilesIcon, role: "applicant" },
]

export function SidebarProvider({ children }: { children: React.ReactNode }) {
    const { pathname } = useLocation();
    const { data: myUser } = useGetMyUser();

    function handleLogout() {
        HTTPManager.post("/users/registration/logout", {}).then(() => {
            localStorage.removeItem("token");
            if (typeof window !== "undefined") {
                window.location.replace("/registration");
            }
        }).catch(error => toast.error("Logout failed: " + error?.message || "Unknown error"));
    }

    return (
        <SidebarProvider_>
            <Sidebar collapsible="icon" className="p-4  bg-indigo-100 dark:bg-slate-950">
                <SidebarHeader className="mb-4 group-data-[collapsible=icon]:hidden border-b-2 border-indigo-300 dark:border-slate-700 pb-4">
                    <h1 className="font-bold text-ellipsis overflow-hidden whitespace-nowrap">Talent Technical Evaluation</h1>
                </SidebarHeader>
                <SidebarContent>
                    {LINKS.filter(link => !link.role || link.role === myUser?.role).map(({title,to,icon: Icon}, i) => (
                        <Link
                            key={i}
                            to={to}
                            title={title}
                            className={`flex place-items-center group-data-[collapsible=icon]:place-content-center gap-2 px-4 py-2 group-data-[collapsible=icon]:p-0 group-data-[collapsible=icon]:size-8 group-data-[collapsible=icon]:-mx-2 hover:bg-indigo-200 dark:hover:bg-slate-800 rounded-md ${pathname.startsWith(to) ? "bg-indigo-300 dark:bg-slate-700" : ""}`}
                        >
                            <Icon />{" "}
                            <span className="group-data-[collapsible=icon]:hidden">{title}</span>
                        </Link>
                    ))}
                </SidebarContent>
                <SidebarFooter>
                    {myUser && (
                        <div className="group-data-[collapsible=icon]:-mx-4 flex gap-2">
                            <Popover>
                                <PopoverTrigger>
                                    <Avatar.Avatar className="shrink-0 cursor-pointer" tabIndex={0}>
                                        {/* <Avatar.AvatarImage
                                            src="https://github.com/ashamethedestroyer.png"
                                            alt="@ashamethedestroyer"
                                            className="size-10 rounded-full group-data-[collapsible=icon]:size-8"
                                        /> */}
                                        <Avatar.AvatarFallback className="rounded-full bg-indigo-200 dark:bg-gray-800 size-10 group-data-[collapsible=icon]:size-8 flex items-center justify-center">
                                            {myUser ? `${myUser.first_name[0]}${myUser.last_name[0]}` : "U"}
                                        </Avatar.AvatarFallback>
                                    </Avatar.Avatar>
                                </PopoverTrigger>
                                <PopoverContent className="w-min p-0">
                                    <Button variant="ghost" className="w-full text-left" onClick={handleLogout}>
                                        Logout
                                    </Button>
                                </PopoverContent>
                            </Popover>
                            <div className="overflow-hidden group-data-[collapsible=icon]:hidden">
                                <p className="font-bold whitespace-nowrap text-ellipsis overflow-hidden text-start">
                                    {myUser.first_name} {myUser.last_name}
                                </p>
                                <p className="whitespace-nowrap text-ellipsis overflow-hidden">
                                    {myUser.email}
                                </p>
                            </div>
                        </div>
                    )}
                </SidebarFooter>
            </Sidebar>
            <SidebarInset className="flex flex-col h-screen">
                {children}
            </SidebarInset>
        </SidebarProvider_>
    );
}
