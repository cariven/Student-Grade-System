import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { register } from "../api/api"

export default function Register() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  async function handleRegister(e) {
    e.preventDefault()
    setError("")
    setSuccess("")

    if (!email.trim() || !password.trim()) {
      setError("Email dan password wajib diisi")
      return
    }

    if (password.length < 8) {
      setError("Password minimal 8 karakter")
      return
    }

    if (password !== confirmPassword) {
      setError("Konfirmasi password tidak cocok")
      return
    }

    setLoading(true)
    try {
      const { ok, data } = await register(email, password)
      if (ok) {
        setSuccess("Register berhasil! Mengalihkan ke login...")
        setTimeout(() => navigate("/"), 1200)
      } else {
        setError(data.error || "Register gagal")
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
          <div className="auth-logo">✨</div>
          <h1 className="auth-title">Buat Akun Baru</h1>
          <p className="auth-subtitle">Daftar untuk mulai gunakan sistem</p>
        </div>

        {error && <div className="alert alert-error">⚠️ {error}</div>}
        {success && <div className="alert alert-success">✅ {success}</div>}

        <form onSubmit={handleRegister}>
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
                placeholder="Minimal 8 karakter"
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

          <div className="form-group">
            <label className="form-label">Konfirmasi Password</label>
            <div className="form-input-wrapper">
              <span className="form-icon">🔐</span>
              <input
                type={showPassword ? "text" : "password"}
                className="form-input"
                placeholder="Ulangi password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                disabled={loading}
              />
            </div>
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner"></span>
                Memproses...
              </>
            ) : (
              "Daftar Sekarang"
            )}
          </button>
        </form>

        <div className="auth-footer">
          Sudah punya akun?
          <span className="auth-link" onClick={() => navigate("/")}>
            Login di sini
          </span>
        </div>
      </div>
    </div>
  )
}