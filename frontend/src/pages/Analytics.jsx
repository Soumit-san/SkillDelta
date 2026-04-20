import { useEffect, useState } from "react";
import SidebarLayout from "../layout/SidebarLayout";
import api from "../services/api";
import API from "../services/apiRoutes";
import GlobalLoader from "../components/GlobalLoader";

export default function Analytics() {
  const [data, setData] = useState(null);
  const userId = localStorage.getItem("user_id");

  if (!userId)
    return (
      <SidebarLayout>
        <GlobalLoader />
      </SidebarLayout>
    );

  useEffect(() => {
    api
      .get(API.dashboard.overview(userId))
      .then((res) => {
        const skillsList = res.data;
        const totalSkills = skillsList.length;
        const activeSkills = skillsList.filter(s => s.status !== "Rotting" && s.status !== "Forgotten").length;
        const avgHealth = totalSkills > 0
          ? Math.round(skillsList.reduce((acc, curr) => acc + curr.health, 0) / totalSkills)
          : 0;

        setData({
          total_skills: totalSkills,
          active_skills: activeSkills,
          average_health: avgHealth
        });
      })
      .catch((err) => console.log("Analytics error:", err.response?.data));
  }, [userId]);

  if (!data)
    return (
      <SidebarLayout>
        <GlobalLoader />
      </SidebarLayout>
    );

  return (
    <SidebarLayout>
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold text-white tracking-tight mb-8">Analytics Overview</h1>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            ["Total Skills", data.total_skills, "📚"],
            ["Active Skills", data.active_skills, "🔥"],
            ["Avg Health", `${data.average_health}%`, "❤️"],
          ].map(([label, val, icon], i) => (
            <div
              key={i}
              className="p-8 bg-[#1c1d27] rounded-3xl shadow-lg border border-white/5 hover:border-white/10 transition-all flex flex-col items-center justify-center text-center relative overflow-hidden group hover:-translate-y-1"
            >
              <div className="absolute top-0 right-0 p-4 opacity-30 text-6xl group-hover:scale-110 group-hover:opacity-60 transition-all duration-300">
                {icon}
              </div>
              <p className="text-sm font-bold text-gray-400 uppercase tracking-widest">{label}</p>
              <p className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-red-500 to-orange-400 mt-3 drop-shadow-sm">{val}</p>
            </div>
          ))}
        </div>
      </div>
    </SidebarLayout>
  );
}