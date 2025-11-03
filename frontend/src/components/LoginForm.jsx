import { useState } from "react";
import { sendLoginRequest } from "../api";

export default function LoginForm({ onResult }) {
  const [website, setWebsite] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await sendLoginRequest({ website, username, password });
      let resData = await res.json();
      onResult({...resData, website: website});
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  let loginFormStyle = { borderRadius: "6px", minWidth: "20%", fontSize: "1.5rem" }

  return (
    <form onSubmit={handleSubmit}>
      <select className="form-select mb-3" style={loginFormStyle} value={website} onChange={(e) => setWebsite(e.target.value)}>
        <option style={loginFormStyle} value="">Choose website to proceed</option>
        <option style={loginFormStyle} value="fo1">fo1</option>
        <option style={loginFormStyle} value="fo2">fo2</option>
      </select>
      {website &&
        <div className="input-group mb-3">
          <div className="form-floating">
            <input
              className="form-control mb-2"
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              />
            <input
              className="form-control mb-2"
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              />
                <button className="btn px-5 fs-4 mt-2 btn-info"  type="submit" disabled={loading}>
                  {loading ? "Logging in..." : "Send"}
                </button>
            {error && <p style={{ color: "red" }}>{error}</p>}
          </div>
        </div>
        }
    </form>
  );
}
