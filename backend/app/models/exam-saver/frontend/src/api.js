import axios from "axios";

// Set VITE_API_URL in a .env file to point at a deployed backend.
// Falls back to a local server for development.
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

const client = axios.create({ baseURL: BASE_URL });

/**
 * Upload a file plus its metadata.
 * @param {{ file: File, type: string, name: string, description: string, usage: string }} payload
 */
export async function uploadDocument({ file, type, name, description, usage }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("type", type);
  formData.append("name", name);
  formData.append("description", description);
  formData.append("usage", usage);

  const { data } = await client.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

/**
 * Fetch saved items, optionally filtered by category.
 * @param {"notes"|"photos"|"texts"} type
 */
export async function getDocuments(type) {
  const { data } = await client.get("/documents", { params: { type } });
  return data;
}

/**
 * Fetch a single saved item by id.
 * @param {string} id
 */
export async function getDocument(id) {
  const { data } = await client.get(`/document/${id}`);
  return data;
}

/**
 * Build the absolute URL for a stored file so it can be previewed
 * or downloaded directly in the browser.
 * @param {string} filePath - the file_path returned by the API, e.g. "/uploads/abc.png"
 */
export function fileUrl(filePath) {
  return `${BASE_URL}${filePath}`;
}
