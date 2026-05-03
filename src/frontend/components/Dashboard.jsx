import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { getStudents, addStudent, deleteStudent, getGrades, addGrade, deleteGrade } from "../api/api"

export default function Dashboard() {
  const [students, setStudents] = useState([])
  const [name, setName] = useState("")
  const [selectedStudent, setSelectedStudent] = useState(null)
  const [grades, setGrades] = useState([])
  const [tugas, setTugas] = useState("")
  const [uts, setUts] = useState("")
  const [uas, setUas] = useState("")
  const [toasts, setToasts] = useState([])
  const [confirmModal, setConfirmModal] = useState(null)
  const navigate = useNavigate()
  const token = localStorage.getItem("token")

  useEffect(() => {
    if (!token) { navigate("/"); return }
    loadStudents()
  }, [])

  function showToast(message, type = "success") {
    const id = Date.now()
    setToasts(prev => [...prev, { id, message, type }])
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id))
    }, 3000)
  }

  async function loadStudents() {
    try {
      const { ok, data } = await getStudents(token)
      if (ok) setStudents(data)
    } catch {
      showToast("Gagal memuat data mahasiswa", "error")
    }
  }

  async function handleAddStudent(e) {
    e.preventDefault()
    if (!name.trim()) {
      showToast("Nama tidak boleh kosong", "error")
      return
    }
    const { ok, data } = await addStudent(token, name)
    if (ok) {
      setName("")
      loadStudents()
      showToast("Mahasiswa berhasil ditambahkan")
    } else {
      showToast(data.error || "Gagal tambah mahasiswa", "error")
    }
  }

  function askDeleteStudent(studentId, studentName) {
    setConfirmModal({
      title: "Hapus Mahasiswa?",
      text: `Apakah kamu yakin ingin menghapus "${studentName}"? Semua nilai juga akan terhapus.`,
      onConfirm: () => handleDeleteStudent(studentId)
    })
  }

  async function handleDeleteStudent(studentId) {
    setConfirmModal(null)
    await deleteStudent(token, studentId)
    if (selectedStudent?.id === studentId) {
      setSelectedStudent(null)
      setGrades([])
    }
    loadStudents()
    showToast("Mahasiswa berhasil dihapus")
  }

  async function handleSelectStudent(student) {
    setSelectedStudent(student)
    const { ok, data } = await getGrades(token, student.id)
    if (ok) setGrades(data)
  }

  async function handleAddGrade(e) {
    e.preventDefault()
    if (!selectedStudent) {
      showToast("Pilih mahasiswa dulu", "error")
      return
    }
    if (!tugas || !uts || !uas) {
      showToast("Semua nilai wajib diisi", "error")
      return
    }
    const { ok, data } = await addGrade(token, selectedStudent.id, parseFloat(tugas), parseFloat(uts), parseFloat(uas))
    if (ok) {
      setTugas(""); setUts(""); setUas("")
      handleSelectStudent(selectedStudent)
      showToast("Nilai berhasil ditambahkan")
    } else {
      showToast(data.error || "Gagal input nilai", "error")
    }
  }

  async function handleDeleteGrade(gradeId) {
    await deleteGrade(token, gradeId)
    handleSelectStudent(selectedStudent)
    showToast("Nilai berhasil dihapus")
  }

  function handleLogout() {
    localStorage.removeItem("token")
    navigate("/")
  }

  function getInitials(name) {
    return name.split(" ").map(w => w[0]).slice(0, 2).join("").toUpperCase()
  }

  const gradeColor = {
    A: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
    B: "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
    C: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
    D: "linear-gradient(135deg, #f97316 0%, #ea580c 100%)",
    E: "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
  }

  return (
    <div className="dashboard-wrapper">
      {/* Toast Notifications */}
      <div className="toast-container">
        {toasts.map(t => (
          <div key={t.id} className={`toast toast-${t.type}`}>
            {t.type === "success" ? "✅" : "⚠️"} {t.message}
          </div>
        ))}
      </div>

      {/* Confirm Modal */}
      {confirmModal && (
        <div className="modal-backdrop" onClick={() => setConfirmModal(null)}>
          <div className="modal-card" onClick={e => e.stopPropagation()}>
            <div className="modal-icon">⚠️</div>
            <h3 className="modal-title">{confirmModal.title}</h3>
            <p className="modal-text">{confirmModal.text}</p>
            <div className="modal-actions">
              <button className="btn-cancel" onClick={() => setConfirmModal(null)}>Batal</button>
              <button className="btn-confirm" onClick={confirmModal.onConfirm}>Ya, Hapus</button>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="dashboard-header">
        <div className="dashboard-header-left">
          <div className="dashboard-logo">🎓</div>
          <div>
            <h1 className="dashboard-title">Student Grade System</h1>
            <p className="dashboard-subtitle">Kelola data mahasiswa & nilai</p>
          </div>
        </div>
        <button onClick={handleLogout} className="btn-logout">
          🚪 Logout
        </button>
      </div>

      <div className="dashboard-container">
        {/* Tambah Mahasiswa */}
        <div className="card-add-student">
          <h3 className="card-title">➕ Tambah Mahasiswa Baru</h3>
          <form className="add-student-form" onSubmit={handleAddStudent}>
            <input
              placeholder="Masukkan nama mahasiswa..."
              value={name}
              onChange={e => setName(e.target.value)}
              className="form-input"
              style={{ paddingLeft: "14px" }}
            />
            <button type="submit" className="btn-add">Tambah</button>
          </form>
        </div>

        {/* Grid 2 Kolom */}
        <div className="dashboard-grid">
          {/* Kolom Kiri: Daftar Mahasiswa */}
          <div className="panel">
            <div className="panel-header">
              <span>👥 Daftar Mahasiswa</span>
              <span className="badge-count">{students.length}</span>
            </div>

            {students.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">📭</div>
                <p className="empty-text">Belum ada mahasiswa.<br/>Tambahkan di atas!</p>
              </div>
            ) : (
              students.map(s => (
                <div
                  key={s.id}
                  onClick={() => handleSelectStudent(s)}
                  className={`student-item ${selectedStudent?.id === s.id ? "active" : ""}`}
                >
                  <div className="student-info">
                    <div className="student-avatar">{getInitials(s.name)}</div>
                    <span className="student-name">{s.name}</span>
                  </div>
                  <button
                    onClick={e => { e.stopPropagation(); askDeleteStudent(s.id, s.name) }}
                    className="btn-delete"
                  >
                    Hapus
                  </button>
                </div>
              ))
            )}
          </div>

          {/* Kolom Kanan: Nilai */}
          <div className="panel">
            <div className="panel-header">
              <span>📊 Nilai {selectedStudent ? `— ${selectedStudent.name}` : ""}</span>
              {selectedStudent && <span className="badge-count">{grades.length}</span>}
            </div>

            {!selectedStudent ? (
              <div className="empty-state">
                <div className="empty-icon">👈</div>
                <p className="empty-text">Pilih mahasiswa di sebelah<br/>untuk melihat nilai.</p>
              </div>
            ) : (
              <>
                <form className="grade-input-box" onSubmit={handleAddGrade}>
                  <div className="grade-input-row">
                    <input className="grade-input" placeholder="Tugas" value={tugas} onChange={e => setTugas(e.target.value)} type="number" min="0" max="100" />
                    <input className="grade-input" placeholder="UTS" value={uts} onChange={e => setUts(e.target.value)} type="number" min="0" max="100" />
                    <input className="grade-input" placeholder="UAS" value={uas} onChange={e => setUas(e.target.value)} type="number" min="0" max="100" />
                  </div>
                  <button type="submit" className="btn-submit-grade">Input Nilai</button>
                </form>

                {grades.length === 0 ? (
                  <div className="empty-state">
                    <div className="empty-icon">📝</div>
                    <p className="empty-text">Belum ada nilai.</p>
                  </div>
                ) : (
                  grades.map(g => (
                    <div key={g.id} className="grade-item">
                      <div className="grade-details">
                        <div className="grade-scores">
                          <span>Tugas: {g.tugas}</span>
                          <span>UTS: {g.uts}</span>
                          <span>UAS: {g.uas}</span>
                        </div>
                        <div className="grade-final-row">
                          <span className="grade-final-label">Nilai Akhir:</span>
                          <span className="grade-final-value">{g.final}</span>
                          <span className="grade-badge" style={{ background: gradeColor[g.grade] }}>
                            {g.grade}
                          </span>
                        </div>
                      </div>
                      <button onClick={() => handleDeleteGrade(g.id)} className="btn-delete">
                        Hapus
                      </button>
                    </div>
                  ))
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}