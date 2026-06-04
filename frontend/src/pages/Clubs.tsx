import { useState, useMemo, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { BookOpen, Trophy, Medal, Star, ChevronDown, ChevronRight, Cpu, Users } from 'lucide-react'
import { clubsApi } from '@/api/client'
import type { Club, Criterion } from '@/types'

// ── Tier detection helpers ────────────────────────────────────────────────────

type Tier = 'half' | 'full' | 'honour' | 'other'

function detectTier(slug: string): Tier {
  if (slug.includes('half-colour')) return 'half'
  if (slug.includes('full-colour')) return 'full'
  if (slug.includes('honour-colour')) return 'honour'
  return 'other'
}

interface TierMeta {
  label: string
  shortLabel: string
  icon: React.FC<{ className?: string; style?: React.CSSProperties }>
  gradientFrom: string
  gradientTo: string
  borderColor: string
  badgeBg: string
  badgeText: string
}

const TIER_META: Record<Tier, TierMeta> = {
  half: {
    label: 'Half Colours',
    shortLabel: '½',
    icon: Medal,
    gradientFrom: 'rgba(148,163,184,0.12)',
    gradientTo: 'rgba(100,116,139,0.06)',
    borderColor: 'rgba(148,163,184,0.35)',
    badgeBg: 'rgba(148,163,184,0.15)',
    badgeText: '#cbd5e1',
  },
  full: {
    label: 'Full Colours',
    shortLabel: '★',
    icon: Trophy,
    gradientFrom: 'rgba(251,191,36,0.15)',
    gradientTo: 'rgba(245,158,11,0.06)',
    borderColor: 'rgba(251,191,36,0.40)',
    badgeBg: 'rgba(251,191,36,0.15)',
    badgeText: '#fcd34d',
  },
  honour: {
    label: 'Honour Colours',
    shortLabel: '✦',
    icon: Star,
    gradientFrom: 'rgba(167,139,250,0.15)',
    gradientTo: 'rgba(139,92,246,0.06)',
    borderColor: 'rgba(167,139,250,0.40)',
    badgeBg: 'rgba(167,139,250,0.15)',
    badgeText: '#c4b5fd',
  },
  other: {
    label: 'Sub-club',
    shortLabel: '○',
    icon: Users,
    gradientFrom: 'rgba(71,85,105,0.10)',
    gradientTo: 'rgba(51,65,85,0.05)',
    borderColor: 'rgba(71,85,105,0.30)',
    badgeBg: 'rgba(71,85,105,0.20)',
    badgeText: '#94a3b8',
  },
}

// ── Criterion row ─────────────────────────────────────────────────────────────

function CriterionRow({ criterion }: { criterion: Criterion }) {
  return (
    <div className="flex items-start gap-3">
      <div className="mt-[5px] w-1.5 h-1.5 rounded-full bg-slate-400 flex-shrink-0 opacity-60" />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-slate-200 leading-snug">{criterion.title}</p>
        {criterion.description && (
          <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">{criterion.description}</p>
        )}
        {criterion.year_group_applicable && (
          <span className="inline-flex items-center mt-1.5 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-sky-500/15 text-sky-400 border border-sky-500/20">
            Year {criterion.year_group_applicable}+ only
          </span>
        )}
      </div>
    </div>
  )
}

// ── AND separator ─────────────────────────────────────────────────────────────

function AndSeparator() {
  return (
    <div className="flex items-center gap-2 my-2.5 ml-4">
      <div className="flex-1 h-px" style={{ background: 'rgba(255,255,255,0.07)' }} />
      <span className="text-[10px] font-bold tracking-widest text-slate-600 uppercase">AND</span>
      <div className="flex-1 h-px" style={{ background: 'rgba(255,255,255,0.07)' }} />
    </div>
  )
}

// ── OR separator ──────────────────────────────────────────────────────────────

function OrSeparator() {
  return (
    <div className="flex items-center gap-3 my-4">
      <div className="flex-1 h-px" style={{ background: 'rgba(255,255,255,0.10)' }} />
      <div
        className="flex items-center justify-center w-8 h-8 rounded-full flex-shrink-0"
        style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.10)' }}
      >
        <span className="text-[11px] font-black text-slate-400 uppercase tracking-wider">OR</span>
      </div>
      <div className="flex-1 h-px" style={{ background: 'rgba(255,255,255,0.10)' }} />
    </div>
  )
}

