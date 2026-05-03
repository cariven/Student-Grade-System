async function request(path, options = {}) {
  try {
    const res = await fetch(path, options);
    const data = await res.json();
    return { ok: res.ok, status: res.status, data };
  } catch (err) {
    throw new Error('Tidak bisa connect ke backend');
  }
}

export async function register(email, password) {
  return request('/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
}

export async function login(email, password) {
  return request('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
}

export async function getStudents(token) {
  return request('/students', {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function addStudent(token, name) {
  return request('/students', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ name }),
  });
}

export async function deleteStudent(token, studentId) {
  return request(`/students/${studentId}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getGrades(token, studentId) {
  return request(`/students/${studentId}/grades`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function addGrade(token, studentId, tugas, uts, uas) {
  return request('/grades', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ student_id: studentId, tugas, uts, uas }),
  });
}

export async function deleteGrade(token, gradeId) {
  return request(`/grades/${gradeId}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  });
}