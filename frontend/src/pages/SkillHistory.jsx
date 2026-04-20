import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../services/api";
import SidebarLayout from "../layout/SidebarLayout";

export default function SkillHistory() {
  const { id } = useParams(); // skill_id
  const [history, setHistory] = useState([]);

  const loadHistory = async () => {
    try {
      // Backend does not have a /skill_history/skill endpoint for GET.
      // closest is decay curve history.
      const res = await api.get(`/analysis/skills/${id}/decay-curve`);
      const mappedHistory = res.data.map(d => ({
        date: d.date,
        health: d.score,
        action: "Recorded Decay"
      }));
      setHistory(mappedHistory);
    } catch (err) {
      console.log("History load error:", err.response?.data);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [id]);

  return (
    <SidebarLayout>
      <h1 className="text-3xl font-bold mb-6">Skill History</h1>

      <div className="space-y-6">
        {history.map((entry, i) => (
          <div
            key={i}
            className="p-4 bg-white/10 rounded-xl backdrop-blur-xl border border-white/10"
          >
            <p className="text-lg">{entry.date}</p>
            <p className="opacity-80">Health: {entry.health}%</p>
            <p className="opacity-80">Action: {entry.action}</p>
          </div>
        ))}
      </div>
    </SidebarLayout>
  );
}