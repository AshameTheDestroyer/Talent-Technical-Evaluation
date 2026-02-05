import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
	index("routes/home.tsx"),
	route("jobs", "routes/jobs.tsx"),
	route("jobs/:id", "routes/jobs.$id.tsx"),
] satisfies RouteConfig;
