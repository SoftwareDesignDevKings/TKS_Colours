import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Search, UserPlus, ArrowRight, User, Upload, AlertCircle } from 'lucide-react'
import { studentsApi } from '@/api/client'
import toast from 'react-hot-toast'
import type { CreateStudentPayload } from '@/types'

const YEAR_OPTIONS = [7, 8, 9, 10, 11, 12]
const COHORT_OPTIONS = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i)

export default function Students() {
  const [search, setSearch] = useState('')
  const [yearFilter, setYearFilter] = useState<number | ''>('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState<CreateStudentPayload>({
    name: '', email: '', year_group: 7, cohort_year: new Date().getFullYear(),
  })

  const qc = useQueryClient()

  const { data: students = [], isLoading } = useQuery({
    queryKey: ['students', yearFilter, search],
    queryFn: () => studentsApi.list({
      ...(yearFilter ? { year_group: Number(yearFilter) } : {}),
      ...(search ? { search } : {}),
    }),
  })

  const createMutation = useMutation({
    mutationFn: studentsApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['students'] })
      toast.success('Student added successfully')
      setShowForm(false)
      setForm({ name: '', email: '', year_group: 7, cohort_year: new Date().getFullYear() })
    },
    onError: (err: any) => {
      toast.error(err.response?.data?.detail ?? 'Failed to add student')
    },
  })

  const [importErrors, setImportErrors] = useState<string[]>([])
  
  const importMutation = useMutation({
    mutationFn: studentsApi.bulkImport,
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ['students'] })
      toast.success(data.message)
      if (data.errors && data.errors.length > 0) {
        setImportErrors(data.errors)
      } else {
        setImportErrors([])
      }
    },
    onError: (err: any) => {
      toast.error(err.response?.data?.detail ?? 'Failed to import students')
      setImportErrors([])
    }
  })

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    if (!file.name.endsWith('.csv')) {
      toast.error('Must be a CSV file')
      return
    }
    toast.loading('Importing students...', { id: 'import' })
    importMutation.mutate(file, {
      onSettled: () => toast.dismiss('import'),
    })
    e.target.value = '' // Reset input
  }

  return (
    <div className="space-y-5">
      <div className="page-header">
        <div>
          <h1 className="page-title">Students</h1>
          <p className="text-slate-400 text-sm mt-0.5">{students.length} students</p>
        </div>
        <div className="flex gap-2">
          <label className="btn-secondary cursor-pointer">
            <Upload className="w-4 h-4" />
            <span className="hidden sm:inline">Bulk Import</span>
            <input type="file" accept=".csv" className="hidden" onChange={handleFileUpload} />
          </label>
          <button
            id="add-student-btn"
            onClick={() => setShowForm(v => !v)}
            className="btn-primary"
          >
            <UserPlus className="w-4 h-4" />
            <span className="hidden sm:inline">Add Student</span>
          </button>
        </div>
      </div>
      
      {importErrors.length > 0 && (
        <div className="card p-4 border-amber-500/30 bg-amber-500/5 animate-slide-up">
          <div className="flex items-center gap-2 text-amber-400 mb-2">
            <AlertCircle className="w-5 h-5" />
            <h3 className="font-semibold text-sm">Import completed with some errors</h3>
          </div>
          <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
            {importErrors.map((err, i) => (
              <li key={i}>{err}</li>
            ))}
          </ul>
          <button 
            onClick={() => setImportErrors([])} 
            className="text-xs text-slate-400 hover:text-white mt-3 underline decoration-slate-600 underline-offset-4"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Add student form */}
      {showForm && (
        <div className="card p-5 animate-slide-up">
          <h2 className="text-sm font-semibold text-white mb-4">New Student</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="label">Full Name</label>
              <input
                id="student-name"
                className="input"
                placeholder="e.g. Jane Smith"
                value={form.name}
                onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
              />
            </div>
            <div>
              <label className="label">Email</label>
              <input
                id="student-email"
                type="email"
                className="input"
                placeholder="student@school.edu"
                value={form.email}
                onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
              />
            </div>
            <div>
              <label className="label">Year Group</label>
              <select
                id="student-year"
                className="input"
                value={form.year_group}
                onChange={e => setForm(f => ({ ...f, year_group: Number(e.target.value) }))}
              >
                {YEAR_OPTIONS.map(y => (
                  <option key={y} value={y}>Year {y}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="label">Cohort Year</label>
              <select
                id="student-cohort"
                className="input"
                value={form.cohort_year}
                onChange={e => setForm(f => ({ ...f, cohort_year: Number(e.target.value) }))}
              >
                {COHORT_OPTIONS.map(y => (
                  <option key={y} value={y}>{y}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="flex gap-3 mt-4">
            <button
              id="submit-student-btn"
              onClick={() => createMutation.mutate(form)}
              disabled={!form.name || !form.email || createMutation.isPending}
              className="btn-primary"
            >
              {createMutation.isPending ? 'Saving…' : 'Save Student'}
            </button>
            <button onClick={() => setShowForm(false)} className="btn-secondary">
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            id="student-search"
            className="input pl-9"
            placeholder="Search by name or email…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
        <select
          id="year-filter"
          className="input sm:w-40"
          value={yearFilter}
          onChange={e => setYearFilter(e.target.value ? Number(e.target.value) : '')}
        >
          <option value="">All year groups</option>
          {YEAR_OPTIONS.map(y => (
            <option key={y} value={y}>Year {y}</option>
          ))}
        </select>
      </div>

      {/* Table */}
      <div className="card overflow-hidden">
        {isLoading ? (
          <div className="flex items-center justify-center py-16">
            <div className="w-8 h-8 border-2 border-accent/40 border-t-accent rounded-full animate-spin" />
          </div>
        ) : students.length === 0 ? (
          <div className="flex flex-col items-center py-16 text-slate-500">
            <User className="w-10 h-10 mb-3 opacity-40" />
            <p className="text-sm">No students found</p>
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Year Group</th>
                <th>Cohort</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {students.map(student => (
                <tr key={student.id}>
                  <td className="font-medium text-white">{student.name}</td>
                  <td className="text-slate-400">{student.email}</td>
                  <td>
                    <span className="badge bg-indigo-500/20 text-indigo-400">
                      Year {student.year_group}
                    </span>
                  </td>
                  <td className="text-slate-400">{student.cohort_year}</td>
                  <td className="text-right">
                    <Link
                      to={`/students/${student.id}`}
                      className="btn-ghost text-xs py-1 px-2 inline-flex"
                    >
                      View <ArrowRight className="w-3 h-3" />
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
