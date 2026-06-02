import { useQuery } from '@tanstack/react-query'
import { BookOpen, Trophy, CheckSquare } from 'lucide-react'
import { clubsApi } from '@/api/client'
import type { Club } from '@/types'

function CriteriaCount({ clubId }: { clubId: string }) {
  const { data = [] } = useQuery({
    queryKey: ['criteria', clubId],
    queryFn: () => clubsApi.criteria(clubId),
  })
  return (
    <span className="badge bg-slate-500/20 text-slate-400 text-[10px]">
      {data.length} criteria
    </span>
  )
}

function ClubCard({ club, isSubClub = false }: { club: Club; isSubClub?: boolean }) {
  const { data: criteria = [] } = useQuery({
    queryKey: ['criteria', club.id],
    queryFn: () => clubsApi.criteria(club.id),
  })

  return (
    <div className={`card overflow-hidden ${isSubClub ? 'border-l-4' : ''}`}
      style={isSubClub ? { borderLeftColor: club.colour } : {}}>
      {/* Club header */}
      <div className="p-5 border-b border-surface-border">
        <div className="flex items-center gap-3">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
            style={{ background: club.colour + '22' }}
          >
            <Trophy className="w-5 h-5" style={{ color: club.colour }} />
          </div>
          <div>
            <h3 className="font-semibold text-white">{club.name}</h3>
            {club.description && (
              <p className="text-xs text-slate-400 mt-0.5">{club.description}</p>
            )}
          </div>
          <CriteriaCount clubId={club.id} />
        </div>
      </div>

      {/* Criteria list */}
      <div className="divide-y divide-surface-border/50">
        {criteria.length === 0 ? (
          <p className="px-5 py-4 text-sm text-slate-500">No criteria defined yet.</p>
        ) : (
          criteria.map((c, i) => (
            <div key={c.id} className="flex items-start gap-3 px-5 py-3.5">
              <CheckSquare className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm text-slate-200">{c.title}</p>
                {c.description && (
                  <p className="text-xs text-slate-500 mt-0.5">{c.description}</p>
                )}
                {c.required_count > 1 && (
                  <span className="badge bg-violet-500/20 text-violet-400 text-[10px] mt-1">
                    ×{c.required_count} required
                  </span>
                )}
              </div>
              <span className="text-[10px] text-slate-600">{i + 1}</span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default function Clubs() {
  const { data: clubs = [], isLoading } = useQuery({
    queryKey: ['clubs'],
    queryFn: clubsApi.list,
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title">Clubs & Criteria</h1>
        <p className="text-slate-400 text-sm mt-1">
          All co-curricular clubs and their award criteria.
        </p>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-24">
          <div className="w-8 h-8 border-2 border-accent/40 border-t-accent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="space-y-6">
          {clubs.map(club => (
            <div key={club.id} className="space-y-3">
              <ClubCard club={club} />
              {/* Sub-clubs */}
              {club.sub_clubs.length > 0 && (
                <div className="pl-6 space-y-3">
                  {club.sub_clubs.map(sub => (
                    <ClubCard key={sub.id} club={sub} isSubClub />
                  ))}
                </div>
              )}
            </div>
          ))}

          {clubs.length === 0 && (
            <div className="flex flex-col items-center py-16 text-slate-500">
              <BookOpen className="w-10 h-10 mb-3 opacity-40" />
              <p className="text-sm">No clubs found. Run the seed script to get started.</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
