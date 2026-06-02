import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ArrowLeft, CheckCircle2, PlusCircle, ClipboardList, Trophy } from 'lucide-react'
import { studentsApi, clubsApi, achievementsApi, applicationsApi } from '@/api/client'
import { format } from 'date-fns'
import type { Club, Achievement, Application } from '@/types'

function ProgressRing({ met, total }: { met: number; total: number }) {
  const pct = total === 0 ? 0 : Math.round((met / total) * 100)
  return (
    <div className="flex flex-col items-center">
      <div className="relative w-16 h-16">
        <svg className="w-16 h-16 -rotate-90" viewBox="0 0 64 64">
          <circle cx="32" cy="32" r="26" fill="none" stroke="#334155" strokeWidth="6" />
          <circle
            cx="32" cy="32" r="26" fill="none"
            stroke={pct === 100 ? '#10b981' : '#7c3aed'}
            strokeWidth="6"
            strokeDasharray={`${2 * Math.PI * 26}`}
            strokeDashoffset={`${2 * Math.PI * 26 * (1 - pct / 100)}`}
            strokeLinecap="round"
            className="transition-all duration-700"
          />
        </svg>
        <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-white">
          {pct}%
        </span>
      </div>
      <p className="text-xs text-slate-400 mt-1">{met}/{total}</p>
    </div>
  )
}

function ClubProgressCard({
  club,
  achievements,
  applications,
  allClubs,
}: {
  club: Club
  achievements: Achievement[]
  applications: Application[]
  allClubs: Club[]
}) {
  const { data: criteria = [] } = useQuery({
    queryKey: ['criteria', club.id],
    queryFn: () => clubsApi.criteria(club.id),
  })

  // Match achievements within the club family by exact ID or by title
  const clubAchievements = achievements.filter(a => {
    if (!a.criterion) return false
    if (a.criterion.club_id === club.id) return true
    
    const achievementClub = allClubs.find(c => c.id === a.criterion?.club_id)
    if (!achievementClub) return false

    const aParentId = achievementClub.parent_club_id || achievementClub.id
    const currentParentId = club.parent_club_id || club.id

    if (aParentId === currentParentId) {
      return criteria.some(c => c.title === a.criterion?.title)
    }
    return false
  })

  const clubApp = applications.find(a => a.club_id === club.id)

  return (
    <div className="card p-5">
      <div className="flex items-center gap-3 mb-4">
        <div
          className="w-8 h-8 rounded-lg flex items-center justify-center"
          style={{ background: club.colour + '33' }}
        >
          <Trophy className="w-4 h-4" style={{ color: club.colour }} />
        </div>
        <div className="flex-1">
          <p className="font-semibold text-white text-sm">{club.name}</p>
          {clubApp && (
            <span className={`badge badge-${clubApp.status} text-[10px]`}>
              {clubApp.status}
            </span>
          )}
        </div>
        <ProgressRing met={clubAchievements.length} total={criteria.length} />
      </div>
      {clubAchievements.length === 0 ? (
        <p className="text-xs text-slate-500">No achievements logged yet</p>
      ) : (
        <ul className="space-y-2">
          {clubAchievements.slice(0, 3).map(a => (
            <li key={a.id} className="criterion-item-met">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-xs font-medium text-white">{a.criterion?.title}</p>
                {a.evidence_note && (
                  <p className="text-[11px] text-slate-400 mt-0.5 line-clamp-2">{a.evidence_note}</p>
                )}
                <p className="text-[10px] text-slate-500 mt-0.5">
                  {format(new Date(a.achieved_at), 'd MMM yyyy')}
                </p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default function StudentProfile() {
  const { id } = useParams<{ id: string }>()

  const { data: student, isLoading } = useQuery({
    queryKey: ['student', id],
    queryFn: () => studentsApi.get(id!),
    enabled: !!id,
  })
  const { data: clubs = [] } = useQuery({
    queryKey: ['clubs'],
    queryFn: clubsApi.list,
  })
  const { data: achievements = [] } = useQuery({
    queryKey: ['achievements', id],
    queryFn: () => achievementsApi.list({ student_id: id }),
    enabled: !!id,
  })
  const { data: applications = [] } = useQuery({
    queryKey: ['applications', 'student', id],
    queryFn: () => applicationsApi.list({ student_id: id }),
    enabled: !!id,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-24">
        <div className="w-8 h-8 border-2 border-accent/40 border-t-accent rounded-full animate-spin" />
      </div>
    )
  }
  if (!student) return <p className="text-slate-400">Student not found.</p>

  // Flatten all clubs including sub-clubs
  const allClubs = clubs.flatMap(c => [c, ...c.sub_clubs])

  return (
    <div className="space-y-6">
      {/* Back */}
      <Link to="/students" className="btn-ghost text-sm inline-flex">
        <ArrowLeft className="w-4 h-4" /> Back to Students
      </Link>

      {/* Header */}
      <div className="card p-6 flex flex-col sm:flex-row gap-4 items-start sm:items-center">
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-accent to-violet-400 flex items-center justify-center text-white font-bold text-xl flex-shrink-0 shadow-glow">
          {student.name.charAt(0).toUpperCase()}
        </div>
        <div className="flex-1">
          <h1 className="page-title">{student.name}</h1>
          <p className="text-slate-400 text-sm">{student.email}</p>
          <div className="flex flex-wrap gap-2 mt-2">
            <span className="badge bg-indigo-500/20 text-indigo-400">Year {student.year_group}</span>
            <span className="badge bg-slate-500/20 text-slate-400">Cohort {student.cohort_year}</span>
            {!student.is_active && <span className="badge bg-red-500/20 text-red-400">Inactive</span>}
          </div>
        </div>
        <Link to={`/achievements/new?student=${id}`} className="btn-primary flex-shrink-0">
          <PlusCircle className="w-4 h-4" /> Log Achievement
        </Link>
      </div>

      {/* Club progress */}
      <div>
        <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wide mb-3">
          Club Progress
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {allClubs.map(club => (
            <ClubProgressCard
              key={club.id}
              club={club}
              achievements={achievements}
              applications={applications}
              allClubs={allClubs}
            />
          ))}
        </div>
      </div>

      {/* Application history */}
      {applications.length > 0 && (
        <div>
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wide mb-3">
            Application History
          </h2>
          <div className="card overflow-hidden">
            <div className="divide-y divide-surface-border/50">
              {applications.map(app => (
                <Link
                  key={app.id}
                  to={`/applications/${app.id}`}
                  className="flex items-center gap-4 px-5 py-3.5 hover:bg-surface-elevated/50 transition-colors"
                >
                  <ClipboardList className="w-4 h-4 text-slate-500 flex-shrink-0" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-white">
                      {app.club?.name ?? 'Club'} Application
                    </p>
                    <p className="text-xs text-slate-400">
                      Applied {format(new Date(app.applied_at), 'd MMM yyyy')}
                      {app.decided_at && ` · Decided ${format(new Date(app.decided_at), 'd MMM yyyy')}`}
                    </p>
                  </div>
                  <span className={`badge badge-${app.status}`}>{app.status}</span>
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
