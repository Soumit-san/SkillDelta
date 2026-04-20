import { useState } from "react";
import api from "../services/api";

export default function AddSkillModal({ close, refresh }) {
  const [name, setName] = useState("");
  const [level, setLevel] = useState("Beginner");
  const [date, setDate] = useState("");

  const userId = localStorage.getItem("user_id"); // ⭐ REQUIRED

  const add = async () => {
    if (!name.trim() || !date.trim()) return;

    try {
      await api.post("/skills/", {
        name,
        level,
        learned_date: date,
        user_id: Number(userId),  // ⭐ FIXED — backend requires user_id
      });

      refresh();
      close();
    } catch (err) {
      console.log("Add Skill Error:", err.response?.data);
    }
  };

  return (
    <div className="fixed inset-0 bg-[#0f0f16]/80 backdrop-blur-sm flex items-center justify-center z-50 animate-in fade-in duration-200">
      <div className="bg-[#121221] border border-white/10 shadow-2xl p-8 rounded-[2rem] w-[400px] transform transition-all shadow-purple-500/10">

        <h2 className="text-3xl font-bold mb-6 text-white tracking-tight">Add New Skill</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-purple-200/70 mb-1 ml-1">Skill Name</label>
            <input
              className="w-full px-4 py-3 bg-white/5 border border-white/10 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 rounded-xl outline-none transition-all placeholder:text-white/20 text-white"
              placeholder="e.g. React, Python, Django..."
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-purple-200/70 mb-1 ml-1">Current Level</label>
            <div className="relative">
              <select
                className="w-full px-4 py-3 bg-white/5 border border-white/10 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 rounded-xl outline-none transition-all text-white appearance-none cursor-pointer"
                value={level}
                onChange={(e) => setLevel(e.target.value)}
              >
                <option value="Beginner" className="bg-gray-800 text-white">Beginner</option>
                <option value="Intermediate" className="bg-gray-800 text-white">Intermediate</option>
                <option value="Advanced" className="bg-gray-800 text-white">Advanced</option>
              </select>
              <div className="absolute inset-y-0 right-4 flex items-center pointer-events-none text-white/50">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-purple-200/70 mb-1 ml-1">Date Started Learning</label>
            <input
              type="date"
              className="w-full px-4 py-3 bg-white/5 border border-white/10 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 rounded-xl outline-none transition-all text-white cursor-pointer color-scheme-dark"
              style={{ colorScheme: "dark" }}
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>
        </div>

        <div className="flex justify-end gap-3 mt-8">
          <button
            onClick={close}
            className="px-5 py-2.5 bg-white/5 hover:bg-white/10 rounded-xl transition-colors font-medium text-white/80"
          >
            Cancel
          </button>

          <button
            onClick={add}
            disabled={!name.trim() || !date.trim()}
            className="px-6 py-2.5 bg-purple-600 hover:bg-purple-500 disabled:opacity-50 disabled:hover:bg-purple-600 rounded-xl transition-colors font-medium shadow-lg shadow-purple-500/20"
          >
            Save Skill
          </button>
        </div>
      </div>
    </div>
  );
}