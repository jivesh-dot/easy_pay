import axios from 'axios';

const base = import.meta.env.VITE_BASE_URL;
const backendPort = import.meta.env.VITE_BACKEND_PORT || '8000';
const frontendPort = import.meta.env.VITE_FRONTEND_PORT || '5173';

export const frontEndUrl = `${base}:${frontendPort}`;
export const backendEndUrl = `${base}:${backendPort}`;

console.info(`frontEndUrl = ${frontEndUrl}`);
console.info(`backendEndUrl = ${backendEndUrl}`);

export const api = axios.create({ baseURL: `${backendEndUrl}/api/v1` });