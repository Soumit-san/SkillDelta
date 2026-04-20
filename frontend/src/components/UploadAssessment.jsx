import { useState } from "react";
import api from "../services/api";

export default function UploadAssessment({ id, onWeakTopics }) {
  const [file, setFile] = useState(null);

  const upload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      // ✅ FIXED ROUTE
      const res = await api.post(`/assessment/${id}`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      onWeakTopics(res.data.weak_topics || []);
    } catch (err) {
      console.log("Assessment upload error:", err.response?.data);
    }
  };

  return (
    <div className="p-6 bg-white/10 backdrop-blur-xl rounded-2xl">
      <h2 className="text-2xl mb-3">Upload Assessment</h2>

      <input
        type="file"
        accept=".pdf,.png,.jpg,.jpeg,.csv,.docx"
        onChange={(e) => setFile(e.target.files[0])}
        className="text-white mb-3"
      />

      <button
        onClick={upload}
        className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700"
      >
        Upload
      </button>
    </div>
  );
}