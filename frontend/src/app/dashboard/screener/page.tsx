'use client'

import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { screenerAPI } from '@/lib/api'
import { toast } from 'sonner'
import { formatNumber, formatPercentage } from '@/lib/utils'
import { Search, Filter, TrendingUp, X } from 'lucide-react'
import Link from 'next/link'

interface Filter {
  field: string
  min?: number
  max?: number
}

export default function ScreenerPage() {
  const [filters, setFilters] = useState<Record<string, any>>({})
  const [activeFilters, setActiveFilters] = useState<Filter[]>([])

  // Fetch available filters
  const { data: availableFilters } = useQuery({
    queryKey: ['screener-filters'],
    queryFn: async () => {
      const response = await screenerAPI.getFilters()
      return response.data.filters
    },
  })

  // Fetch preset screens
  const { data: presets } = useQuery({
    queryKey: ['screener-presets'],
    queryFn: async () => {
      const response = await screenerAPI.getPresets()
      return response.data.presets
    },
  })

  // Screen mutation
  const screenMutation = useMutation({
    mutationFn: (filters: any) => screenerAPI.screen({ filters }),
    onSuccess: () => {
      toast.success('Screen completed successfully')
    },
    onError: () => {
      toast.error('Failed to run screen')
    },
  })

  const handleAddFilter = (field: string, type: 'min' | 'max', value: string) => {
    const numValue = parseFloat(value)
    if (isNaN(numValue)) return

    setFilters((prev: any) => ({
      ...prev,
      [field]: {
        ...prev[field],
        [type]: numValue,
      },
    }))
  }

  const handleRunScreen = () => {
    screenMutation.mutate(filters)
  }

  const handleRunPreset = (presetKey: string) => {
    if (presets && presets[presetKey]) {
      const presetFilters = presets[presetKey].filters
      setFilters(presetFilters)
      screenMutation.mutate(presetFilters)
    }
  }

  const handleRemoveFilter = (field: string) => {
    const newFilters = { ...filters }
    delete newFilters[field]
    setFilters(newFilters)
  }

  const results = screenMutation.data?.data.results || []

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Stock Screener</h1>
        <p className="text-muted-foreground">Filter stocks by 50+ criteria</p>
      </div>

      <Tabs defaultValue="custom">
        <TabsList>
          <TabsTrigger value="custom">Custom Screen</TabsTrigger>
          <TabsTrigger value="presets">Preset Strategies</TabsTrigger>
        </TabsList>

        {/* Custom Screen */}
        <TabsContent value="custom" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Build Your Screen</CardTitle>
              <CardDescription>Add filters to find stocks matching your criteria</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {/* Market Cap */}
                <div className="space-y-2">
                  <Label>Market Cap (Cr)</Label>
                  <div className="flex gap-2">
                    <Input
                      type="number"
                      placeholder="Min"
                      onChange={(e) => handleAddFilter('market_cap', 'min', e.target.value)}
                    />
                    <Input
                      type="number"
                      placeholder="Max"
                      onChange={(e) => handleAddFilter('market_cap', 'max', e.target.value)}
                    />
                  </div>
                </div>

                {/* P/E Ratio */}
                <div className="space-y-2">
                  <Label>P/E Ratio</Label>
                  <div className="flex gap-2">
                    <Input
                      type="number"
                      placeholder="Min"
                      onChange={(e) => handleAddFilter('pe_ratio', 'min', e.target.value)}
                    />
                    <Input
                      type="number"
                      placeholder="Max"
                      onChange={(e) => handleAddFilter('pe_ratio', 'max', e.target.value)}
                    />
                  </div>
                </div>

                {/* ROE */}
                <div className="space-y-2">
                  <Label>ROE (%)</Label>
                  <div className="flex gap-2">
                    <Input
                      type="number"
                      placeholder="Min"
                      onChange={(e) => handleAddFilter('roe', 'min', e.target.value)}
                    />
                    <Input
                      type="number"
                      placeholder="Max"
                      onChange={(e) => handleAddFilter('roe', 'max', e.target.value)}
                    />
                  </div>
                </div>

                {/* Debt/Equity */}
                <div className="space-y-2">
                  <Label>Debt/Equity</Label>
                  <div className="flex gap-2">
                    <Input
                      type="number"
                      placeholder="Min"
                      onChange={(e) => handleAddFilter('debt_to_equity', 'min', e.target.value)}
                    />
                    <Input
                      type="number"
                      placeholder="Max"
                      onChange={(e) => handleAddFilter('debt_to_equity', 'max', e.target.value)}
                    />
                  </div>
                </div>

                {/* Revenue Growth */}
                <div className="space-y-2">
                  <Label>Revenue Growth 3Y CAGR (%)</Label>
                  <div className="flex gap-2">
                    <Input
                      type="number"
                      placeholder="Min"
                      onChange={(e) => handleAddFilter('revenue_growth_3y_cagr', 'min', e.target.value)}
                    />
                    <Input
                      type="number"
                      placeholder="Max"
                      onChange={(e) => handleAddFilter('revenue_growth_3y_cagr', 'max', e.target.value)}
                    />
                  </div>
                </div>

                {/* Current Ratio */}
                <div className="space-y-2">
                  <Label>Current Ratio</Label>
                  <div className="flex gap-2">
                    <Input
                      type="number"
                      placeholder="Min"
                      onChange={(e) => handleAddFilter('current_ratio', 'min', e.target.value)}
                    />
                    <Input
                      type="number"
                      placeholder="Max"
                      onChange={(e) => handleAddFilter('current_ratio', 'max', e.target.value)}
                    />
                  </div>
                </div>
              </div>

              {/* Active Filters */}
              {Object.keys(filters).length > 0 && (
                <div className="mt-4 p-4 bg-muted rounded-lg">
                  <p className="text-sm font-medium mb-2">Active Filters:</p>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(filters).map(([field, value]: [string, any]) => (
                      <Badge key={field} variant="secondary" className="gap-2">
                        {field}: {value.min && `≥${value.min}`} {value.min && value.max && '&'} {value.max && `≤${value.max}`}
                        <X
                          className="h-3 w-3 cursor-pointer"
                          onClick={() => handleRemoveFilter(field)}
                        />
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              <Button
                className="mt-4 w-full"
                onClick={handleRunScreen}
                disabled={screenMutation.isPending || Object.keys(filters).length === 0}
              >
                <Search className="mr-2 h-4 w-4" />
                {screenMutation.isPending ? 'Screening...' : 'Run Screen'}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Preset Strategies */}
        <TabsContent value="presets">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {presets && Object.entries(presets).map(([key, preset]: [string, any]) => (
              <Card key={key} className="hover:shadow-md transition-shadow cursor-pointer">
                <CardHeader>
                  <CardTitle>{preset.name}</CardTitle>
                  <CardDescription>{preset.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button
                    className="w-full"
                    onClick={() => handleRunPreset(key)}
                    disabled={screenMutation.isPending}
                  >
                    <TrendingUp className="mr-2 h-4 w-4" />
                    Run This Screen
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Results */}
      {results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Results ({screenMutation.data?.data.total_count})</CardTitle>
            <CardDescription>
              Found in {screenMutation.data?.data.execution_time_ms.toFixed(0)}ms
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Symbol</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Sector</TableHead>
                  <TableHead className="text-right">Market Cap</TableHead>
                  <TableHead className="text-right">P/E</TableHead>
                  <TableHead className="text-right">ROE</TableHead>
                  <TableHead className="text-right">D/E</TableHead>
                  <TableHead></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.map((stock: any) => (
                  <TableRow key={stock.symbol}>
                    <TableCell className="font-medium">{stock.symbol}</TableCell>
                    <TableCell>{stock.name}</TableCell>
                    <TableCell>{stock.sector}</TableCell>
                    <TableCell className="text-right">{formatNumber(stock.market_cap)}</TableCell>
                    <TableCell className="text-right">{formatNumber(stock.pe_ratio)}</TableCell>
                    <TableCell className="text-right">{stock.roe ? formatPercentage(stock.roe, 1) : 'N/A'}</TableCell>
                    <TableCell className="text-right">{formatNumber(stock.debt_to_equity)}</TableCell>
                    <TableCell>
                      <Link href={`/dashboard/companies/${stock.symbol}`}>
                        <Button size="sm" variant="outline">View</Button>
                      </Link>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
