# AI Tax Prototype - Frontend

The React frontend for the AI-Augmented Tax Engagement Prototype, built with Vite.

## Setup

### Prerequisites

- Node.js 14+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install
# or
yarn
```

### Environment Setup

1. Copy `../shared/environment/frontend.env` to `.env.local`
2. Update values if needed

### Development Server

```bash
npm run dev
# or
yarn dev
```

The development server will be available at http://localhost:5173

### Building for Production

```bash
npm run build
# or
yarn build
```

## Features

- User switching between Jeff (Preparer) and Hanna (Reviewer)
- Project list view
- Task list filtered by current user
- Task details with embedded AI chat
- Document viewing
- Action buttons triggered from AI suggestions
