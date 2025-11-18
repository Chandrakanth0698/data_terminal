'use client'

import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { alertsAPI } from '@/lib/api'
import { formatDate, formatNumber } from '@/lib/utils'
import { Bell, Plus, Trash2 } from 'lucide-react'

export default function AlertsPage() {
  const { data: alerts, isLoading } = useQuery({
    queryKey: ['alerts'],
    queryFn: async () => {
      const response = await alertsAPI.list(true)
      return response.data
    },
  })

  if (isLoading) {
    return <div className="flex items-center justify-center h-96">Loading...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Alerts</h1>
          <p className="text-muted-foreground">Manage your stock alerts and notifications</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Alert
        </Button>
      </div>

      {alerts && alerts.length > 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>Active Alerts ({alerts.length})</CardTitle>
            <CardDescription>You'll be notified when these conditions are met</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Title</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Condition</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {alerts.map((alert: any) => (
                  <TableRow key={alert.id}>
                    <TableCell className="font-medium">{alert.title}</TableCell>
                    <TableCell>
                      <Badge variant="outline">{alert.alert_type}</Badge>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {alert.condition_field && alert.condition_operator && alert.condition_value &&
                        `${alert.condition_field} ${alert.condition_operator} ${formatNumber(alert.condition_value)}`
                      }
                    </TableCell>
                    <TableCell>
                      <Badge variant={alert.is_triggered ? 'success' : 'secondary'}>
                        {alert.is_triggered ? 'Triggered' : 'Active'}
                      </Badge>
                    </TableCell>
                    <TableCell>{formatDate(alert.created_at)}</TableCell>
                    <TableCell>
                      <Button variant="ghost" size="sm">
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      ) : (
        <Card className="py-12">
          <CardContent className="text-center">
            <Bell className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No Active Alerts</h3>
            <p className="text-muted-foreground mb-4">Create alerts to get notified about stock movements</p>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Create Alert
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
