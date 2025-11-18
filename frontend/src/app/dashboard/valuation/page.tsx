'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Calculator, Plus } from 'lucide-react'

export default function ValuationPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">DCF Valuation</h1>
          <p className="text-muted-foreground">Build discounted cash flow models</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Model
        </Button>
      </div>

      <Card className="py-12">
        <CardContent className="text-center">
          <Calculator className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold mb-2">No DCF Models</h3>
          <p className="text-muted-foreground mb-4">Create valuation models to estimate fair value</p>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Create Model
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
