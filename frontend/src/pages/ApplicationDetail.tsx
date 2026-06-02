import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ArrowLeft, CheckCircle2, XCircle, User, Trophy, Clock } from 'lucide-react'
import { applicationsApi, staffApi } from '@/api/client'
import { format } from 'date-fns'
import { useState } from 'react'
import toast from 'react-hot-toast'
import type { ApplicationStatus } from '@/types'

export default function ApplicationDetail() {
  const { id } = useParams<{ id: string }>()
  const qc = useQueryClient()
  const [decisionNotes, setDecisionNotes] = useState('')
  const [decisionStaff, setDecisionStaff] = useState('')

  const { data: app, isLoading } = useQuery({
    queryKey: ['application', id],
    queryFn: () => applicationsApi.get(id!),
    enabled: !!id,
  })
  const { data: staffList = [] } = useQuery({
    queryKey: ['staff'],
    queryFn: staffApi.list,
  })

  const updateMutation = useMutation({
    mutationFn: (status: ApplicationStatus) =>
      applicationsApi.update(id!, {
        status,
        notes: decisionNotes || undefined,
        decided_by_id: decisionStaff || undefined,
      }),
    onSuccess: (_, status) => {
      qc.invalidateQueries({ queryKey: ['application', id] })
      qc.invalidateQueries({ queryKey: ['applications'] })
      qc.invalidateQueries({ queryKey: ['notifications'] })
      toast.success(`Application ${status}`)
    },
    onError: (err: any) => {
      toast.error(err.response?.data?.detail ?? 'Failed to update application')
    },
  })

  if (isLoading) return (
    <div className="flex items-center justify-center py-24">
      <div className="w-8 h-8 border-2 border-accent/40 border-t-accent rounded-full animate-spin" />
    </div>
  )
  if (!app) return <p className="text-slate-400">Application not found.</p>

  const isPending = app.status === 'pending'

  return (
    <div className="space-y-6 max-w-2xl">
      <Link to="/applications" className="btn-ghost text-sm inline-flex">
        <ArrowLeft className="w-4 h-4" /> Back to Applications
      </Link>

      {/* Application card */}
      <div className="card p-6 space-y-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Application</p>
            <h1 className="text-xl font-bold text-white">
              {app.club?.name ?? 'Club'} Award
            </h1>
          </div>
          <span className={`badge badge-${app.status} text-sm px-3 py-1`}>{app.status}</span>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="card-elevated p-4 flex items-center gap-3">
            <User className="w-5 h-5 text-indigo-400 flex-shrink-0" />
            <div>
              <p className="text-xs text-slate-500">Student</p>
              <Link to={`/students/${app.student_id}`} className="text-sm font-medium text-white hover:text-accent-light transition-colors">
                {app.student?.name ?? '—'}
              </Link>
              {app.student && (
                <p className="text-xs text-slate-400">Year {app.student.year_group}</p>
              )}
            </div>
          </div>
          <div className="card-elevated p-4 flex items-center gap-3">
            <Trophy className="w-5 h-5 text-amber-400 flex-shrink-0" />
            <div>
              <p className="text-xs text-slate-500">Club</p>
              <p className="text-sm font-medium text-white">{app.club?.name ?? '—'}</p>
              <span className="badge text-[10px] px-2 py-0.5 bg-violet-500/20 text-violet-400">
                {app.auto_triggered ? 'Auto-triggered' : 'Manual'}
              </span>
            </div>
          </div>
        </div>

        <div className="flex gap-6 text-sm text-slate-400">
          <div className="flex items-center gap-1.5">
            <Clock className="w-4 h-4" />
            Applied {format(new Date(app.applied_at), 'd MMMM yyyy')}
          </div>
          {app.decided_at && (
            <div className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Decided {format(new Date(app.decided_at), 'd MMMM yyyy')}
            </div>
          )}
        </div>

        {app.notes && (
          <div className="bg-surface-elevated rounded-xl p-4 border border-surface-border">
            <p className="text-xs text-slate-500 mb-1">Notes</p>
            <p className="text-sm text-slate-300">{app.notes}</p>
          </div>
        )}
      </div>

      {/* Decision panel — only show if pending */}
      {isPending && (
        <div className="card p-6 space-y-4 border-accent/20 animate-slide-up">
          <h2 className="text-sm font-semibold text-white">Make a Decision</h2>

          <div>
            <label htmlFor="decision-notes" className="label">Notes (optional)</label>
            <textarea
              id="decision-notes"
              className="input min-h-[80px] resize-y"
              placeholder="Add any context or reasoning for this decision…"
              value={decisionNotes}
              onChange={e => setDecisionNotes(e.target.value)}
            />
          </div>

          <div>
            <label htmlFor="decision-staff" className="label">Decided by *</label>
            <select
              id="decision-staff"
              className="input"
              value={decisionStaff}
              onChange={e => setDecisionStaff(e.target.value)}
            >
              <option value="">Select staff member…</option>
              {staffList.map(s => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.role === 'admin' ? 'Head of Dept' : s.role})
                </option>
              ))}
            </select>
          </div>

          <div className="flex gap-3 pt-1">
            <button
              id="approve-btn"
              onClick={() => updateMutation.mutate('approved')}
              disabled={updateMutation.isPending}
              className="btn bg-emerald-600 text-white hover:bg-emerald-700"
            >
              <CheckCircle2 className="w-4 h-4" />
              Approve Award
            </button>
            <button
              id="reject-btn"
              onClick={() => updateMutation.mutate('rejected')}
              disabled={updateMutation.isPending}
              className="btn-danger"
            >
              <XCircle className="w-4 h-4" />
              Reject
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
