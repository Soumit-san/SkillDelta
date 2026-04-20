import { useState, useEffect } from "react";
import api from "../services/api";
import API from "../services/apiRoutes";
import SidebarLayout from "../layout/SidebarLayout";
import AddSkillModal from "../components/AddSkillModal";
import GlobalLoader from "../components/GlobalLoader";
import SkillCard from "../components/SkillCard";

export default function Dashboard() {
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState(false);
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState("all");
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const userId = localStorage.getItem("user_id");

  // 🚫 Prevent API call before userId is available
  if (!userId) {
    return (
      <SidebarLayout>
        <GlobalLoader />
      </SidebarLayout>
    );
  }

  const loadSkills = async () => {
    setLoading(true);
    try {
      if (selectedRole === "all") {
        const res = await api.get(API.dashboard.overview(userId));
        setSkills(res.data);
      } else {
        const res = await api.get(`/skills/filter?role=${selectedRole}`);
        setSkills(res.data.skills);
      }
    } catch (err) {
      console.log("Skill Loading Error:", err.response?.data);
    } finally {
      setLoading(false);
    }
  };

  const loadRoles = async () => {
    try {
      const res = await api.get("/skills/roles");
      setRoles(res.data);
    } catch (err) {
      console.log("Load roles error", err);
    }
  };

  useEffect(() => {
    loadRoles();
  }, []);

  useEffect(() => {
    loadSkills();
  }, [userId, selectedRole]);  // <-- Re-fetch when role changes

  return (
    <SidebarLayout>
      <div className="flex justify-between items-center mb-10">
        <div>
          <h1 className="text-4xl font-bold text-white tracking-tight">Your Skills</h1>

          <div className="relative mt-3 w-64">
            <button
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="w-full flex items-center justify-between p-3 bg-[#1c1d27] hover:bg-[#252633] border border-white/10 rounded-xl text-gray-200 transition-colors shadow-sm"
            >
              <span className="flex items-center gap-2 font-medium">
                {selectedRole === "all" ? (
                  "All Roles"
                ) : (
                  <>
                    {roles.find(r => r.key === selectedRole)?.icon} {roles.find(r => r.key === selectedRole)?.label}
                  </>
                )}
              </span>
              <svg className={`w-4 h-4 text-gray-400 transition-transform duration-300 ${isDropdownOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {/* Custom Dropdown Menu */}
            {isDropdownOpen && (
              <div className="absolute top-full left-0 mt-2 w-full bg-[#1c1d27] border border-white/10 rounded-xl shadow-2xl z-50 overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
                <button
                  onClick={() => {
                    setSelectedRole("all");
                    setIsDropdownOpen(false);
                  }}
                  className={`w-full text-left px-4 py-3 hover:bg-white/5 transition-colors font-medium ${selectedRole === "all" ? 'bg-gradient-to-r from-red-600/10 to-orange-500/10 text-orange-400 border-l-2 border-orange-500' : 'text-gray-300'}`}
                >
                  All Roles
                </button>
                {roles.map(r => (
                  <button
                    key={r.key}
                    onClick={() => {
                      setSelectedRole(r.key);
                      setIsDropdownOpen(false);
                    }}
                    className={`w-full text-left px-4 py-3 hover:bg-white/5 transition-colors flex items-center gap-2 font-medium ${selectedRole === r.key ? 'bg-gradient-to-r from-red-600/10 to-orange-500/10 text-orange-400 border-l-2 border-orange-500' : 'text-gray-300'}`}
                  >
                    <span>{r.icon}</span> <span>{r.label}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        <button
          onClick={() => setModal(true)}
          className="px-6 py-3 bg-gradient-to-r from-red-600 to-orange-500 hover:from-red-500 hover:to-orange-400 text-white font-bold rounded-xl max-h-12 shadow-lg shadow-orange-500/20 transition-all flex items-center gap-2"
        >
          <span>+</span> Add Skill
        </button>
      </div>

      {/* Skill List */}
      {loading ? (
        <GlobalLoader />
      ) : (
        <div className="grid md:grid-cols-3 gap-6">
          {skills.map((skill) => (
            <SkillCard key={skill.id || skill.skill_id} skill={skill} refresh={loadSkills} />
          ))}
        </div>
      )}

      {modal && (
        <AddSkillModal
          close={() => setModal(false)}
          refresh={loadSkills}
        />
      )}
    </SidebarLayout>
  );
}

