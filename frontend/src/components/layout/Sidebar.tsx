'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import {
  LayoutDashboard,
  Search,
  TrendingUp,
  Calculator,
  Briefcase,
  FileText,
  Bell,
  BookMarked,
  LogOut,
  Settings,
} from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { useRouter } from 'next/navigation'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Screener', href: '/dashboard/screener', icon: Search },
  { name: 'Companies', href: '/dashboard/companies', icon: TrendingUp },
  { name: 'Valuation', href: '/dashboard/valuation', icon: Calculator },
  { name: 'Portfolio', href: '/dashboard/portfolio', icon: Briefcase },
  { name: 'Research', href: '/dashboard/research', icon: FileText },
  { name: 'Watchlist', href: '/dashboard/watchlist', icon: BookMarked },
  { name: 'Alerts', href: '/dashboard/alerts', icon: Bell },
]

export function Sidebar() {
  const pathname = usePathname()
  const router = useRouter()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  return (
    <div className="flex h-screen w-64 flex-col fixed left-0 top-0 bg-card border-r">
      {/* Logo */}
      <div className="flex h-16 items-center border-b px-6">
        <TrendingUp className="w-8 h-8 text-primary mr-2" />
        <span className="font-bold text-lg">Stock Analysis</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4 overflow-y-auto">
        {navigation.map((item) => {
          const isActive = pathname === item.href || pathname?.startsWith(item.href + '/')
          return (
            <Link key={item.name} href={item.href}>
              <Button
                variant={isActive ? 'secondary' : 'ghost'}
                className={cn(
                  'w-full justify-start',
                  isActive && 'bg-secondary'
                )}
              >
                <item.icon className="mr-3 h-5 w-5" />
                {item.name}
              </Button>
            </Link>
          )
        })}
      </nav>

      {/* User Section */}
      <div className="border-t p-4">
        <div className="mb-3 px-2">
          <p className="text-sm font-medium truncate">{user?.full_name || user?.username}</p>
          <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
        </div>
        <div className="space-y-1">
          <Link href="/dashboard/settings">
            <Button variant="ghost" className="w-full justify-start">
              <Settings className="mr-3 h-5 w-5" />
              Settings
            </Button>
          </Link>
          <Button variant="ghost" className="w-full justify-start" onClick={handleLogout}>
            <LogOut className="mr-3 h-5 w-5" />
            Logout
          </Button>
        </div>
      </div>
    </div>
  )
}