// ── Tier card ─────────────────────────────────────────────────────────────────

interface PathData { subClub: Club; criteria: Criterion[] }
interface TierGroup { tier: Tier; paths: PathData[] }

function TierCard({ group, clubColour }: { group: TierGroup; clubColour: string }) {
  const meta = TIER_META[group.tier]
  const Icon = meta.icon
  const pathCount = group.paths.length
  const totalCriteria = group.paths.reduce((n, p) => n + p.criteria.length, 0)

  return (
    <div
      className="flex flex-col rounded-2xl overflow-hidden"
      style={{
        background: `linear-gradient(160deg, ${meta.gradientFrom}, ${meta.gradientTo})`,
        border: `1px solid ${meta.borderColor}`,
      }}
    >
      {/* Header */}
      <div
        className="px-5 pt-5 pb-4"
        style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}
      >
        <div className="flex items-center gap-3">
          <div
            className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
            style={{ background: clubColour + '22' }}
          >
            <Icon className="w-4 h-4" style={{ color: clubColour }} />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-sm font-bold text-white">{meta.label}</h3>
            <p className="text-[11px] text-slate-500 mt-0.5">
              {pathCount === 1
                ? `${totalCriteria} requirement${totalCriteria !== 1 ? 's' : ''}`
                : `${pathCount} qualifying paths`}
            </p>
          </div>
          <span
            className="px-2.5 py-1 rounded-full text-[11px] font-bold flex-shrink-0"
            style={{ background: meta.badgeBg, color: meta.badgeText }}
          >
            {meta.shortLabel}
          </span>
        </div>
      </div>

      {/* Paths */}
      <div className="flex-1 px-5 py-4">
        {group.paths.map((path, pathIdx) => (
          <div key={path.subClub.id}>
            <div className="space-y-3">
              {path.criteria.length === 0 ? (
                <p className="text-xs text-slate-600 italic">No criteria defined.</p>
              ) : (
                path.criteria.map((criterion, criIdx) => (
                  <div key={criterion.id}>
                    <CriterionRow criterion={criterion} />
                    {criIdx < path.criteria.length - 1 && <AndSeparator />}
                  </div>
                ))
              )}
            </div>
            {pathIdx < group.paths.length - 1 && <OrSeparator />}
          </div>
        ))}
      </div>
    </div>
  )
}

// ── Sub-club chip (for non-colour sub-clubs like Cyber, AI) ──────────────────

function SubClubChip({ club }: { club: Club }) {
  return (
    <div
      className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl"
      style={{
        background: 'rgba(255,255,255,0.03)',
        border: `1px solid rgba(255,255,255,0.07)`,
        borderLeft: `3px solid ${club.colour}`,
      }}
    >
      <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: club.colour }} />
      <div>
        <p className="text-xs font-semibold text-slate-300">{club.name}</p>
        {club.description && (
          <p className="text-[11px] text-slate-500 mt-0.5 leading-relaxed">{club.description}</p>
        )}
      </div>
    </div>
  )
}

// ── Single sub-club criteria loader (hook-safe) ───────────────────────────────
// We render one of these per sub-club so hooks are called at the top level of
// a component, not inside a loop or conditional in a parent component.

interface SubClubLoaderProps {
  subClub: Club
  onLoaded: (subClubId: string, criteria: Criterion[]) => void
}

