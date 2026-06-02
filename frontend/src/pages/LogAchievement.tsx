import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { Trophy, ChevronDown } from 'lucide-react'
import { studentsApi, clubsApi, achievementsApi, staffApi } from '@/api/client'
import toast from 'react-hot-toast'

export default function LogAchievement() {
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const qc = useQueryClient()

  const [studentId, setStudentId] = useState(params.get('student') ?? '')
  const [clubId, setClubId] = useState('')
  const [criterionId, setCriterionId] = useState('')
  const [staffId, setStaffId] = useState('')
  const [evidenceNote, setEvidenceNote] = useState('')
  const [evidenceUrl, setEvidenceUrl] = useState('')

  const { data: students = [] } = useQuery({ queryKey: ['students'], queryFn: () => studentsApi.list({ is_active: true }) })
  const { data: clubs = [] } = useQuery({ queryKey: ['clubs'], queryFn: clubsApi.list })
  const { data: staffList = [] } = useQuery({ queryKey: ['staff'], queryFn: staffApi.list })

  // Flatten clubs including sub-clubs for selection
  const allClubs = clubs.flatMap(c => [c, ...c.sub_clubs])

  const { data: criteria = [] } = useQuery({
    queryKey: ['criteria', clubId],
    queryFn: () => clubsApi.criteria(clubId),
    enabled: !!clubId,
  })

  // Reset criterion when club changes
  useEffect(() => { setCriterionId('') }, [clubId])

  const mutation = useMutation({
    mutationFn: achievementsApi.log,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['achievements'] })
      qc.invalidateQueries({ queryKey: ['applications'] })
      qc.invalidateQueries({ queryKey: ['notifications'] })
      toast.success('Achievement logged! Criteria checked automatically.')
      navigate(studentId ? `/students/${studentId}` : '/students')
    },
    onError: (err: any) => {
      toast.error(err.response?.data?.detail ?? 'Failed to log achievement')
    },
  })

  const canSubmit = studentId && criterionId

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="page-title">Log Achievement</h1>
        <p className="text-slate-400 text-sm mt-1">
          Record a student's achievement against a club criterion. The system will automatically
          check if they have now met all criteria for an award.
        </p>
      </div>

      <div className="card p-6 space-y-5">
        {/* Student */}
        <div>
          <label htmlFor="select-student" className="label">Student *</label>
          <div className="relative">
            <select
              id="select-student"
              className="input pr-9 appearance-none"
              value={studentId}
              onChange={e => setStudentId(e.target.value)}
            >
              <option value="">Select a student…</option>
              {students.map(s => (
                <option key={s.id} value={s.id}>
                  {s.name} — Year {s.year_group}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
          </div>
        </div>

        {/* Club */}
        <div>
          <label htmlFor="select-club" className="label">Club *</label>
          <div className="relative">
            <select
              id="select-club"
              className="input pr-9 appearance-none"
              value={clubId}
              onChange={e => setClubId(e.target.value)}
            >
              <option value="">Select a club…</option>
              {allClubs.map(c => (
                <option key={c.id} value={c.id}>
                  {c.parent_club_id ? `  ↳ ${c.name}` : c.name}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
          </div>
        </div>

        {/* Criterion */}
        {clubId && (
          <div className="animate-slide-up">
            <label className="label">Criterion *</label>
            <div className="space-y-2">
              {criteria.length === 0 ? (
                <p className="text-sm text-slate-500">No criteria defined for this club yet.</p>
              ) : (
                criteria.map(c => (
                  <button
                    key={c.id}
                    id={`criterion-${c.id}`}
                    type="button"
                    onClick={() => setCriterionId(c.id)}
                    className={`w-full text-left p-3.5 rounded-xl border transition-all duration-200 ${
                      criterionId === c.id
                        ? 'border-accent/60 bg-accent/10 text-white'
                        : 'border-surface-border bg-surface-elevated text-slate-300 hover:border-surface-border/80 hover:bg-surface-elevated/80'
                    }`}
                  >
                    <p className="text-sm font-medium">{c.title}</p>
                    {c.description && (
                      <p className="text-xs text-slate-500 mt-0.5">{c.description}</p>
                    )}
                    {c.required_count > 1 && (
                      <p className="text-xs text-accent-light mt-1">Requires {c.required_count} instances</p>
                    )}
                  </button>
                ))
              )}
            </div>
          </div>
        )}

        {/* Evidence */}
        <div>
          <label htmlFor="evidence-note" className="label">Evidence Note</label>
          <textarea
            id="evidence-note"
            className="input min-h-[90px] resize-y"
            placeholder="Describe the achievement or provide context…"
            value={evidenceNote}
            onChange={e => setEvidenceNote(e.target.value)}
          />
        </div>

        <div>
          <label htmlFor="evidence-url" className="label">Evidence URL (optional)</label>
          <input
            id="evidence-url"
            type="url"
            className="input"
            placeholder="https://drive.google.com/…"
            value={evidenceUrl}
            onChange={e => setEvidenceUrl(e.target.value)}
          />
        </div>

        {/* Logged by */}
        <div>
          <label htmlFor="logged-by" className="label">Logged by (optional)</label>
          <div className="relative">
            <select
              id="logged-by"
              className="input pr-9 appearance-none"
              value={staffId}
              onChange={e => setStaffId(e.target.value)}
            >
              <option value="">Select staff member…</option>
              {staffList.map(s => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
          </div>
        </div>

        {/* Submit */}
        <div className="pt-2 border-t border-surface-border flex gap-3">
          <button
            id="submit-achievement-btn"
            onClick={() => mutation.mutate({
              student_id: studentId,
              criterion_id: criterionId,
              logged_by_staff_id: staffId || undefined,
              evidence_note: evidenceNote || undefined,
              evidence_url: evidenceUrl || undefined,
            })}
            disabled={!canSubmit || mutation.isPending}
            className="btn-primary"
          >
            <Trophy className="w-4 h-4" />
            {mutation.isPending ? 'Saving…' : 'Log Achievement'}
          </button>
          <button onClick={() => navigate(-1)} className="btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  )
}
