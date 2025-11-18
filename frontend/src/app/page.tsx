import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { TrendingUp, Search, Calculator, Briefcase, Bell, FileText, BarChart3, Shield } from 'lucide-react'

export default function Home() {
  const features = [
    {
      icon: Search,
      title: "Stock Screener",
      description: "Filter 1000s of stocks with 50+ criteria including valuation, profitability, and growth metrics"
    },
    {
      icon: BarChart3,
      title: "Financial Analysis",
      description: "10+ years of financial statements, 40+ calculated ratios, and peer comparison"
    },
    {
      icon: Calculator,
      title: "DCF Valuation",
      description: "Build detailed DCF models with customizable assumptions and sensitivity analysis"
    },
    {
      icon: Briefcase,
      title: "Portfolio Tracking",
      description: "Track multiple portfolios with XIRR calculations and performance metrics"
    },
    {
      icon: FileText,
      title: "Research Notes",
      description: "Document your research with SWOT analysis and investment thesis tracking"
    },
    {
      icon: Bell,
      title: "Smart Alerts",
      description: "Price alerts, ratio thresholds, earnings reminders, and news notifications"
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-800">
      {/* Hero Section */}
      <div className="container mx-auto px-4 pt-20 pb-16">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Professional Stock Analysis for Indian Markets
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            Comprehensive fundamental analysis platform for NSE/BSE stocks.
            Implement Richard Coffin's 6-step analysis framework with institutional-grade tools.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" className="text-lg px-8">
                Get Started Free
              </Button>
            </Link>
            <Link href="/login">
              <Button size="lg" variant="outline" className="text-lg px-8">
                Sign In
              </Button>
            </Link>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-16 max-w-5xl mx-auto">
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-600">50+</div>
            <div className="text-sm text-muted-foreground">Screening Filters</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-600">40+</div>
            <div className="text-sm text-muted-foreground">Financial Ratios</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-600">10+</div>
            <div className="text-sm text-muted-foreground">Years of Data</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-600">100%</div>
            <div className="text-sm text-muted-foreground">Free Data Sources</div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Everything You Need for Stock Analysis</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {features.map((feature, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <feature.icon className="w-12 h-12 text-blue-600 mb-4" />
                <CardTitle>{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Use Cases */}
      <div className="bg-blue-600 text-white py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Perfect For</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="text-center">
              <TrendingUp className="w-16 h-16 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Individual Investors</h3>
              <p className="text-blue-100">Make informed decisions with professional-grade analysis tools</p>
            </div>
            <div className="text-center">
              <Shield className="w-16 h-16 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Value Investors</h3>
              <p className="text-blue-100">Find undervalued gems using Graham & Buffett principles</p>
            </div>
            <div className="text-center">
              <BarChart3 className="w-16 h-16 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Research Analysts</h3>
              <p className="text-blue-100">Comprehensive data and tools for deep fundamental research</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-3xl font-bold mb-4">Ready to Start Analyzing?</h2>
        <p className="text-xl text-muted-foreground mb-8">Join thousands of investors making smarter decisions</p>
        <Link href="/register">
          <Button size="lg" className="text-lg px-12">
            Create Free Account
          </Button>
        </Link>
      </div>

      {/* Footer */}
      <footer className="border-t mt-16 py-8">
        <div className="container mx-auto px-4 text-center text-muted-foreground">
          <p>© 2024 Stock Analysis Platform. All rights reserved.</p>
          <p className="text-sm mt-2">Data from NSE, BSE, Yahoo Finance, and other free sources</p>
        </div>
      </footer>
    </div>
  )
}
