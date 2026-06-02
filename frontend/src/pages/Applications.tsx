import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link, useSearchParams } from 'react-router-dom'
import { ClipboardList, ArrowRight } from 'lucide-react'
import { applicationsApi } from '@/api/client'
import { format } from 'date-fns'
import type { ApplicationStatus } from '@/types'

const STATUS_TABS: { value: ApplicationStatus | ''; label: string; class: string }[] = [
  { value: '', label: 'All', class: 'bg-slate-500/20 text-slate-300' },
  { value: 'pending', label: 'Pending', class: 'bg-amber-500/20 text-amber-400' },
  { value: 'approved', label: 'Approved', class: 'bg-emerald-500/20 text-emerald-400' },
  { value: 'rejected', label: 'Rejected', class: 'bg-red-500/20 text-red-400' },
]

export default function Applications() {
  const [params] = useSearchParams()
  const [statusFilter, setStatusFilter] = useState<ApplicationStatus | ''>(
    (params.get('status') as ApplicationStatus) ?? ''
  )

  const { data: applications = [], isLoading } = useQuery({
    queryKey: ['applications', statusFilter],
    queryFn: () => applicationsApi.list(statusFilter ? { status: statusFilter } : {}),
  })

  return (
    <div className="space-y-5">
      <div className="page-header">
        <div>
          <h1 className="page-title">Applications</h1>
          <p className="text-slate-400 text-sm mt-0.5">{applications.length} results</p>
        </div>
      </div>

      {/* Status filter tabs */}
      <div className="flex flex-wrap gap-2">
        {STATUS_TABS.map(tab => (
          <button
            key={tab.value}
            id={`filter-${tab.value || 'all'}`}
            onClick={() => setStatusFilter(tab.value)}
            className={`badge px-3 py-1.5 text-xs font-medium cursor-pointer transition-all duration-200
              ${statusFilter === tab.value ? tab.class + ' ring-1 ring-current' : 'bg-surface-elevated text-slate-400 hover:text-white'}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* List */}
      <div className="card overflow-hidden">
        {isLoading ? (
          <div className="flex items-center justify-center py-16">
            <div className="w-8 h-8 border-2 border-accent/40 border-t-accent rounded-full animate-spin" />
          </div>
        ) : applications.length === 0 ? (
          <div className="flex flex-col items-center py-16 text-slate-500">
            <ClipboardList className="w-10 h-10 mb-3 opacity-40" />
            <p className="text-sm">No applications found</p>
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Club</th>
                <th>Applied</th>
                <th>Status</th>
                <th>Trigger</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {applications.map(app => (
                <tr key={app.id}>
                  <td className="font-medium text-white">{app.student?.name ?? '—'}</td>
                  <td>
                    <span className="text-slate-300">{app.club?.name ?? '—'}</span>
                  </td>
                  <td className="text-slate-400 text-xs">
                    {format(new Date(app.applied_at), 'd MMM yyyy')}
                  </td>
                  <td>
                    <span className={`badge badge-${app.status}`}>{app.status}</span>
                  </td>
                  <td>
                    <span className={`badge text-xs ${app.auto_triggered ? 'bg-violet-500/20 text-violet-400' : 'bg-slate-500/20 text-slate-400'}`}>
                      {app.auto_triggered ? 'Auto' : 'Manual'}
                    </span>
                  </td>
                  <td className="text-right">
                    <Link
                      to={`/applications/${app.id}`}
                      className="btn-ghost text-xs py-1 px-2 inline-flex"
                    >
                      Review <ArrowRight className="w-3 h-3" />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
