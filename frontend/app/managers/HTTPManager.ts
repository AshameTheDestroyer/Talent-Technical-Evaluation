import axios from "axios";
import { toast } from "react-toastify";

// Use runtime configuration with fallback to environment variable
// Handle SSR by checking if window is available
const getBaseURL = () => {
    if (typeof window !== 'undefined' && (window as any).APP_CONFIG?.API_BASE_URL) {
        return (window as any).APP_CONFIG.API_BASE_URL;
    }
    // Fallback to environment variable during build time
    return import.meta.env.VITE_APP_API_URL || undefined;
};

const baseURL = getBaseURL();

export const HTTPManager = axios.create({
    baseURL: baseURL,
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