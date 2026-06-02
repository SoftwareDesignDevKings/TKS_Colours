import { Outlet, NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard, Users, Trophy, ClipboardList,
  Bell, BookOpen, PlusCircle, Menu, X,
} from 'lucide-react'
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { notificationsApi } from '@/api/client'

const navItems = [
  { to: '/dashboard',       label: 'Dashboard',     icon: LayoutDashboard },
  { to: '/students',        label: 'Students',      icon: Users },
  { to: '/clubs',           label: 'Clubs',         icon: BookOpen },
  { to: '/achievements/new',label: 'Log Achievement',icon: PlusCircle },
  { to: '/applications',    label: 'Applications',  icon: ClipboardList },
  { to: '/notifications',   label: 'Notifications', icon: Bell },
]

export default function AppShell() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()

  const { data: countData } = useQuery({
    queryKey: ['notifications', 'unread-count'],
    queryFn: notificationsApi.unreadCount,
    refetchInterval: 60_000,
  })
  const unreadCount = countData?.count ?? 0

  return (
    <div className="flex h-screen overflow-hidden bg-surface">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/60 backdrop-blur-sm lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed inset-y-0 left-0 z-30 w-64 flex flex-col
          bg-surface-card border-r border-surface-border
          transform transition-transform duration-300 ease-in-out
          lg:static lg:translate-x-0
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        {/* Logo */}
        <div className="flex items-center justify-between px-5 py-5 border-b border-surface-border">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accent to-violet-400 flex items-center justify-center shadow-glow">
              <Trophy className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-sm font-bold text-white leading-tight">TKS Colours</p>
              <p className="text-xs text-slate-500 leading-tight">Achievement Tracker</p>
            </div>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="btn-ghost p-1.5 lg:hidden"
            aria-label="Close menu"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          {navItems.map(({ to, label, icon: Icon }) => {
            const isActive = location.pathname.startsWith(to) && to !== '/'
            return (
              <NavLink
                key={to}
                to={to}
                onClick={() => setSidebarOpen(false)}
                className={isActive ? 'nav-item-active' : 'nav-item'}
              >
                <Icon className="w-4 h-4 flex-shrink-0" />
                <span className="flex-1">{label}</span>
                {to === '/notifications' && unreadCount > 0 && (
                  <span className="flex items-center justify-center w-5 h-5 rounded-full bg-accent text-white text-[10px] font-bold animate-pulse-soft">
                    {unreadCount > 9 ? '9+' : unreadCount}
                  </span>
                )}
              </NavLink>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="px-5 py-4 border-t border-surface-border">
          <p className="text-xs text-slate-600">MVP — Staff Only</p>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top bar (mobile) */}
        <header className="lg:hidden flex items-center gap-3 px-4 py-3 border-b border-surface-border bg-surface-card">
          <button
            onClick={() => setSidebarOpen(true)}
            className="btn-ghost p-2"
            aria-label="Open menu"
          >
            <Menu className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-2">
            <Trophy className="w-4 h-4 text-accent-light" />
            <span className="font-semibold text-white text-sm">TKS Colours</span>
          </div>
          {unreadCount > 0 && (
            <NavLink to="/notifications" className="ml-auto">
              <div className="relative">
                <Bell className="w-5 h-5 text-slate-400" />
                <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-accent text-white text-[9px] font-bold flex items-center justify-center">
                  {unreadCount > 9 ? '9+' : unreadCount}
                </span>
              </div>
            </NavLink>
          )}
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-6 xl:p-8">
          <div className="max-w-6xl mx-auto animate-in">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
