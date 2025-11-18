'use client'

import { useParams } from 'next/navigation'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { companiesAPI, financialAPI } from '@/lib/api'
import { formatNumber, formatCurrency, formatPercentage, formatDate } from '@/lib/utils'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp, TrendingDown, Building2, Globe, Users } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function CompanyPage() {
  const params = useParams()
  const symbol = params.symbol as string

  // Fetch company details
  const { data: company, isLoading: companyLoading } = useQuery({
    queryKey: ['company', symbol],
    queryFn: async () => {
      const response = await companiesAPI.getCompany(symbol)
      return response.data
    },
  })

  // Fetch financial ratios
  const { data: ratiosData } = useQuery({
    queryKey: ['ratios', symbol],
    queryFn: async () => {
      const response = await financialAPI.getRatios(symbol, 5)
      return response.data
    },
  })

  // Fetch peer comparison
  const { data: peerData } = useQuery({
    queryKey: ['peers', symbol],
    queryFn: async () => {
      const response = await financialAPI.getPeerComparison(symbol)
      return response.data
    },
  })

  if (companyLoading) {
    return <div className="flex items-center justify-center h-96">Loading...</div>
  }

  if (!company) {
    return <div className="flex items-center justify-center h-96">Company not found</div>
  }

  const latestRatio = ratiosData?.ratios?.[0]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold">{company.symbol}</h1>
          <p className="text-xl text-muted-foreground">{company.name}</p>
          <div className="flex gap-2 mt-2">
            {company.sector && <Badge variant="secondary">{company.sector}</Badge>}
            {company.industry && <Badge variant="outline">{company.industry}</Badge>}
          </div>
        </div>
        <div className="text-right">
          <p className="text-sm text-muted-foreground">Market Cap</p>
          <p className="text-2xl font-bold">{formatCurrency(company.market_cap, 'INR')}</p>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>P/E Ratio</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{formatNumber(latestRatio?.pe_ratio)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>ROE</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{latestRatio?.roe ? formatPercentage(latestRatio.roe, 1) : 'N/A'}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Debt/Equity</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{formatNumber(latestRatio?.debt_to_equity)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Current Ratio</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{formatNumber(latestRatio?.current_ratio)}</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="ratios">Ratios</TabsTrigger>
          <TabsTrigger value="charts">Charts</TabsTrigger>
          <TabsTrigger value="peers">Peers</TabsTrigger>
          <TabsTrigger value="valuation">Valuation</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Company Overview</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {company.description && (
                <div>
                  <h4 className="font-semibold mb-2">About</h4>
                  <p className="text-sm text-muted-foreground">{company.description}</p>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4">
                {company.website && (
                  <div className="flex items-start gap-2">
                    <Globe className="h-5 w-5 text-muted-foreground mt-0.5" />
                    <div>
                      <p className="text-sm font-medium">Website</p>
                      <a href={company.website} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-600 hover:underline">
                        {company.website}
                      </a>
                    </div>
                  </div>
                )}

                {company.headquarters && (
                  <div className="flex items-start gap-2">
                    <Building2 className="h-5 w-5 text-muted-foreground mt-0.5" />
                    <div>
                      <p className="text-sm font-medium">Headquarters</p>
                      <p className="text-sm text-muted-foreground">{company.headquarters}</p>
                    </div>
                  </div>
                )}

                {company.employees && (
                  <div className="flex items-start gap-2">
                    <Users className="h-5 w-5 text-muted-foreground mt-0.5" />
                    <div>
                      <p className="text-sm font-medium">Employees</p>
                      <p className="text-sm text-muted-foreground">{formatNumber(company.employees)}</p>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Ratios Tab */}
        <TabsContent value="ratios" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            {/* Profitability */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Profitability</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm">ROE</span>
                  <span className="font-medium">{latestRatio?.roe ? formatPercentage(latestRatio.roe, 1) : 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">ROA</span>
                  <span className="font-medium">{latestRatio?.roa ? formatPercentage(latestRatio.roa, 1) : 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Net Margin</span>
                  <span className="font-medium">{latestRatio?.net_margin ? formatPercentage(latestRatio.net_margin, 1) : 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Operating Margin</span>
                  <span className="font-medium">{latestRatio?.operating_margin ? formatPercentage(latestRatio.operating_margin, 1) : 'N/A'}</span>
                </div>
              </CardContent>
            </Card>

            {/* Valuation */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Valuation</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm">P/E Ratio</span>
                  <span className="font-medium">{formatNumber(latestRatio?.pe_ratio)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">P/B Ratio</span>
                  <span className="font-medium">{formatNumber(latestRatio?.pb_ratio)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">P/S Ratio</span>
                  <span className="font-medium">{formatNumber(latestRatio?.ps_ratio)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">EV/EBITDA</span>
                  <span className="font-medium">{formatNumber(latestRatio?.ev_ebitda)}</span>
                </div>
              </CardContent>
            </Card>

            {/* Solvency */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Solvency</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm">Debt/Equity</span>
                  <span className="font-medium">{formatNumber(latestRatio?.debt_to_equity)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Current Ratio</span>
                  <span className="font-medium">{formatNumber(latestRatio?.current_ratio)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Quick Ratio</span>
                  <span className="font-medium">{formatNumber(latestRatio?.quick_ratio)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Interest Coverage</span>
                  <span className="font-medium">{formatNumber(latestRatio?.interest_coverage)}</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Charts Tab */}
        <TabsContent value="charts">
          <Card>
            <CardHeader>
              <CardTitle>Financial Trends</CardTitle>
              <CardDescription>Historical performance over time</CardDescription>
            </CardHeader>
            <CardContent>
              {ratiosData?.ratios && ratiosData.ratios.length > 0 && (
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={ratiosData.ratios.reverse()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="period_end" tickFormatter={(val) => new Date(val).getFullYear().toString()} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="roe" stroke="#8884d8" name="ROE %" />
                    <Line type="monotone" dataKey="roa" stroke="#82ca9d" name="ROA %" />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Peers Tab */}
        <TabsContent value="peers">
          <Card>
            <CardHeader>
              <CardTitle>Peer Comparison</CardTitle>
              <CardDescription>Compare with industry peers</CardDescription>
            </CardHeader>
            <CardContent>
              {peerData?.peers && peerData.peers.length > 0 ? (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Company</TableHead>
                      <TableHead className="text-right">P/E</TableHead>
                      <TableHead className="text-right">ROE</TableHead>
                      <TableHead className="text-right">D/E</TableHead>
                      <TableHead className="text-right">Current Ratio</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    <TableRow className="bg-muted/50">
                      <TableCell className="font-medium">{company.symbol}</TableCell>
                      <TableCell className="text-right">{formatNumber(latestRatio?.pe_ratio)}</TableCell>
                      <TableCell className="text-right">{latestRatio?.roe ? formatPercentage(latestRatio.roe, 1) : 'N/A'}</TableCell>
                      <TableCell className="text-right">{formatNumber(latestRatio?.debt_to_equity)}</TableCell>
                      <TableCell className="text-right">{formatNumber(latestRatio?.current_ratio)}</TableCell>
                    </TableRow>
                    {peerData.peers.map((peer: any) => (
                      <TableRow key={peer.symbol}>
                        <TableCell>{peer.symbol}</TableCell>
                        <TableCell className="text-right">{formatNumber(peer.ratios?.pe_ratio)}</TableCell>
                        <TableCell className="text-right">{peer.ratios?.roe ? formatPercentage(peer.ratios.roe, 1) : 'N/A'}</TableCell>
                        <TableCell className="text-right">{formatNumber(peer.ratios?.debt_to_equity)}</TableCell>
                        <TableCell className="text-right">{formatNumber(peer.ratios?.current_ratio)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                <p className="text-center text-muted-foreground py-8">No peer data available</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Valuation Tab */}
        <TabsContent value="valuation">
          <Card>
            <CardHeader>
              <CardTitle>Valuation Analysis</CardTitle>
              <CardDescription>Build DCF model and analyze fair value</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <p className="text-muted-foreground mb-4">Create a DCF model to estimate fair value</p>
                <Button>Build DCF Model</Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
