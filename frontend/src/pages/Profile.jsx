import { useEffect, useState } from "react";
import SidebarLayout from "../layout/SidebarLayout";
import api from "../services/api";
import API from "../services/apiRoutes";
import GlobalLoader from "../components/GlobalLoader";

export default function Profile() {
  const [user, setUser] = useState(null);

  const [isEditing, setIsEditing] = useState(false);
  const [editName, setEditName] = useState("");

  const loadUser = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        setUser({ name: "Unknown", email: "No token found", created_at: new Date() });
        return;
      }

      const res = await api.get(API.users.me());
      setUser({
        name: res.data.name || "User",
        email: res.data.email || "No email in database",
        created_at: res.data.created_at || new Date().toISOString()
      });
      setEditName(res.data.name || "User");

    } catch (err) {
      console.log("Profile load error:", err);
      setUser({ name: "Error", email: "Could not fetch profile", created_at: new Date() });
    }
  };

  const handleSave = async () => {
    try {
      await api.put("/users/update", { name: editName });
      setUser(prev => ({ ...prev, name: editName }));
      setIsEditing(false);

      // Dispatch an event so SidebarLayout can update its state instantly
      window.dispatchEvent(new Event('user-updated'));
    } catch (err) {
      console.log("Failed to update profile", err);
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  if (!user)
    return (
      <SidebarLayout>
        <GlobalLoader />
      </SidebarLayout>
    );

  return (
    <SidebarLayout>
      <div className="max-w-3xl mx-auto relative">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-white tracking-tight">Your Profile</h1>
          <button
            onClick={() => window.location.href = "/dashboard"}
            className="w-10 h-10 bg-white/5 hover:bg-white/10 rounded-full flex items-center justify-center text-gray-400 hover:text-white transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <div className="bg-[#1c1d27] border border-white/5 p-8 rounded-[2rem] shadow-lg flex flex-col items-center sm:items-start text-center sm:text-left gap-8">

          <div className="flex flex-col sm:flex-row items-center gap-6 w-full pb-8 border-b border-white/5 relative">
            <div className="w-24 h-24 bg-gradient-to-br from-red-600/10 to-orange-500/10 text-orange-400 rounded-full flex items-center justify-center text-4xl font-extrabold uppercase ring-4 ring-orange-500/10 shrink-0">
              {user.email && user.email !== "No email in database" ? user.email.charAt(0) : user.name.charAt(0)}
            </div>
            <div className="flex-1 w-full">
              {isEditing ? (
                <input
                  type="text"
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  className="bg-black/20 border border-white/10 rounded-xl px-4 py-2 text-3xl font-bold text-white focus:outline-none focus:border-orange-500 w-full sm:w-auto text-center sm:text-left"
                  autoFocus
                />
              ) : (
                <h2 className="text-3xl font-bold text-white">{user.name}</h2>
              )}
              <div className="mt-3 flex flex-wrap gap-2 justify-center sm:justify-start">
                <span className="text-gray-300 bg-white/5 px-3 py-1 rounded-full text-xs font-semibold border border-white/10">ACTIVE LEARNER</span>
              </div>
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-4 w-full">
            <div className="bg-black/20 border border-white/5 p-5 rounded-2xl flex items-start gap-4 hover:border-white/10 transition-colors">
              <div className="w-12 h-12 bg-white/5 rounded-xl border border-white/5 flex items-center justify-center text-2xl shrink-0">✉️</div>
              <div>
                <p className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Email Address</p>
                <p className="text-lg font-bold text-gray-100 truncate">{user.email}</p>
              </div>
            </div>

            <div className="bg-black/20 border border-white/5 p-5 rounded-2xl flex items-start gap-4 hover:border-white/10 transition-colors">
              <div className="w-12 h-12 bg-white/5 rounded-xl border border-white/5 flex items-center justify-center text-2xl shrink-0">🗓️</div>
              <div>
                <p className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Joined Date</p>
                <p className="text-lg font-bold text-gray-100 truncate">
                  {new Date(user.created_at).toLocaleDateString(undefined, {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
              </div>
            </div>
          </div>

          <div className="w-full mt-4 flex justify-end gap-3">
            {isEditing && (
              <button
                onClick={() => { setIsEditing(false); setEditName(user.name); }}
                className="px-6 py-3 bg-white/5 hover:bg-white/10 text-white font-bold rounded-xl transition-all"
              >
                Cancel
              </button>
            )}
            <button
              onClick={isEditing ? handleSave : () => setIsEditing(true)}
              className="px-6 py-3 bg-gradient-to-r from-red-600 to-orange-500 hover:from-red-500 hover:to-orange-400 text-white font-bold rounded-xl shadow-lg shadow-orange-500/20 transition-all active:scale-95"
            >
              {isEditing ? "Save Name" : "Edit Profile"}
            </button>
          </div>

        </div>
      </div>
    </SidebarLayout>
  );
}