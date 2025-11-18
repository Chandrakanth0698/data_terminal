'use client'

import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { researchAPI } from '@/lib/api'
import { formatDate } from '@/lib/utils'
import { FileText, Plus } from 'lucide-react'
import Link from 'next/link'

export default function ResearchPage() {
  const { data: notes, isLoading } = useQuery({
    queryKey: ['research-notes'],
    queryFn: async () => {
      const response = await researchAPI.list()
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
          <h1 className="text-3xl font-bold">Research Notes</h1>
          <p className="text-muted-foreground">Document your investment thesis and analysis</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Note
        </Button>
      </div>

      {notes && notes.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2">
          {notes.map((note: any) => (
            <Card key={note.id} className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="line-clamp-1">{note.title}</CardTitle>
                    <CardDescription className="mt-1">
                      Updated {formatDate(note.updated_at)}
                    </CardDescription>
                  </div>
                  {note.thesis_type && (
                    <Badge variant={note.thesis_type === 'Bull' ? 'success' : note.thesis_type === 'Bear' ? 'destructive' : 'secondary'}>
                      {note.thesis_type}
                    </Badge>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                {note.content && (
                  <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
                    {note.content}
                  </p>
                )}
                <div className="flex items-center gap-2">
                  {note.investment_horizon && (
                    <Badge variant="outline" className="text-xs">
                      {note.investment_horizon}
                    </Badge>
                  )}
                  {note.confidence_level && (
                    <Badge variant="outline" className="text-xs">
                      Confidence: {note.confidence_level}/5
                    </Badge>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card className="py-12">
          <CardContent className="text-center">
            <FileText className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No Research Notes</h3>
            <p className="text-muted-foreground mb-4">Start documenting your investment research</p>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Create Note
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
