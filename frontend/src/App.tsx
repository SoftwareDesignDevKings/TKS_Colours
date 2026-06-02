import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import AppShell from '@/components/AppShell'
import Dashboard from '@/pages/Dashboard'
import Students from '@/pages/Students'
import StudentProfile from '@/pages/StudentProfile'
import LogAchievement from '@/pages/LogAchievement'
import Applications from '@/pages/Applications'
import ApplicationDetail from '@/pages/ApplicationDetail'
import Clubs from '@/pages/Clubs'
import Notifications from '@/pages/Notifications'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/students" element={<Students />} />
          <Route path="/students/:id" element={<StudentProfile />} />
          <Route path="/achievements/new" element={<LogAchievement />} />
          <Route path="/applications" element={<Applications />} />
          <Route path="/applications/:id" element={<ApplicationDetail />} />
          <Route path="/clubs" element={<Clubs />} />
          <Route path="/notifications" element={<Notifications />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
