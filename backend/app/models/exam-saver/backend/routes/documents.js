const express = require("express");
const mongoose = require("mongoose");
const upload = require("../middleware/upload");
const Document = require("../models/Document");

const router = express.Router();

const VALID_TYPES = ["notes", "photos", "texts"];

/**
 * POST /upload
 * multipart/form-data body:
 *   file        - the uploaded file (required)
 *   type        - "notes" | "photos" | "texts" (required)
 *   name        - short title (required)
 *   description - what the item is (required)
 *   usage       - how/when it should be used (required)
 */
router.post("/upload", upload.single("file"), async (req, res) => {
  try {
    const { type, name, description, usage } = req.body;

    if (!req.file) {
      return res.status(400).json({ error: "A file is required." });
    }

    if (!type || !VALID_TYPES.includes(type)) {
      return res.status(400).json({
        error: `"type" must be one of: ${VALID_TYPES.join(", ")}`,
      });
    }

    if (!name || !description || !usage) {
      return res.status(400).json({
        error: "name, description, and usage are all required.",
      });
    }

    const document = await Document.create({
      type,
      name,
      description,
      usage,
      file_path: `/uploads/${req.file.filename}`,
    });

    return res.status(201).json(document.toJSON());
  } catch (err) {
    console.error("Upload failed:", err);
    return res.status(500).json({ error: "Upload failed." });
  }
});

/**
 * GET /documents?type=notes|photos|texts
 * Returns saved items, optionally filtered by category.
 * Read-only: this is the only way to list documents. There is no
 * update or delete route anywhere in this API.
 */
router.get("/documents", async (req, res) => {
  try {
    const { type } = req.query;

    if (type && !VALID_TYPES.includes(type)) {
      return res.status(400).json({
        error: `"type" must be one of: ${VALID_TYPES.join(", ")}`,
      });
    }

    const filter = type ? { type } : {};
    const documents = await Document.find(filter).sort({ created_at: -1 });

    return res.json(documents.map((doc) => doc.toJSON()));
  } catch (err) {
    console.error("Fetching documents failed:", err);
    return res.status(500).json({ error: "Could not fetch documents." });
  }
});

/**
 * GET /document/:id
 * Returns a single saved item by its id.
 */
router.get("/document/:id", async (req, res) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ error: "Invalid document id." });
    }

    const document = await Document.findById(id);

    if (!document) {
      return res.status(404).json({ error: "Document not found." });
    }

    return res.json(document.toJSON());
  } catch (err) {
    console.error("Fetching document failed:", err);
    return res.status(500).json({ error: "Could not fetch document." });
  }
});

module.exports = router;
