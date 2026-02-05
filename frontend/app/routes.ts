import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
	index("routes/home.tsx"),
	route("jobs", "routes/jobs.tsx"),
	route("jobs/create", "routes/jobs.create.tsx"),
	route("jobs/:id", "routes/jobs.$id.tsx"),
	route("jobs/:jid/assessments/generate", "routes/jobs.$jid.assessments.generate.tsx"),
	route("jobs/:jid/assessments/:id", "routes/jobs.$jid.assessments.$id.tsx"),
	route("jobs/:jid/assessments/:aid/applications", "routes/jobs.$jid.assessments.$aid.applications.tsx"),
	route("jobs/:jid/assessments/:aid/applications/:id", "routes/jobs.$jid.assessments.$aid.applications.$id.tsx"),
	route("dashboard", "routes/dashboard.tsx"),
	route("registration", "routes/registration.tsx"),
] satisfies RouteConfig;
