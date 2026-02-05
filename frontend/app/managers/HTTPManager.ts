import axios from "axios";
import { toast } from "react-toastify";

export const HTTPManager = axios.create({
    baseURL: import.meta.env.VITE_APP_API_URL,
    headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
});

HTTPManager.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    toast.error("Request error: " + error.message);
    return Promise.reject(error);
});