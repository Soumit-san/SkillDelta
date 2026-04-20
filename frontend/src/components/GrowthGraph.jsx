import { useEffect, useState } from "react";
import api from "../services/api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function GrowthGraph({ id }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    api.get(`/growth/history/${id}`)   // ✅ FIXED ROUTE
      .then((res) => setData(res.data))
      .catch((err) => console.log("Growth graph error:", err.response?.data));
  }, [id]);

  return (
    <div className="bg-white/10 p-6 rounded-2xl backdrop-blur-xl">
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="date" stroke="#fff" />
          <YAxis stroke="#fff" />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="growth"           // ✅ FIXED DATA KEY
            stroke="#80d8ff"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}