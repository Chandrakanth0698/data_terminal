import axios, { AxiosError, AxiosResponse } from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (username: string, password: string) =>
    api.post('/auth/login', new URLSearchParams({ username, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    api.post('/auth/register', data),
  getMe: () => api.get('/auth/me'),
}

// Companies API
export const companiesAPI = {
  search: (query: string, limit = 10) =>
    api.get('/companies/search', { params: { query, limit } }),
  getCompany: (symbol: string) => api.get(`/companies/${symbol}`),
  getBySector: (sector: string, limit = 50) =>
    api.get(`/companies/sector/${sector}`, { params: { limit } }),
  list: (params?: { skip?: number; limit?: number; exchange?: string; sector?: string }) =>
    api.get('/companies/', { params }),
}

// Screener API
export const screenerAPI = {
  screen: (data: { filters: any; limit?: number; offset?: number }) =>
    api.post('/screener/screen', data),
  getFilters: () => api.get('/screener/filters'),
  getPresets: () => api.get('/screener/presets'),
  runPreset: (presetName: string, limit = 100, offset = 0) =>
    api.post(`/screener/presets/${presetName}`, null, { params: { limit, offset } }),
}

// Financial API
export const financialAPI = {
  getStatements: (symbol: string, params?: { statement_type?: string; period_type?: string; years?: number }) =>
    api.get(`/financial/${symbol}/statements`, { params }),
  getRatios: (symbol: string, years = 10) =>
    api.get(`/financial/${symbol}/ratios`, { params: { years } }),
  getPeerComparison: (symbol: string) =>
    api.get(`/financial/${symbol}/peer-comparison`),
}

// Valuation API
export const valuationAPI = {
  createDCF: (symbol: string, data: any) =>
    api.post(`/valuation/${symbol}/dcf`, data),
  getDCF: (symbol: string, modelId: number) =>
    api.get(`/valuation/${symbol}/dcf/${modelId}`),
}

// Portfolio API
export const portfolioAPI = {
  list: () => api.get('/portfolio/'),
  create: (data: { name: string; description?: string }) =>
    api.post('/portfolio/', data),
  get: (portfolioId: number) => api.get(`/portfolio/${portfolioId}`),
  addHolding: (portfolioId: number, data: { company_id: number; quantity: number; average_price: number }) =>
    api.post(`/portfolio/${portfolioId}/holdings`, data),
}

// Research Notes API
export const researchAPI = {
  list: () => api.get('/research/'),
  create: (data: any) => api.post('/research/', data),
  get: (noteId: number) => api.get(`/research/${noteId}`),
}

// Alerts API
export const alertsAPI = {
  list: (activeOnly = true) => api.get('/alerts/', { params: { active_only: activeOnly } }),
  create: (data: any) => api.post('/alerts/', data),
  delete: (alertId: number) => api.delete(`/alerts/${alertId}`),
}
