import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import {
  Users, ClipboardList, Trophy, Bell,
  TrendingUp, ArrowRight, Clock, CheckCircle2,
} from 'lucide-react'
import { applicationsApi, studentsApi, notificationsApi } from '@/api/client'
import { format } from 'date-fns'
import type { Application } from '@/types'

function StatusBadge({ status }: { status: string }) {
  const map: Record<string, string> = {
    pending: 'badge-pending',
    approved: 'badge-approved',
    rejected: 'badge-rejected',
    withdrawn: 'badge-withdrawn',
  }
  return <span className={map[status] ?? 'badge'}>{status}</span>
}

export default function Dashboard() {
  const { data: students = [] } = useQuery({
    queryKey: ['students'],
    queryFn: () => studentsApi.list({ is_active: true }),
  })
  const { data: pendingApps = [] } = useQuery({
    queryKey: ['applications', 'pending'],
    queryFn: () => applicationsApi.list({ status: 'pending' }),
  })
  const { data: recentApps = [] } = useQuery({
    queryKey: ['applications', 'recent'],
    queryFn: () => applicationsApi.list({}),
  })
  const { data: countData } = useQuery({
    queryKey: ['notifications', 'unread-count'],
    queryFn: notificationsApi.unreadCount,
  })

  const approvedCount = recentApps.filter(a => a.status === 'approved').length

  const stats = [
    {
      label: 'Active Students',
      value: students.length,
      icon: Users,
      colour: 'text-indigo-400',
      bg: 'bg-indigo-500/10',
      href: '/students',
    },
    {
      label: 'Pending Applications',
      value: pendingApps.length,
      icon: Clock,
      colour: 'text-amber-400',
      bg: 'bg-amber-500/10',
      href: '/applications?status=pending',
    },
    {
      label: 'Awards Approved',
      value: approvedCount,
      icon: CheckCircle2,
      colour: 'text-emerald-400',
      bg: 'bg-emerald-500/10',
      href: '/applications?status=approved',
    },
    {
      label: 'Unread Alerts',
      value: countData?.count ?? 0,
      icon: Bell,
      colour: 'text-violet-400',
      bg: 'bg-violet-500/10',
      href: '/notifications',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="page-title">Dashboard</h1>
        <p className="text-slate-400 text-sm mt-1">
          {format(new Date(), "EEEE, d MMMM yyyy")}
        </p>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map(({ label, value, icon: Icon, colour, bg, href }) => (
          <Link key={label} to={href} className="stat-card group hover:border-surface-border/80 hover:-translate-y-0.5 transition-all duration-200">
            <div className={`w-10 h-10 rounded-xl ${bg} flex items-center justify-center mb-3`}>
              <Icon className={`w-5 h-5 ${colour}`} />
            </div>
            <p className="text-2xl font-bold text-white">{value}</p>
            <p className="text-xs text-slate-400">{label}</p>
            <ArrowRight className="w-3.5 h-3.5 text-slate-600 group-hover:text-slate-400 mt-1 transition-colors" />
          </Link>
        ))}
      </div>

      {/* Pending applications */}
      <div className="card overflow-hidden">
        <div className="flex items-center justify-between px-5 py-4 border-b border-surface-border">
          <div className="flex items-center gap-2">
            <ClipboardList className="w-4 h-4 text-amber-400" />
            <h2 className="font-semibold text-white text-sm">Pending Applications</h2>
            {pendingApps.length > 0 && (
              <span className="badge bg-amber-500/20 text-amber-400">{pendingApps.length}</span>
            )}
          </div>
          <Link to="/applications?status=pending" className="btn-ghost text-xs py-1.5 px-3">
            View all <ArrowRight className="w-3 h-3" />
          </Link>
        </div>

        {pendingApps.length === 0 ? (
          <div className="flex flex-col items-center py-12 text-slate-500">
            <CheckCircle2 className="w-8 h-8 mb-2 text-emerald-600" />
            <p className="text-sm">No pending applications</p>
          </div>
        ) : (
          <div className="divide-y divide-surface-border/50">
            {pendingApps.slice(0, 5).map((app: Application) => (
              <Link
                key={app.id}
                to={`/applications/${app.id}`}
                className="flex items-center gap-4 px-5 py-3.5 hover:bg-surface-elevated/50 transition-colors group"
              >
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">
                    {app.student?.name ?? 'Student'}
                  </p>
                  <p className="text-xs text-slate-400">
                    {app.club?.name ?? 'Club'} · Applied {format(new Date(app.applied_at), 'd MMM yyyy')}
                  </p>
                </div>
                <StatusBadge status={app.status} />
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-slate-300 transition-colors flex-shrink-0" />
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Link
          to="/achievements/new"
          className="card p-5 flex items-center gap-4 hover:border-accent/40 hover:-translate-y-0.5 transition-all duration-200 group"
        >
          <div className="w-10 h-10 rounded-xl bg-accent/20 flex items-center justify-center flex-shrink-0">
            <Trophy className="w-5 h-5 text-accent-light" />
          </div>
          <div>
            <p className="font-semibold text-white text-sm">Log Achievement</p>
            <p className="text-xs text-slate-400">Record a student's latest achievement</p>
          </div>
          <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-slate-300 ml-auto transition-colors" />
        </Link>
        <Link
          to="/students"
          className="card p-5 flex items-center gap-4 hover:border-indigo-500/40 hover:-translate-y-0.5 transition-all duration-200 group"
        >
          <div className="w-10 h-10 rounded-xl bg-indigo-500/20 flex items-center justify-center flex-shrink-0">
            <TrendingUp className="w-5 h-5 text-indigo-400" />
          </div>
          <div>
            <p className="font-semibold text-white text-sm">View Student Progress</p>
            <p className="text-xs text-slate-400">Browse all students and their criteria</p>
          </div>
          <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-slate-300 ml-auto transition-colors" />
        </Link>
      </div>
    </div>
  )
}
