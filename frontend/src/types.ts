// ── Domain types matching backend Pydantic schemas ──────────────────────────

export interface Student {
  id: string
  name: string
  email: string
  year_group: number
  cohort_year: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Club {
  id: string
  name: string
  slug: string
  description: string | null
  colour: string
  parent_club_id: string | null
  is_active: boolean
  sub_clubs: Club[]
}

export interface Criterion {
  id: string
  club_id: string
  title: string
  description: string | null
  required_count: number
  year_group_applicable: number | null
  sort_order: number
  is_active: boolean
}

export interface Achievement {
  id: string
  student_id: string
  criterion_id: string
  logged_by_staff_id: string | null
  evidence_note: string | null
  evidence_url: string | null
  achieved_at: string
  created_at: string
  criterion?: Criterion
}

export type ApplicationStatus = 'pending' | 'approved' | 'rejected' | 'withdrawn'

export interface Application {
  id: string
  student_id: string
  club_id: string
  status: ApplicationStatus
  auto_triggered: boolean
  notes: string | null
  applied_at: string
  decided_at: string | null
  decided_by_id: string | null
  created_at: string
  updated_at: string
  student?: Student
  club?: Club
}

export interface Reminder {
  id: string
  application_id: string
  staff_id: string | null
  due_at: string
  sent_at: string | null
  acknowledged_at: string | null
  created_at: string
}

export interface Staff {
  id: string
  name: string
  email: string
  role: string
  is_active: boolean
}

export type NotificationType =
  | 'criteria_met'
  | 'reminder_due'
  | 'application_approved'
  | 'application_rejected'

export interface Notification {
  id: string
  type: NotificationType
  title: string
  body: string | null
  student_id: string | null
  application_id: string | null
  club_id: string | null
  is_read: boolean
  created_at: string
  read_at: string | null
}

export interface CriteriaStatus {
  club_id: string
  club_name: string
  total_criteria: number
  met_criteria: number
  is_complete: boolean
  criteria_detail: {
    criterion_id: string
    title: string
    required_count: number
    current_count: number
    is_met: boolean
  }[]
}

// ── API payloads ─────────────────────────────────────────────────────────────

export interface CreateStudentPayload {
  name: string
  email: string
  year_group: number
  cohort_year: number
}

export interface LogAchievementPayload {
  student_id: string
  criterion_id: string
  logged_by_staff_id?: string
  evidence_note?: string
  evidence_url?: string
}

export interface UpdateApplicationPayload {
  status?: ApplicationStatus
  notes?: string
  decided_by_id?: string
}
