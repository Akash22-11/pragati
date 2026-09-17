const mongoose = require("mongoose");

// A single saved item: a note, a photo, or a text file, plus the
// metadata the user filled in when uploading it.
const documentSchema = new mongoose.Schema(
  {
    type: {
      type: String,
      required: true,
      enum: ["notes", "photos", "texts"],
    },
    name: {
      type: String,
      required: true,
      trim: true,
    },
    description: {
      type: String,
      required: true,
      trim: true,
    },
    usage: {
      type: String,
      required: true,
      trim: true,
    },
    file_path: {
      type: String,
      required: true,
    },
    created_at: {
      type: Date,
      default: Date.now,
    },
  },
  {
    // No `updatedAt` timestamp is tracked on purpose: saved documents
    // are read-only after creation, so there is nothing to update.
    versionKey: false,
    toJSON: {
      transform: (_doc, ret) => {
        ret.id = ret._id.toString();
        delete ret._id;
        return ret;
      },
    },
  }
);

module.exports = mongoose.model("Document", documentSchema);
