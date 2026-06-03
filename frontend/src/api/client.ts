import axios from 'axios'
import type {
  Student, Club, Criterion, Achievement, Application,
  Notification, CriteriaStatus, Staff,
  CreateStudentPayload, LogAchievementPayload, UpdateApplicationPayload,
} from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

// ── Students ─────────────────────────────────────────────────────────────────
export const studentsApi = {
  list: (params?: { year_group?: number; is_active?: boolean; search?: string }) =>
    api.get<Student[]>('/students', { params }).then(r => r.data),

  get: (id: string) =>
    api.get<Student>(`/students/${id}`).then(r => r.data),

  create: (payload: CreateStudentPayload) =>
    api.post<Student>('/students', payload).then(r => r.data),

  update: (id: string, payload: Partial<CreateStudentPayload & { is_active: boolean }>) =>
    api.patch<Student>(`/students/${id}`, payload).then(r => r.data),

  deactivate: (id: string) =>
    api.delete(`/students/${id}`),

  bulkImport: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post<{ message: string; errors: string[] }>('/students/bulk-import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }).then(r => r.data)
  },
}

// ── Clubs ─────────────────────────────────────────────────────────────────────
export const clubsApi = {
  list: () =>
    api.get<Club[]>('/clubs').then(r => r.data),

  get: (id: string) =>
    api.get<Club>(`/clubs/${id}`).then(r => r.data),

  criteria: (clubId: string) =>
    api.get<Criterion[]>(`/clubs/${clubId}/criteria`).then(r => r.data),
}

// ── Achievements ─────────────────────────────────────────────────────────────
export const achievementsApi = {
  list: (params?: { student_id?: string; club_id?: string }) =>
    api.get<Achievement[]>('/achievements', { params }).then(r => r.data),

  log: (payload: LogAchievementPayload) =>
    api.post<Achievement>('/achievements', payload).then(r => r.data),

  delete: (id: string) =>
    api.delete(`/achievements/${id}`),

  criteriaStatus: (studentId: string, clubId: string) =>
    api.get<CriteriaStatus>('/achievements/criteria-status', {
      params: { student_id: studentId, club_id: clubId },
    }).then(r => r.data),
}

// ── Applications ─────────────────────────────────────────────────────────────
export const applicationsApi = {
  list: (params?: { status?: string; club_id?: string; student_id?: string }) =>
    api.get<Application[]>('/applications', { params }).then(r => r.data),

  get: (id: string) =>
    api.get<Application>(`/applications/${id}`).then(r => r.data),

  update: (id: string, payload: UpdateApplicationPayload) =>
    api.patch<Application>(`/applications/${id}`, payload).then(r => r.data),
}

// ── Notifications ─────────────────────────────────────────────────────────────
export const notificationsApi = {
  list: (unreadOnly = false) =>
    api.get<Notification[]>('/notifications', { params: { unread_only: unreadOnly } })
      .then(r => r.data),

  unreadCount: () =>
    api.get<{ count: number }>('/notifications/unread-count').then(r => r.data),

  markRead: (id: string) =>
    api.post<Notification>(`/notifications/${id}/read`).then(r => r.data),

  markAllRead: () =>
    api.post('/notifications/read-all'),
}

// ── Staff ─────────────────────────────────────────────────────────────────────
export const staffApi = {
  list: () =>
    api.get<Staff[]>('/staff').then(r => r.data),
}

export default api
