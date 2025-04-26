# AI-Augmented Tax Engagement Frontend

This is the frontend for the AI-Augmented Tax Engagement prototype application. It's built with React, TypeScript, and Vite, and uses Tailwind CSS for styling.

## Setup

### Prerequisites

- Node.js (v14 or newer)
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```
   cd frontend
   ```
3. Install dependencies:
   ```
   npm install
   ```
   or
   ```
   yarn
   ```

### Environment Variables

Copy the `.env.local` file to create a local environment:

```
cp .env.local .env
```

Update the variables as needed:

- `VITE_API_URL`: URL of the backend API (default: http://localhost:8000)

## Development

Start the development server:

```
npm run dev
```

or

```
yarn dev
```

This will start the Vite development server on port 3000.

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── api/             # API clients
│   │   ├── auth.ts      # Authentication API
│   │   ├── projects.ts  # Projects API
│   │   ├── tasks.ts     # Tasks API
│   │   ├── chat.ts      # Chat API
│   │   ├── actions.ts   # Actions API
│   ├── components/      # Reusable components
│   │   ├── ChatWidget.tsx       # AI chat interface
│   │   ├── ActionButtons.tsx    # Action execution buttons
│   ├── context/         # React contexts
│   │   ├── AuthContext.tsx      # Authentication context
│   ├── pages/           # Page components
│   │   ├── LoginPage.tsx        # User login
│   │   ├── ProjectsPage.tsx     # Project list
│   │   ├── TasksPage.tsx        # Task list
│   │   ├── TaskDetailPage.tsx   # Task details with chat
│   ├── utils/           # Utility functions
│   │   ├── session.ts           # Session management
│   ├── App.tsx          # Main app component
│   ├── main.tsx         # Entry point
│   ├── index.css        # Global styles
├── .env                 # Environment variables
├── .env.local           # Local environment overrides
├── package.json         # Dependencies and scripts
├── vite.config.ts       # Vite configuration
├── tailwind.config.js   # Tailwind CSS configuration
├── postcss.config.js    # PostCSS configuration
├── tsconfig.json        # TypeScript configuration
```

## Features

- **Authentication**: User switching between Jeff (Preparer) and Hanna (Reviewer)
- **Project Management**: View and select projects
- **Task Management**: View tasks assigned to the current user
- **Task Details**: View task details, associated documents, and due dates
- **AI Assistant**: Chat with an AI assistant for tax-related questions
- **Action Execution**: Execute AI-suggested actions like generating missing info letters

## Users

The application has two hardcoded users:

1. **Jeff (Preparer)**
   - Username: `jeff`
   - Password: `password`
   - Role: Preparer

2. **Hanna (Reviewer)**
   - Username: `hanna`
   - Password: `password`
   - Role: Reviewer

## API Integration

The frontend communicates with the backend API through several client modules:

- `auth.ts`: User authentication and session management
- `projects.ts`: Fetch project data
- `tasks.ts`: Fetch task data filtered by user and project
- `chat.ts`: Send messages to the AI assistant and receive responses
- `actions.ts`: Execute AI-suggested actions

## Building for Production

```
npm run build
```

or

```
yarn build
```

This will generate optimized production files in the `dist` directory.
