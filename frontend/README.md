# Stock Analysis Platform - Frontend

Modern, responsive frontend built with Next.js 14, React 18, TypeScript, and TailwindCSS.

## Tech Stack

- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type safety
- **TailwindCSS** - Utility-first CSS
- **shadcn/ui** - Beautiful component library
- **TanStack Query** - Data fetching and caching
- **Zustand** - State management
- **Recharts** - Data visualization
- **Axios** - HTTP client

## Features

### Pages

- **Landing Page** - Marketing page with feature showcase
- **Authentication** - Login and Registration
- **Dashboard** - Overview with quick stats and actions
- **Stock Screener** - Filter stocks with 50+ criteria
- **Companies** - Search and analyze companies
- **Company Details** - Comprehensive analysis with tabs:
  - Overview
  - Financial Ratios
  - Charts
  - Peer Comparison
  - Valuation
- **Portfolio** - Track multiple portfolios
- **Research Notes** - Document investment thesis
- **Watchlist** - Monitor stocks
- **Alerts** - Price and ratio alerts
- **Valuation** - DCF calculator
- **Settings** - User preferences

### Components

- Reusable UI components from shadcn/ui
- Custom components for financial data display
- Charts and visualizations
- Responsive layout with sidebar navigation

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local

# Edit .env.local with your API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── page.tsx      # Landing page
│   │   ├── login/        # Authentication
│   │   ├── register/
│   │   └── dashboard/    # Main app
│   │       ├── page.tsx  # Dashboard
│   │       ├── screener/
│   │       ├── companies/
│   │       ├── portfolio/
│   │       ├── research/
│   │       ├── alerts/
│   │       ├── watchlist/
│   │       ├── valuation/
│   │       └── settings/
│   ├── components/
│   │   ├── ui/           # shadcn/ui components
│   │   └── layout/       # Layout components
│   ├── lib/
│   │   ├── api.ts        # API client
│   │   └── utils.ts      # Utilities
│   └── store/
│       └── authStore.ts  # Zustand store
├── public/               # Static files
└── package.json
```

## API Integration

The frontend communicates with the FastAPI backend via REST API:

```typescript
// Example API call
import { companiesAPI } from '@/lib/api'

const { data } = await companiesAPI.getCompany('RELIANCE')
```

All API calls are typed and use TanStack Query for caching and state management.

## Styling

- **TailwindCSS** for utility classes
- **CSS Variables** for theming
- **Dark Mode** support built-in
- **Responsive Design** mobile-first approach

## State Management

- **Zustand** for global state (auth)
- **TanStack Query** for server state
- **React Context** for theme

## Development

### Code Style

- TypeScript for type safety
- ESLint for linting
- Prettier for formatting

### Adding New Pages

1. Create page in `src/app/dashboard/yourpage/page.tsx`
2. Add route to sidebar in `src/components/layout/Sidebar.tsx`
3. Create API functions in `src/lib/api.ts` if needed
4. Use TanStack Query for data fetching

### Adding UI Components

We use shadcn/ui components. To add a new component:

```bash
npx shadcn-ui@latest add [component-name]
```

## Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend API URL
```

## Docker

Development:
```bash
docker-compose up frontend
```

Production:
```bash
docker build -f Dockerfile -t stockanalysis-frontend .
docker run -p 3000:3000 stockanalysis-frontend
```

## License

MIT
