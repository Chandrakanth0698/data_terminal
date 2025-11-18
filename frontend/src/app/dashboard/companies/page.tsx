'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { companiesAPI } from '@/lib/api'
import { Search } from 'lucide-react'
import { debounce } from '@/lib/utils'
import Link from 'next/link'
import { Badge } from '@/components/ui/badge'
import { formatCurrency } from '@/lib/utils'

export default function CompaniesPage() {
  const [searchQuery, setSearchQuery] = useState('')

  const { data: companies, isLoading } = useQuery({
    queryKey: ['companies-search', searchQuery],
    queryFn: async () => {
      if (!searchQuery || searchQuery.length < 2) return []
      const response = await companiesAPI.search(searchQuery, 20)
      return response.data
    },
    enabled: searchQuery.length >= 2,
  })

  const handleSearch = debounce((value: string) => {
    setSearchQuery(value)
  }, 300)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Companies</h1>
        <p className="text-muted-foreground">Search and analyze NSE/BSE listed companies</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Search Companies</CardTitle>
          <CardDescription>Search by symbol or company name</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search companies..."
              className="pl-10"
              onChange={(e) => handleSearch(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      {isLoading && (
        <div className="text-center py-8 text-muted-foreground">Searching...</div>
      )}

      {companies && companies.length > 0 && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {companies.map((company: any) => (
            <Link key={company.id} href={`/dashboard/companies/${company.symbol}`}>
              <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg">{company.symbol}</CardTitle>
                      <CardDescription className="line-clamp-1">{company.name}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {company.sector && (
                      <Badge variant="secondary">{company.sector}</Badge>
                    )}
                    {company.market_cap && (
                      <p className="text-sm text-muted-foreground">
                        Market Cap: {formatCurrency(company.market_cap, 'INR')}
                      </p>
                    )}
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}

      {searchQuery.length >= 2 && companies && companies.length === 0 && !isLoading && (
        <div className="text-center py-8 text-muted-foreground">
          No companies found matching "{searchQuery}"
        </div>
      )}

      {searchQuery.length < 2 && (
        <div className="text-center py-8 text-muted-foreground">
          Enter at least 2 characters to search
        </div>
      )}
    </div>
  )
}
