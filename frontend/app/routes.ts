import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
	index("routes/home.tsx"),
	route("jobs", "routes/jobs.tsx"),
	route("jobs/create", "routes/jobs.create.tsx"),
	route("jobs/:id", "routes/jobs.$id.tsx"),
	route("jobs/:jid/assessments/:id", "routes/jobs.$jid.assessments.$id.tsx"),
	route("jobs/:jid/assessment/:aid/applications", "routes/jobs.$jid.assessment.$aid.applications.tsx"),
	route("dashboard", "routes/dashboard.tsx"),
	route("registration", "routes/registration.tsx"),
] satisfies RouteConfig;
