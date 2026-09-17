require("dotenv").config();
const express = require("express");
const cors = require("cors");
const path = require("path");

const connectDB = require("./config/db");
const documentRoutes = require("./routes/documents");

const app = express();

connectDB();

const allowedOrigins = (process.env.CLIENT_ORIGIN || "http://localhost:5173")
  .split(",")
  .map((origin) => origin.trim());

app.use(cors({ origin: allowedOrigins }));
app.use(express.json());

// Serve uploaded files statically so the frontend can preview/download them
// directly, e.g. http://localhost:5000/uploads/<filename>
app.use("/uploads", express.static(path.join(__dirname, "uploads")));

app.use("/", documentRoutes);

app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Exam Saver API running on http://localhost:${PORT}`);
});
