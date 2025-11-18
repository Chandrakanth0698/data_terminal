'use client'

import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { companiesAPI, screenerAPI, portfolioAPI } from '@/lib/api'
import { TrendingUp, TrendingDown, Search, Briefcase, Bell, Target } from 'lucide-react'
import { formatCurrency, formatPercentage, getChangeClass } from '@/lib/utils'
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function DashboardPage() {
  // Fetch market movers
  const { data: marketMovers } = useQuery({
    queryKey: ['market-movers'],
    queryFn: async () => {
      const response = await companiesAPI.list({ limit: 10 })
      return response.data
    },
  })

  // Fetch user's portfolios
  const { data: portfolios } = useQuery({
    queryKey: ['portfolios'],
    queryFn: async () => {
      const response = await portfolioAPI.list()
      return response.data
    },
  })

  const stats = [
    {
      name: 'Total Holdings',
      value: portfolios?.reduce((sum: number, p: any) => sum + (p.holdings?.length || 0), 0) || 0,
      icon: Briefcase,
      color: 'text-blue-600',
    },
    {
      name: 'Active Alerts',
      value: 0,
      icon: Bell,
      color: 'text-yellow-600',
    },
    {
      name: 'Watchlist',
      value: 0,
      icon: Target,
      color: 'text-green-600',
    },
    {
      name: 'Screens Saved',
      value: 0,
      icon: Search,
      color: 'text-purple-600',
    },
  ]

  const presetScreens = [
    { name: 'Value Stocks', key: 'value_stocks' },
    { name: 'Growth Stocks', key: 'growth_stocks' },
    { name: 'Dividend Aristocrats', key: 'dividend_aristocrats' },
    { name: 'Quality Stocks', key: 'quality_stocks' },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">Welcome back! Here's your market overview.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.name}
              </CardTitle>
              <stat.icon className={`h-5 w-5 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Quick Screens */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Screens</CardTitle>
            <CardDescription>Run popular screening strategies</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {presetScreens.map((screen) => (
              <Link key={screen.key} href={`/dashboard/screener?preset=${screen.key}`}>
                <Button variant="outline" className="w-full justify-start">
                  <Search className="mr-2 h-4 w-4" />
                  {screen.name}
                </Button>
              </Link>
            ))}
          </CardContent>
        </Card>

        {/* My Portfolios */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>My Portfolios</CardTitle>
                <CardDescription>Track your investments</CardDescription>
              </div>
              <Link href="/dashboard/portfolio">
                <Button variant="outline" size="sm">View All</Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {portfolios && portfolios.length > 0 ? (
              <div className="space-y-3">
                {portfolios.slice(0, 3).map((portfolio: any) => (
                  <div key={portfolio.id} className="flex items-center justify-between p-3 rounded-lg border">
                    <div>
                      <p className="font-medium">{portfolio.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {formatCurrency(portfolio.total_value)}
                      </p>
                    </div>
                    {portfolio.return_percentage !== null && (
                      <Badge variant={portfolio.return_percentage >= 0 ? 'success' : 'destructive'}>
                        {formatPercentage(portfolio.return_percentage)}
                      </Badge>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-6 text-muted-foreground">
                <p>No portfolios yet</p>
                <Link href="/dashboard/portfolio">
                  <Button className="mt-2" size="sm">Create Portfolio</Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Market Overview */}
      <Card>
        <CardHeader>
          <CardTitle>Market Overview</CardTitle>
          <CardDescription>Recent market activity</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {marketMovers?.slice(0, 5).map((company: any) => (
              <Link key={company.id} href={`/dashboard/companies/${company.symbol}`}>
                <div className="flex items-center justify-between p-3 rounded-lg border hover:bg-accent transition-colors cursor-pointer">
                  <div className="flex-1">
                    <p className="font-medium">{company.symbol}</p>
                    <p className="text-sm text-muted-foreground truncate">{company.name}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium">{formatCurrency(company.market_cap, 'INR')}</p>
                    <p className="text-sm text-muted-foreground">{company.sector}</p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
