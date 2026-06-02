import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Bell, CheckCheck, Trophy, Clock, CheckCircle2, XCircle } from 'lucide-react'
import { notificationsApi } from '@/api/client'
import { formatDistanceToNow } from 'date-fns'
import type { Notification, NotificationType } from '@/types'
import toast from 'react-hot-toast'

const TYPE_CONFIG: Record<NotificationType, { icon: typeof Bell; colour: string; bg: string }> = {
  criteria_met: { icon: Trophy, colour: 'text-amber-400', bg: 'bg-amber-500/10' },
  reminder_due: { icon: Clock, colour: 'text-red-400', bg: 'bg-red-500/10' },
  application_approved: { icon: CheckCircle2, colour: 'text-emerald-400', bg: 'bg-emerald-500/10' },
  application_rejected: { icon: XCircle, colour: 'text-red-400', bg: 'bg-red-500/10' },
}

function NotifCard({ notif }: { notif: Notification }) {
  const qc = useQueryClient()
  const config = TYPE_CONFIG[notif.type] ?? { icon: Bell, colour: 'text-slate-400', bg: 'bg-slate-500/10' }
  const Icon = config.icon

  const markRead = useMutation({
    mutationFn: () => notificationsApi.markRead(notif.id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['notifications'] })
    },
  })

  return (
    <div
      className={`flex gap-4 p-4 rounded-xl border transition-all duration-200 cursor-pointer hover:border-surface-border
        ${notif.is_read ? 'border-surface-border/30 opacity-60' : 'border-surface-border bg-surface-elevated'}`}
      onClick={() => { if (!notif.is_read) markRead.mutate() }}
    >
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${config.bg}`}>
        <Icon className={`w-5 h-5 ${config.colour}`} />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-2">
          <p className={`text-sm font-medium ${notif.is_read ? 'text-slate-400' : 'text-white'}`}>
            {notif.title}
          </p>
          {!notif.is_read && (
            <div className="w-2 h-2 rounded-full bg-accent flex-shrink-0 mt-1.5 animate-pulse-soft" />
          )}
        </div>
        {notif.body && (
          <p className="text-xs text-slate-400 mt-0.5 line-clamp-2">{notif.body}</p>
        )}
        <p className="text-[10px] text-slate-600 mt-1.5">
          {formatDistanceToNow(new Date(notif.created_at), { addSuffix: true })}
        </p>
      </div>
    </div>
  )
}

export default function Notifications() {
  const qc = useQueryClient()

  const { data: notifications = [], isLoading } = useQuery({
    queryKey: ['notifications', 'all'],
    queryFn: () => notificationsApi.list(false),
    refetchInterval: 30_000,
  })

  const markAll = useMutation({
    mutationFn: notificationsApi.markAllRead,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['notifications'] })
      toast.success('All notifications marked as read')
    },
  })

  const unreadCount = notifications.filter(n => !n.is_read).length

  return (
    <div className="space-y-5">
      <div className="page-header">
        <div>
          <h1 className="page-title">Notifications</h1>
          <p className="text-slate-400 text-sm mt-0.5">
            {unreadCount > 0 ? `${unreadCount} unread` : 'All caught up'}
          </p>
        </div>
        {unreadCount > 0 && (
          <button
            id="mark-all-read-btn"
            onClick={() => markAll.mutate()}
            disabled={markAll.isPending}
            className="btn-secondary text-sm"
          >
            <CheckCheck className="w-4 h-4" />
            Mark all read
          </button>
        )}
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-24">
          <div className="w-8 h-8 border-2 border-accent/40 border-t-accent rounded-full animate-spin" />
        </div>
      ) : notifications.length === 0 ? (
        <div className="flex flex-col items-center py-20 text-slate-500">
          <Bell className="w-10 h-10 mb-3 opacity-40" />
          <p className="text-sm">No notifications yet</p>
          <p className="text-xs mt-1 text-slate-600">
            Notifications appear when students meet criteria or applications need attention.
          </p>
        </div>
      ) : (
        <div className="space-y-2">
          {notifications.map(n => (
            <NotifCard key={n.id} notif={n} />
          ))}
        </div>
      )}
    </div>
  )
}
