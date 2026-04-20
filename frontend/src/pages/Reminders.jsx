import { useEffect, useState } from "react";
import SidebarLayout from "../layout/SidebarLayout";
import api from "../services/api";
import API from "../services/apiRoutes";

export default function Reminders() {
  const [reminders, setReminders] = useState([]);
  const userId = localStorage.getItem("user_id");

  const load = async () => {
    try {
      const res = await api.get(API.reminders.list(userId));  // ✔ correct route
      setReminders(res.data);
    } catch (err) {
      console.log("Reminder Load Error:", err.response?.data);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <SidebarLayout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white tracking-tight mb-8">Active Reminders</h1>

        {reminders.length === 0 ? (
          <div className="text-center py-20 bg-[#1c1d27] rounded-3xl border border-white/5 shadow-lg">
            <div className="text-6xl mb-4">🔔</div>
            <h3 className="text-xl font-bold text-gray-100 mb-2">No Reminders Yet</h3>
            <p className="text-gray-400">When your skills begin to decay, you'll see alerts here.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {reminders.map((r) => (
              <div
                key={r.id}
                className="flex flex-col bg-[#1c1d27] p-6 rounded-2xl shadow-lg border border-white/5 hover:border-white/10 transition-colors"
              >
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-gradient-to-br from-red-600/10 to-orange-500/10 text-orange-400 rounded-xl border border-orange-500/10">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
                  </div>
                  <div className="flex-1">
                    <p className="text-lg font-bold text-gray-100 mb-1">{r.message}</p>
                    <div className="flex justify-between items-center mt-2 text-sm font-medium">
                      <span className="text-gray-400 bg-white/5 px-3 py-1 rounded-full border border-white/5">
                        {new Date(r.created_at).toLocaleDateString(undefined, {
                          weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
                        })}
                      </span>
                      {r.email_sent ? (
                        <span className="text-emerald-400 bg-emerald-500/10 px-3 py-1 border border-emerald-500/20 rounded-full flex items-center gap-1">
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                          Email Delivered
                        </span>
                      ) : (
                        <span className="text-orange-400 bg-orange-500/10 px-3 py-1 border border-orange-500/20 rounded-full">In-App Notification</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </SidebarLayout>
  );
}