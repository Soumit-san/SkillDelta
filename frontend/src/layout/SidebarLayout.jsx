import { useState, useEffect, useRef } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import api from "../services/api";
import logo from "../assets/logo.png";

export default function SidebarLayout({ children }) {
  const getInitialUser = () => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const payloadStr = atob(token.split('.')[1]);
        const payload = JSON.parse(payloadStr);
        if (payload.name) return { name: payload.name, email: "" };
      } catch (err) { }
    }
    return { name: "User", email: "" };
  };

  const [isOpen, setIsOpen] = useState(false);
  const [user, setUser] = useState(getInitialUser);
  const [reminders, setReminders] = useState([]);
  const [showReminders, setShowReminders] = useState(false);
  const [hasUnread, setHasUnread] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const dropdownRef = useRef(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const res = await api.get("/users/me");
        setUser({ name: res.data.name, email: res.data.email });
      } catch (err) {
        console.error("Failed to fetch user data", err);
      }
    };

    fetchUserData();

    // Listen for profile updates
    window.addEventListener("user-updated", fetchUserData);

    const fetchReminders = async () => {
      try {
        const userId = localStorage.getItem("user_id");
        if (userId) {
          const res = await api.get(`/reminders/user/${userId}`);
          // Filter for active present day alerts
          const today = new Date().toISOString().split('T')[0];
          const todayAlerts = res.data.filter(r => {
            if (!r.created_at) return false;
            const reminderDate = new Date(r.created_at).toISOString().split('T')[0];
            return reminderDate === today;
          });
          setReminders(todayAlerts);

          if (todayAlerts.length > 0) {
            const maxId = Math.max(...todayAlerts.map(r => r.id));
            const savedMax = parseInt(localStorage.getItem(`last_seen_reminder_id_${userId}`) || '0', 10);
            if (maxId > savedMax) {
              setHasUnread(true);
            }
          }
        }
      } catch (err) {
        console.error("Failed to fetch reminders", err);
      }
    };
    fetchReminders();

    return () => {
      window.removeEventListener("user-updated", fetchUserData);
    };
  }, []);

  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowReminders(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const menu = [
    { label: "Dashboard", path: "/dashboard", icon: "📊" },
    { label: "Analytics", path: "/analytics", icon: "📈" },
    { label: "Reminders", path: "/reminders", icon: "🔔" },
    { label: "Profile", path: "/profile", icon: "👤" },
  ];

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    navigate("/");
  };

  const currentPath = menu.find(m => m.path === location.pathname)?.label || "Dashboard";

  return (
    <div className="min-h-screen bg-[#13141c] text-gray-100 font-sans flex flex-col relative overflow-hidden">

      {/* Off-Canvas Sidebar Drawer */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-72 bg-[#1c1d27] transform transition-all duration-300 ease-in-out flex flex-col ${isOpen ? "translate-x-0 border-r border-white/5 shadow-2xl" : "-translate-x-full border-transparent shadow-none"}`}
      >
        <div className="p-6 flex items-center justify-between border-b border-white/5">
          <Link to="/dashboard" onClick={() => setIsOpen(false)} className="flex items-center gap-2">
            <img src={logo} alt="SkillDelta Logo" className="h-8 w-8 object-contain" />
            <span className="font-bold text-white text-xl tracking-tight">SkillDelta</span>
          </Link>
          <button onClick={() => setIsOpen(false)} className="p-2 text-gray-400 hover:text-white bg-white/5 rounded-lg transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
          {menu.map((item, index) => {
            const active = location.pathname === item.path;
            return (
              <Link
                key={index}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${active
                  ? "bg-gradient-to-r from-red-600 to-orange-500 text-white shadow-lg shadow-red-500/20 border border-white/10"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
                  }`}
              >
                <span className={active ? "opacity-100" : "opacity-60"}>{item.icon}</span>
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-white/5">
          <button
            onClick={logout}
            className="w-full flex items-center justify-center gap-2 py-3 text-red-400 bg-red-500/10 hover:bg-red-500/20 hover:text-red-300 rounded-xl font-semibold transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
            Logout
          </button>
        </div>
      </div>

      {/* Backdrop overlay when sidebar is open */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-40 backdrop-blur-sm transition-opacity"
          onClick={() => setIsOpen(false)}
        ></div>
      )}

      {/* Top Header */}
      <header className="bg-[#181922]/80 backdrop-blur-md border-b border-white/5 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">

            <div className="flex items-center gap-4">
              <button
                onClick={() => setIsOpen(true)}
                className="p-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors focus:outline-none"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
              </button>

              <div className="hidden sm:block">
                {location.pathname === "/dashboard" ? (
                  <div>
                    <h1 className="text-xl font-bold tracking-tight text-white">Hello {user.name},</h1>
                    <p className="text-sm font-medium text-gray-400">Here's your skill summary for today</p>
                  </div>
                ) : (
                  <Link to="/dashboard" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
                    <img src={logo} alt="SkillDelta Logo" className="h-8 w-8 object-contain" />
                    <h1 className="text-xl font-bold tracking-tight text-white">SkillDelta</h1>
                  </Link>
                )}
              </div>
            </div>

            <div className="flex items-center gap-4 relative" ref={dropdownRef}>
              <button
                onClick={() => {
                  const willShow = !showReminders;
                  setShowReminders(willShow);
                  if (willShow && reminders.length > 0) {
                    const userId = localStorage.getItem("user_id");
                    const maxId = Math.max(...reminders.map(r => r.id));
                    localStorage.setItem(`last_seen_reminder_id_${userId}`, maxId);
                    setHasUnread(false);
                  }
                }}
                className="p-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-full transition-colors relative"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
                {hasUnread && (
                  <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-[#181922]"></span>
                )}
              </button>

              {/* Reminders Dropdown */}
              {showReminders && (
                <div className="absolute top-12 right-12 w-80 bg-[#1c1d27] border border-white/10 shadow-2xl rounded-2xl overflow-hidden z-50">
                  <div className="bg-gradient-to-r from-red-600 to-orange-500 p-4">
                    <h3 className="text-white font-bold text-lg leading-none">Today's Alerts</h3>
                    <p className="text-white/80 text-xs mt-1">Pending reminders</p>
                  </div>
                  <div className="max-h-64 overflow-y-auto p-2">
                    {reminders.length === 0 ? (
                      <p className="text-gray-400 text-sm p-4 text-center">No alerts for today.</p>
                    ) : (
                      reminders.map((r, i) => {
                        const skillMatch = r.message.match(/Skill '(.*?)' needs attention/i);
                        const skillName = r.skill || (skillMatch ? skillMatch[1] : "Skill Alert");
                        return (
                          <div key={i} className="p-3 hover:bg-white/5 rounded-xl border border-transparent hover:border-white/5 transition-colors mb-1 cursor-default">
                            <p className="text-white text-sm font-semibold">{skillName}</p>
                            <p className="text-gray-400 text-xs mt-1 truncate">{r.message}</p>
                          </div>
                        );
                      })
                    )}
                  </div>
                  <div className="p-2 border-t border-white/5">
                    <Link to="/reminders" onClick={() => setShowReminders(false)} className="block w-full text-center py-2 text-sm font-semibold text-orange-400 hover:text-orange-300 bg-orange-500/10 hover:bg-orange-500/20 rounded-lg transition-colors">
                      View All Reminders
                    </Link>
                  </div>
                </div>
              )}

              <Link to="/profile" className="w-10 h-10 bg-gradient-to-br from-red-600 to-orange-500 text-white flex items-center justify-center rounded-xl font-bold shadow-lg shadow-orange-500/20 uppercase border border-white/10 hover:scale-105 transition-transform flex-shrink-0 cursor-pointer">
                {user.name.charAt(0)}
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 w-full max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
        {/* On mobile, show the greeting if it's the dashboard since it's hidden in the header */}
        {location.pathname === "/dashboard" && (
          <div className="sm:hidden mb-6">
            <h1 className="text-2xl font-bold tracking-tight text-white">Hello {user.name},</h1>
            <p className="text-sm font-medium text-gray-400">Here's your skill summary for today</p>
          </div>
        )}

        {children}
      </main>

    </div>
  );
}