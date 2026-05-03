import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { login } from "../api/api"

export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  async function handleLogin(e) {
    e.preventDefault()
    setError("")
    setSuccess("")

    if (!email.trim() || !password.trim()) {
      setError("Email dan password wajib diisi")
      return
    }

    setLoading(true)
    try {
      const { ok, data } = await login(email, password)
      if (ok && data.token) {
        localStorage.setItem("token", data.token)
        setSuccess("Login berhasil! Mengalihkan...")
        setTimeout(() => navigate("/dashboard"), 800)
      } else {
        setError(data.error || "Email atau password salah")
      }
    } catch (err) {
      setError("Tidak bisa connect ke backend")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <div className="auth-header">
          <div className="auth-logo">🎓</div>
          <h1 className="auth-title">Selamat Datang</h1>
          <p className="auth-subtitle">Login ke Student Grade System</p>
        </div>

        {error && <div className="alert alert-error">⚠️ {error}</div>}
        {success && <div className="alert alert-success">✅ {success}</div>}

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label className="form-label">Email</label>
            <div className="form-input-wrapper">
              <span className="form-icon">📧</span>
              <input
                type="email"
                className="form-input"
                placeholder="nama@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <div className="form-input-wrapper">
              <span className="form-icon">🔒</span>
              <input
                type={showPassword ? "text" : "password"}
                className="form-input has-toggle"
                placeholder="Masukkan password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                tabIndex={-1}
              >
                {showPassword ? "🙈" : "👁️"}
              </button>
            </div>
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner"></span>
                Memproses...
              </>
            ) : (
              "Login"
            )}
          </button>
        </form>

        <div className="auth-footer">
          Belum punya akun?
          <span className="auth-link" onClick={() => navigate("/register")}>
            Daftar di sini
          </span>
        </div>
      </div>
    </div>
  )
}