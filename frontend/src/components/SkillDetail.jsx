import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import SidebarLayout from "../layout/SidebarLayout";
import api from "../services/api";

import {
  AreaChart,
  Area,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import GlobalLoader from "./GlobalLoader";

export default function SkillDetail() {
  const { id } = useParams(); // skill_id from URL

  const [skill, setSkill] = useState(null);
  const [health, setHealth] = useState(null);
  const [decayData, setDecayData] = useState([]);
  const [growthData, setGrowthData] = useState([]);
  const [weakTopics, setWeakTopics] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [isLoadingRecommendations, setIsLoadingRecommendations] = useState(true);
  const [days, setDays] = useState("");
  const [uploadError, setUploadError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  // Load all skill-related data
  const loadAll = async () => {
    try {
      const userId = localStorage.getItem("user_id");

      const skillPromise = api.get(`/skills/${id}`);
      const healthPromise = api.get(`/analysis/skills/${id}/health`);
      const decayPromise = api.get(`/analysis/skills/${id}/decay-curve`);
      const growthPromise = api.get(`/growth/skills/${id}`);

      // 🔥 Fetch everything concurrently
      const [skillRes, healthRes, decayRes, growthRes] = await Promise.all([
        skillPromise,
        healthPromise,
        decayPromise,
        growthPromise
      ]);

      // Process skill
      if (skillRes.data) {
        setSkill({ name: skillRes.data.name, level: skillRes.data.level });
      } else {
        setSkill({ name: "Unknown Skill", level: "Unknown" });
      }

      // Process others
      setHealth(healthRes.data);
      setDecayData(decayRes.data);
      setGrowthData(growthRes.data?.history || []);

    } catch (err) {
      console.log("Error loading skill details:", err);
    }
  };

  const loadRecommendations = async () => {
    try {
      setIsLoadingRecommendations(true);
      const recRes = await api.get(`/recommendations/skills/${id}`);
      setRecommendations(recRes.data);
    } catch (err) {
      console.log("Error loading recommendations:", err);
    } finally {
      setIsLoadingRecommendations(false);
    }
  };

  useEffect(() => {
    loadAll();
    loadRecommendations();
  }, [id]);

  // ⭐ Practice the skill
  const practice = async () => {
    try {
      await api.post(`/practice/skills/${id}`);  // CORRECTED PATH
      loadAll();
    } catch (err) {
      console.log("Practice error:", err.response?.data);
    }
  };

  // ⭐ Upload assessment file
  const uploadAssessment = async (e) => {
    if (!e.target.files.length) return;

    const form = new FormData();
    form.append("file", e.target.files[0]);

    setIsUploading(true);
    setUploadError(null);

    try {
      const res = await api.post(`/assessment/${id}`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setWeakTopics(res.data?.weak_topics || []);
      // ⭐ Reload to update health, decay curves, and new recommendations
      loadAll();
      loadRecommendations();
    } catch (err) {
      console.log("Assessment upload error:", err.response?.data);
      setUploadError(err.response?.data?.detail || "An error occurred while uploading. Please check the file and try again.");
    } finally {
      setIsUploading(false);
      e.target.value = null; // reset file input safely
    }
  };

  // ⭐ Predict health
  const predict = async () => {
    try {
      const res = await api.get(`/predict/${id}?days=${days}`);
      setPrediction(res.data);
    } catch (err) {
      console.log("Prediction error:", err.response?.data);
    }
  };

  if (!skill) {
    return (
      <SidebarLayout>
        <GlobalLoader />
      </SidebarLayout>
    );
  }

  return (
    <SidebarLayout>
      <h1 className="text-4xl font-bold mb-6">{skill.name}</h1>

      {/* SKILL SUMMARY */}
      <div className="bg-white/10 backdrop-blur-xl border border-white/20 p-6 rounded-3xl mb-8">
        <p className="text-lg opacity-80 mb-2">Level: {skill.level}</p>

        {health && (
          <p>
            <span className="text-4xl font-bold">{health.health}%</span>
            <span
              className={`ml-2 ${health.health > 70
                ? "text-green-400"
                : health.health > 40
                  ? "text-yellow-400"
                  : "text-red-400"
                }`}
            >
              • {health.status}
            </span>
          </p>
        )}

        <button
          onClick={practice}
          className="mt-4 px-6 py-3 bg-gradient-to-r from-red-600 to-orange-500 hover:from-red-500 hover:to-orange-400 font-bold rounded-xl shadow-lg shadow-orange-500/20 transition-all transform hover:-translate-y-0.5"
        >
          I Practiced Today
        </button>
      </div>

      {/* RECOMMENDATIONS SECTION */}
      {isLoadingRecommendations ? (
        <section className="mb-10">
          <h2 className="text-2xl font-bold mb-4">Recommendations</h2>
          <div className="bg-white/10 backdrop-blur-xl p-8 rounded-3xl border border-white/20 flex flex-col items-center justify-center min-h-[200px]">
            <div className="flex space-x-2">
              <div className="w-3 h-3 bg-orange-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div className="w-3 h-3 bg-orange-500 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="w-3 h-3 bg-orange-500 rounded-full animate-bounce"></div>
            </div>
            <p className="mt-4 text-orange-400 font-medium animate-pulse">AI is generating your learning path...</p>
          </div>
        </section>
      ) : recommendations && (
        <section className="mb-10">
          <h2 className="text-2xl font-bold mb-4">Recommendations</h2>
          <div className="bg-white/10 backdrop-blur-xl p-6 rounded-3xl border border-white/20">
            <h3 className="text-xl font-semibold text-orange-400">{recommendations.focus_topic}</h3>
            <p className="opacity-80 mt-2 mb-4">{recommendations.reason}</p>

            <h4 className="font-bold mb-2">Tips to Improve:</h4>
            <ul className="list-disc pl-5 opacity-90">
              {recommendations.tips?.map((tip, i) => (
                <li key={i}>{tip}</li>
              ))}
            </ul>

            {recommendations.resources && recommendations.resources.length > 0 && (
              <div className="mt-8">
                <h4 className="font-bold mb-4">Recommended Resources:</h4>
                <div className="grid gap-4 md:grid-cols-2">
                  {recommendations.resources.map((res, i) => (
                    <a
                      key={i}
                      href={res.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block p-4 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 outline-none focus:ring-2 focus:ring-orange-500 transition-all hover:scale-[1.02] duration-300 shadow-sm"
                    >
                      <div className="flex items-start mb-2">
                        <span className="mr-3 leading-none flex-shrink-0">
                          {res.type === "video" ? (
                            <svg width="28" height="20" viewBox="0 0 28 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <rect width="28" height="20" rx="5" fill="#FF0000"/>
                              <path d="M11.5 6L19 10L11.5 14V6Z" fill="white"/>
                            </svg>
                          ) : (
                            <span className="text-2xl">📚</span>
                          )}
                        </span>
                        <h5 className="font-semibold text-orange-300 line-clamp-2 leading-tight flex-1">
                          {res.title}
                        </h5>
                      </div>

                      {res.type === "video" ? (
                        <div className="mt-2 flex items-center gap-1.5 opacity-80 transition-opacity hover:opacity-100">
                          {res.channel_logo ? (
                            <img src={res.channel_logo} alt={res.channel} className="w-5 h-5 rounded-full object-cover shadow-sm bg-black/20" />
                          ) : (
                            <svg width="18" height="13" viewBox="0 0 28 20" fill="none" xmlns="http://www.w3.org/2000/svg" className="inline-block flex-shrink-0">
                              <rect width="28" height="20" rx="5" fill="#FF0000"/>
                              <path d="M11.5 6L19 10L11.5 14V6Z" fill="white"/>
                            </svg>
                          )}
                          <p className="text-sm text-orange-400 font-medium">
                            {res.channel}
                          </p>
                        </div>
                      ) : (
                        <p className="text-xs opacity-70 mt-2 line-clamp-3 leading-relaxed">
                          {res.summary}
                        </p>
                      )}
                    </a>
                  ))}
                </div>
              </div>
            )}

            {recommendations.plan && (
              <div className="mt-8 p-5 bg-gradient-to-br from-orange-500/10 to-red-600/10 border border-orange-500/20 rounded-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                  <h4 className="font-bold text-orange-400 mb-1 text-lg flex items-center gap-2">
                    <span>🗓️</span> Your Practice Plan
                  </h4>
                  <p className="text-sm text-gray-300">Targeted schedule to efficiently master this skill.</p>
                </div>
                <div className="flex gap-3 text-center w-full sm:w-auto">
                  <div className="flex-1 sm:flex-none bg-[#1c1d27] py-3 px-5 rounded-xl border border-white/10 shadow-inner">
                    <p className="text-2xl font-extrabold text-white">{recommendations.plan.days}</p>
                    <p className="text-xs text-gray-400 font-bold uppercase tracking-wider mt-0.5">Days/Week</p>
                  </div>
                  <div className="flex-1 sm:flex-none bg-[#1c1d27] py-3 px-5 rounded-xl border border-white/10 shadow-inner">
                    <p className="text-2xl font-extrabold text-white">{recommendations.plan.minutes_per_day}</p>
                    <p className="text-xs text-gray-400 font-bold uppercase tracking-wider mt-0.5">Mins/Day</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>
      )}

      {weakTopics.length > 0 && (
        <section className="mb-10">
          <h2 className="text-2xl font-bold mb-4">Weak Subtopics</h2>
          <div className="grid gap-4">
            {weakTopics.map((t, i) => (
              <div key={i} className="p-4 bg-red-500/20 border border-red-300/20 rounded-xl">
                <p className="text-lg font-semibold">{t.topic}</p>
                <p className="opacity-80">Weakness: {t.score}%</p>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="mb-10">
        <h2 className="text-2xl font-bold mb-4">Upload Assessment</h2>
        <div className="flex items-center gap-3">
          <label className={`cursor-pointer group flex items-center justify-center w-12 h-12 bg-white/10 hover:bg-white/20 border border-white/20 hover:border-orange-500 rounded-xl transition-all shadow-sm ${isUploading ? 'opacity-50 pointer-events-none' : ''}`}>
            <span className="text-3xl font-light text-orange-400 group-hover:text-orange-300 group-hover:scale-110 transition-transform leading-none mt-[-2px]">+</span>
            <input
              type="file"
              className="hidden"
              onChange={uploadAssessment}
              disabled={isUploading}
            />
          </label>
          <div className="flex-1 px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white/50 font-medium truncate">
            {isUploading ? "Uploading and analyzing..." : "Upload your assessment file (PDF, TXT, DOCX)"}
          </div>
        </div>
        {uploadError && <p className="mt-3 text-red-400 font-semibold">{uploadError}</p>}
      </section>

      {/* Process data for unique X-axis keys to fix Recharts tooltip bug */}
      <ChartSection title="Decay Curve">
        <div style={{ width: '100%', height: 350 }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={decayData.map((d, i) => ({ ...d, uniqueId: i }))}>
              <defs>
                <linearGradient id="colorDecay" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ea580c" stopOpacity={0.5} />
                  <stop offset="95%" stopColor="#ea580c" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis
                dataKey="uniqueId"
                tickFormatter={(val) => {
                  const dateStr = decayData[val]?.date;
                  if (!dateStr) return "";
                  const dateObj = new Date(dateStr);
                  return dateObj.toLocaleDateString("en-US", { month: "short", day: "numeric" });
                }}
                stroke="#6b7280"
                tick={{ fill: "#9ca3af", fontSize: 12 }}
                tickLine={false}
                axisLine={false}
                minTickGap={30}
                padding={{ left: 20, right: 20 }}
              />
              <YAxis
                stroke="#6b7280"
                tick={{ fill: "#9ca3af", fontSize: 12 }}
                tickLine={false}
                axisLine={false}
              />
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ffffff10" />
              <Tooltip
                contentStyle={{ backgroundColor: "#1e1e2f", border: "1px solid #ea580c", borderRadius: "12px", color: "#fff", boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)" }}
                itemStyle={{ color: "#ea580c", fontWeight: "bold" }}
                labelFormatter={(label) => decayData[label]?.date}
              />
              <Area
                type="monotone"
                dataKey="score"
                stroke="#ea580c"
                strokeWidth={4}
                fillOpacity={1}
                fill="url(#colorDecay)"
                activeDot={{ r: 6, strokeWidth: 0, fill: "#fff" }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </ChartSection>

      <ChartSection title="Growth History">
        <div style={{ width: '100%', height: 350 }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={growthData.map((d, i) => ({ ...d, uniqueId: i }))}>
              <defs>
                <linearGradient id="colorGrowth" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#4ade80" stopOpacity={0.5} />
                  <stop offset="95%" stopColor="#4ade80" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis
                dataKey="uniqueId"
                tickFormatter={(val) => {
                  const dateStr = growthData[val]?.date;
                  if (!dateStr) return "";
                  const dateObj = new Date(dateStr);
                  return dateObj.toLocaleDateString("en-US", { month: "short", day: "numeric" });
                }}
                stroke="#6b7280"
                tick={{ fill: "#9ca3af", fontSize: 12 }}
                tickLine={false}
                axisLine={false}
                minTickGap={30}
                padding={{ left: 20, right: 20 }}
              />
              <YAxis
                stroke="#6b7280"
                tick={{ fill: "#9ca3af", fontSize: 12 }}
                tickLine={false}
                axisLine={false}
              />
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ffffff10" />
              <Tooltip
                contentStyle={{ backgroundColor: "#1e1e2f", border: "1px solid #4ade80", borderRadius: "12px", color: "#fff", boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)" }}
                itemStyle={{ color: "#4ade80", fontWeight: "bold" }}
                labelFormatter={(label) => growthData[label]?.date}
              />
              <Area
                type="monotone"
                dataKey="health"
                stroke="#4ade80"
                strokeWidth={4}
                fillOpacity={1}
                fill="url(#colorGrowth)"
                activeDot={{ r: 6, strokeWidth: 0, fill: "#fff" }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </ChartSection>

      <section>
        <h2 className="text-2xl font-bold mb-4">Predict Future Health</h2>

        <input
          type="number"
          placeholder="Days"
          className="bg-white/10 p-3 rounded-xl border border-white/20 mr-4"
          value={days}
          onChange={(e) => setDays(e.target.value)}
        />

        <button
          onClick={predict}
          className="px-6 py-3 bg-gradient-to-r from-red-600 to-orange-500 hover:from-red-500 hover:to-orange-400 text-white font-bold rounded-xl shadow-lg shadow-orange-500/20 transition-all transform hover:-translate-y-0.5"
        >
          Predict
        </button>

        {prediction && (
          <div className="mt-4 bg-white/10 backdrop-blur-xl p-6 rounded-3xl border border-white/20">
            <p className="text-xl font-bold">Predicted Health: {prediction.predicted_health_after_days}%</p>
            <p
              className={`mt-2 ${prediction.predicted_health_after_days > 70
                ? "text-green-400"
                : prediction.predicted_health_after_days > 40
                  ? "text-yellow-400"
                  : "text-red-400"
                }`}
            >
              Risk: {prediction.risk_level}
            </p>
          </div>
        )}
      </section>

      {/* DISLAIMER */}
      <div className="mt-16 text-center text-xs text-white/40 pb-4">
        * Disclaimer: SkillDelta models health and decay based on cognitive practice metrics. While highly accurate, we recommend relying on your own judgment to confirm true real-world proficiency.
      </div>
    </SidebarLayout>
  );
}

function ChartSection({ title, children }) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <section className="mb-6 bg-white/5 border border-white/10 rounded-3xl overflow-hidden transition-all duration-300">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between p-6 outline-none hover:bg-white/5 transition-colors"
      >
        <h2 className="text-2xl font-bold">{title}</h2>
        <div className={`p-2 rounded-full bg-orange-500/20 text-orange-500 transition-transform duration-500 ${isExpanded ? 'rotate-180' : ''}`}>
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
          </svg>
        </div>
      </button>

      <div
        className={`transition-all duration-500 ease-in-out overflow-hidden ${isExpanded ? 'max-h-[600px] opacity-100' : 'max-h-0 opacity-0'}`}
      >
        <div className="px-6 pb-6 pt-2">
          <div className="bg-[#121221] backdrop-blur-xl p-6 rounded-2xl border border-white/10 shadow-inner">
            {children}
          </div>
        </div>
      </div>
    </section>
  );
}
