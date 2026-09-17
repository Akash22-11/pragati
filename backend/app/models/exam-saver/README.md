# Exam Saver

A read-only study material vault. Upload **Notes**, **Photos**, and **Texts**
with metadata (name, description, usage), then browse and search them. Once
saved, an item can never be edited or deleted through the app — it can only
be viewed.

```
exam-saver/
├── backend/     Express API + MongoDB (Mongoose) + Multer file storage
├── frontend/    React + Vite + TailwindCSS
└── README.md
```

---

## 1. Prerequisites

- Node.js 18+ and npm
- A MongoDB instance — either:
  - Local MongoDB running on `mongodb://127.0.0.1:27017`, or
  - A free [MongoDB Atlas](https://www.mongodb.com/atlas) cluster

---

## 2. Run the backend locally

```bash
cd backend
npm install
cp .env.example .env
# edit .env and set MONGO_URI if you're not using the local default
npm start
```

The API starts on `http://localhost:5000`. Uploaded files are written to
`backend/uploads/` and served back at `http://localhost:5000/uploads/<file>`.

`npm run dev` uses `nodemon` for auto-restart during development.

---

## 3. Run the frontend locally

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env
# edit .env if your backend isn't on http://localhost:5000
npm run dev
```

The app opens on `http://localhost:5173`.

---

## 4. API reference

Base URL: `http://localhost:5000` (or your deployed backend URL).

There are exactly three endpoints. There is intentionally **no** update or
delete endpoint — saved documents are permanent and read-only.

### `POST /upload`

Uploads a file plus its required metadata. `multipart/form-data` body:

| field         | type   | required | notes                              |
|---------------|--------|----------|-------------------------------------|
| `file`        | file   | yes      | the note/photo/text file itself     |
| `type`        | string | yes      | `notes` \| `photos` \| `texts`      |
| `name`        | string | yes      | short title                         |
| `description` | string | yes      | what the item is                    |
| `usage`       | string | yes      | how/when to use it                  |

Example call from the frontend (see `frontend/src/api.js`):

```js
const formData = new FormData();
formData.append("file", file);
formData.append("type", "notes");
formData.append("name", "Algebra formulas");
formData.append("description", "Key formulas for the algebra exam");
formData.append("usage", "Review the night before the test");

const res = await fetch("http://localhost:5000/upload", {
  method: "POST",
  body: formData,
});
const savedDocument = await res.json();
```

Response `201 Created`:

```json
{
  "id": "66bf1a2c9f1b2a0012a3c456",
  "type": "notes",
  "name": "Algebra formulas",
  "description": "Key formulas for the algebra exam",
  "usage": "Review the night before the test",
  "file_path": "/uploads/3f6e2b91-....png",
  "created_at": "2026-09-05T12:00:00.000Z"
}
```

### `GET /documents?type=notes|photos|texts`

Returns saved items, most recent first. Omit `type` to get every category.

```js
const res = await fetch("http://localhost:5000/documents?type=photos");
const photos = await res.json();
```

### `GET /document/:id`

Returns a single saved item.

```js
const res = await fetch(`http://localhost:5000/document/${id}`);
const document = await res.json();
```

---

## 5. Database

MongoDB collection: **`documents`**

| field         | type                              |
|---------------|------------------------------------|
| `id`          | string (Mongo `_id`)               |
| `type`        | `"notes"` \| `"photos"` \| `"texts"` |
| `name`        | string                             |
| `description` | string                             |
| `usage`       | string                             |
| `file_path`   | string (e.g. `/uploads/abc.png`)   |
| `created_at`  | date                                |

Schema lives in `backend/models/Document.js`. No update route or model method
touches an existing document after creation.

---

## 6. Storage

Files are saved to `backend/uploads/` via Multer (see
`backend/middleware/upload.js`), with a UUID-prefixed filename to avoid
collisions. The stored `file_path` (e.g. `/uploads/<uuid>.png`) is what gets
written to MongoDB, and the backend serves that folder statically so the
frontend can preview or download the original file.

**Optional: AWS S3.** To use S3 instead of local disk, swap the Multer
`diskStorage` engine in `backend/middleware/upload.js` for
[`multer-s3`](https://www.npmjs.com/package/multer-s3), and store the
resulting S3 object URL in `file_path` instead of a local path. No other code
needs to change, since the rest of the app only ever reads `file_path` as a
URL.

---

## 7. Authentication

Not included. Exam Saver ships open/unauthenticated for personal use, as
specified. If you need private access later, add a JWT-based login layer in
front of the existing routes without changing their behavior.

---

## 8. Deployment

- **Backend:** deploy `backend/` as a standard Node server (e.g. Render,
  Railway, Fly.io, or your own VM). Set `MONGO_URI` and `CLIENT_ORIGIN`
  environment variables. Make sure the `uploads/` folder is on persistent
  storage (or switch to S3 — see above — if your host has an ephemeral
  filesystem).
- **Frontend:** deploy `frontend/` to Vercel or Netlify. Set the
  `VITE_API_URL` environment variable to your deployed backend's URL, then
  run the standard `npm run build` (Vercel/Netlify do this automatically).
- **Database:** use a [MongoDB Atlas](https://www.mongodb.com/atlas) cluster
  and put its connection string in `MONGO_URI`.

---

## What this app deliberately does not have

- No edit or delete functionality anywhere — uploaded items are permanent.
- No categories beyond Notes, Photos, and Texts.
- No comments, likes, chat, or other social features.
- No SQL database — MongoDB only.
