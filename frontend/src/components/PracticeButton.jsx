import api from "../services/api";

export default function PracticeButton({ id, refresh }) {
  const practice = async () => {
    try {
      await api.post(`/practice/skills/${id}`);  // ✅ FIXED ROUTE
      refresh();
    } catch (err) {
      console.log("Practice error:", err.response?.data);
    }
  };

  return (
    <button
      onClick={practice}
      className="px-6 py-3 bg-green-600 hover:bg-green-700 rounded-xl mt-4"
    >
      I Practiced Today
    </button>
  );
}