function SubClubLoader({ subClub, onLoaded }: SubClubLoaderProps) {
  const { data = [], isFetched } = useQuery({
    queryKey: ['criteria', subClub.id],
    queryFn: () => clubsApi.criteria(subClub.id),
  })

  // Notify parent when criteria for this sub-club are ready
  useEffect(() => {
    if (isFetched) onLoaded(subClub.id, data)
  }, [isFetched, data]) // eslint-disable-line react-hooks/exhaustive-deps

  return null // purely a data-fetching component
}

// ── Club panel ────────────────────────────────────────────────────────────────

function ClubPanel({ club }: { club: Club }) {
  const [othersOpen, setOthersOpen] = useState(false)
  const [criteriaMap, setCriteriaMap] = useState<Record<string, Criterion[]>>({})

  const handleLoaded = (subClubId: string, criteria: Criterion[]) => {
    setCriteriaMap(prev => {
      if (prev[subClubId] === criteria) return prev // avoid unnecessary re-renders
      return { ...prev, [subClubId]: criteria }
    })
  }

  const colourSubClubs = club.sub_clubs.filter(s => detectTier(s.slug) !== 'other')
  const otherSubClubs = club.sub_clubs.filter(s => detectTier(s.slug) === 'other')

  const loadedCount = Object.keys(criteriaMap).length
  const isLoading = loadedCount < colourSubClubs.length

  // Build tier groups once all criteria are loaded
  const tierGroups = useMemo<TierGroup[]>(() => {
    const map = new Map<Tier, TierGroup>()
    for (const sub of colourSubClubs) {
      const tier = detectTier(sub.slug)
      if (!map.has(tier)) map.set(tier, { tier, paths: [] })
      map.get(tier)!.paths.push({ subClub: sub, criteria: criteriaMap[sub.id] ?? [] })
    }
    const order: Tier[] = ['half', 'full', 'honour']
    return order.filter(t => map.has(t)).map(t => map.get(t)!)
  }, [criteriaMap, colourSubClubs])

  return (
    <div className="space-y-6">
      {/* Hidden loaders — one per colour sub-club */}
      {colourSubClubs.map(sub => (
        <SubClubLoader key={sub.id} subClub={sub} onLoaded={handleLoaded} />
      ))}

      {/* Club header */}
      <div
        className="flex items-center gap-4 pb-4"
        style={{ borderBottom: '1px solid rgba(255,255,255,0.07)' }}
      >
        <div
          className="w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0"
          style={{ background: club.colour + '20' }}
        >
          <Trophy className="w-6 h-6" style={{ color: club.colour }} />
        </div>
        <div>
          <h2 className="text-xl font-bold text-white">{club.name}</h2>
          {club.description && (
            <p className="text-sm text-slate-400 mt-0.5">{club.description}</p>
          )}
        </div>
      </div>

      {/* Loading spinner */}
      {isLoading && colourSubClubs.length > 0 && (
        <div className="flex items-center justify-center py-12">
          <div className="w-6 h-6 border-2 border-accent/40 border-t-accent rounded-full animate-spin" />
        </div>
      )}

      {/* Tier cards — shown once all loaded */}
      {!isLoading && tierGroups.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {tierGroups.map(group => (
            <TierCard key={group.tier} group={group} clubColour={club.colour} />
          ))}
        </div>
      )}

      {!isLoading && tierGroups.length === 0 && colourSubClubs.length === 0 && (
        <p className="text-sm text-slate-500 italic">No colour criteria defined for this club yet.</p>
      )}

      {/* Non-colour sub-clubs */}
      {otherSubClubs.length > 0 && (
        <div>
          <button
            onClick={() => setOthersOpen(o => !o)}
            className="flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-slate-300 transition-colors uppercase tracking-widest mb-3"
          >
            {othersOpen
              ? <ChevronDown className="w-3 h-3" />
              : <ChevronRight className="w-3 h-3" />}
            Member Sub-clubs ({otherSubClubs.length})
          </button>
          {othersOpen && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {otherSubClubs.map(sub => <SubClubChip key={sub.id} club={sub} />)}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ── Club tab icons ────────────────────────────────────────────────────────────

const SLUG_ICONS: Record<string, React.FC<{ className?: string }>> = {
  robotics: ({ className }) => <Cpu className={className} />,
  media: ({ className }) => <BookOpen className={className} />,
  programming: ({ className }) => <Star className={className} />,
}

// ── Legend strip ─────────────────────────────────────────────────────────────

function Legend() {
  const tiers: Tier[] = ['half', 'full', 'honour']
  return (
    <div className="flex flex-wrap items-center gap-x-5 gap-y-2 px-1">
      {tiers.map(tier => {
        const meta = TIER_META[tier]
        const Icon = meta.icon
        return (
          <div key={tier} className="flex items-center gap-1.5">
            <div
              className="w-5 h-5 rounded-md flex items-center justify-center flex-shrink-0"
              style={{ background: meta.badgeBg }}
            >
              <Icon className="w-3 h-3" style={{ color: meta.badgeText }} />
            </div>
            <span className="text-xs font-medium" style={{ color: meta.badgeText }}>
              {meta.label}
            </span>
          </div>
        )
      })}
      <p className="text-xs text-slate-600 ml-auto hidden sm:block">
        Paths separated by <span className="font-bold text-slate-500">OR</span>
        {' · '}requirements within a path by <span className="font-bold text-slate-500">AND</span>
      </p>
    </div>
  )
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function Clubs() {
  const { data: clubs = [], isLoading } = useQuery({
    queryKey: ['clubs'],
    queryFn: clubsApi.list,
  })

  const topLevel = clubs.filter(c => !c.parent_club_id)
  const [activeSlug, setActiveSlug] = useState<string | null>(null)

  const activeClub = activeSlug
    ? (topLevel.find(c => c.slug === activeSlug) ?? topLevel[0] ?? null)
    : (topLevel[0] ?? null)

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="page-title">Clubs &amp; Criteria</h1>
        <p className="text-slate-400 text-sm mt-1">
          Award criteria for each co-curricular club. A student qualifies when they satisfy{' '}
          <strong className="text-slate-300">any one</strong> qualifying path within a tier.
        </p>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-24">
          <div className="w-8 h-8 border-2 border-accent/40 border-t-accent rounded-full animate-spin" />
        </div>
      ) : topLevel.length === 0 ? (
        <div className="flex flex-col items-center py-16 text-slate-500">
          <BookOpen className="w-10 h-10 mb-3 opacity-40" />
          <p className="text-sm">No clubs found. Run the seed script to get started.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Club tab selector */}
          <div className="flex flex-wrap gap-2">
            {topLevel.map(club => {
              const isActive = activeClub?.id === club.id
              const IconComp = SLUG_ICONS[club.slug]
              return (
                <button
                  key={club.id}
                  onClick={() => setActiveSlug(club.slug)}
                  className={`
                    flex items-center gap-2.5 px-5 py-2.5 rounded-xl text-sm font-semibold
                    transition-all duration-200 focus-visible:outline-none focus-visible:ring-2
                    focus-visible:ring-accent/60
                  `}
                  style={isActive ? {
                    background: `linear-gradient(135deg, ${club.colour}28, ${club.colour}14)`,
                    border: `1px solid ${club.colour}55`,
                    color: '#ffffff',
                    boxShadow: `0 4px 20px ${club.colour}22`,
                    transform: 'scale(1.02)',
                  } : {
                    background: 'rgba(255,255,255,0.04)',
                    border: '1px solid rgba(255,255,255,0.08)',
                    color: '#94a3b8',
                  }}
                >
                  {IconComp && <IconComp className="w-4 h-4" />}
                  {club.name}
                </button>
              )
            })}
          </div>

          {/* Legend */}
          <Legend />

          {/* Active club panel */}
          {activeClub && (
            <div
              key={activeClub.id}
              className="card p-6"
              style={{ borderTop: `3px solid ${activeClub.colour}` }}
            >
              <ClubPanel club={activeClub} />
            </div>
          )}
        </div>
      )}
    </div>
  )
}
