import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function SkillCard({ skill, refresh }) {
  const navigate = useNavigate();
  const [showConfirm, setShowConfirm] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const deleteSkill = async () => {
    setIsDeleting(true);
    try {
      await api.delete(`/skills/${(skill.id || skill.skill_id)}`);
      refresh();
    } catch (err) {
      console.log("Delete error:", err);
      setIsDeleting(false);
      setShowConfirm(false);
    }
  };

  const getHealthColor = () => {
    if (skill.health > 70) return "#10b981"; // Emerald for stable
    if (skill.health > 40) return "#f59e0b"; // Amber for at-risk
    return "#ef4444"; // Red for critical
  };

  const getTextColor = () => {
    if (skill.health > 70) return "text-emerald-500";
    if (skill.health > 40) return "text-amber-500";
    return "text-red-500";
  };

  const status = skill.health > 70 ? "Stable" : skill.health > 40 ? "Moderate Decay" : "Critical Decay";

  // Calculate days since learned to show "Last practiced X days ago"
  const getDaysAgo = () => {
    const practiceDate = skill.last_practiced || skill.learned_date;
    if (!practiceDate) return "Unknown";
    const lastPractice = new Date(practiceDate);
    const now = new Date();
    const diff = Math.floor((now - lastPractice) / (1000 * 60 * 60 * 24));

    if (diff === 0) return "Today";
    if (diff === 1) return "1 day ago";
    if (diff < 7) return `${diff} days ago`;
    const weeks = Math.floor(diff / 7);
    if (weeks === 1) return "1 week ago";
    return `${weeks} weeks ago`;
  };

  // SVG dimensions
  const radius = 35;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (skill.health / 100) * circumference;

  return (
    <>
      <div
        onClick={() => navigate(`/skill/${(skill.id || skill.skill_id)}`)}
        className="relative bg-[#1c1d27] rounded-[2rem] p-6 shadow-lg border border-white/5 hover:border-white/10 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 cursor-pointer flex justify-between w-full"
      >
        {/* Left Content */}
        <div className="flex flex-col justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-100 tracking-tight leading-none mb-1">{(skill.name || skill.skill)}</h2>
            <p className="text-sm font-medium text-gray-400 capitalize">{skill.level || "Beginner"}</p>
          </div>

          <div className="mt-8">
            <h3 className="text-3xl font-extrabold text-white leading-none">{skill.health}%</h3>
            <p className="text-sm font-medium text-gray-400 mt-1">{status}</p>
          </div>

          <div className="mt-6 flex items-center gap-1.5 text-xs font-semibold text-orange-400">
            <span>🔥</span>
            <span>Last practiced {getDaysAgo()}</span>
          </div>
        </div>

        {/* Right Content */}
        <div className="flex flex-col items-end justify-between">

          {/* Circular Progress Indicator */}
          <div className="relative w-[80px] h-[80px] flex items-center justify-center">
            <svg className="transform -rotate-90 w-full h-full" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r={radius}
                fill="transparent"
                stroke="#2a2b36"
                strokeWidth="8"
              />
              <circle
                cx="50"
                cy="50"
                r={radius}
                fill="transparent"
                stroke={getHealthColor()}
                strokeWidth="8"
                strokeLinecap="round"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                className="transition-all duration-1000 ease-out"
              />
            </svg>
            <div className={`absolute flex items-center justify-center ${getTextColor()}`}>
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
              </svg>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-2 mt-auto">
            <button
              onClick={(e) => {
                e.stopPropagation();
                setShowConfirm(true);
              }}
              className="p-2 text-gray-500 hover:text-red-400 hover:bg-white/5 rounded-full transition-colors"
              title="Delete Skill"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
            <button
              onClick={(e) => {
                e.stopPropagation();
                navigate(`/skill/${(skill.id || skill.skill_id)}`);
              }}
              className="p-2 text-orange-400 hover:bg-white/5 rounded-full transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Modern Confirmation Modal (Dim Dark Theme adapted) */}
      {showConfirm && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 animate-in fade-in duration-200"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="bg-[#1c1d27] border border-white/10 shadow-2xl p-8 rounded-[2rem] w-[400px] transform transition-all text-center">

            <div className="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-6 text-red-500 ring-4 ring-red-500/5">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>

            <h2 className="text-2xl font-bold text-gray-100 mb-2">Delete Skill?</h2>
            <p className="text-gray-400 font-medium mb-8">
              Are you sure you want to completely remove <strong className="text-white">{(skill.name || skill.skill)}</strong>? This action cannot be undone and you will lose all tracking history.
            </p>

            <div className="flex gap-3 w-full">
              <button
                onClick={() => setShowConfirm(false)}
                disabled={isDeleting}
                className="flex-1 px-4 py-3 bg-white/5 hover:bg-white/10 border border-white/5 rounded-xl transition-colors font-semibold text-gray-300"
              >
                Cancel
              </button>
              <button
                onClick={deleteSkill}
                disabled={isDeleting}
                className="flex-1 px-4 py-3 bg-gradient-to-r from-red-600 to-orange-500 hover:from-red-500 hover:to-orange-400 disabled:opacity-50 shadow-lg shadow-orange-500/20 rounded-xl transition-all font-bold text-white tracking-wide"
              >
                {isDeleting ? "Deleting..." : "Yes, Delete"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}