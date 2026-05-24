# BankAssist AI Customer Portal

Customer-facing static frontend demo for a retail banking self-service experience. It complements the internal Streamlit operations dashboard in the parent repository by showing the customer experience side of digital banking support.

## What It Demonstrates

- Modern fintech-style landing page for a public demo experience.
- Demo customer dashboard with synthetic profile, onboarding status, account health, support requests, recent transactions, and fraud alert status.
- Rule-based support request triage that returns priority, estimated SLA, recommended department, and customer-friendly guidance.
- Suspicious transaction reporting with mock fraud risk scoring, next action, and safety messaging.
- Service status timeline covering onboarding, support, and fraud workflows.

## Important Demo Notes

- Static frontend only.
- No backend.
- No real authentication.
- No real customer data.
- No OpenAI API required.
- All data and AI-style responses are mock or rule-based simulations.

## Tech Stack

- React
- Vite
- Tailwind CSS
- lucide-react icons

## Local Development

Install dependencies:

```bash
npm install
```

Run the local development server:

```bash
npm run dev
```

Build for production:

```bash
npm run build
```

Preview the production build locally:

```bash
npm run preview
```

## Vercel Deployment

Deploy the `customer-portal/` folder as a standalone Vercel project.

Recommended Vercel settings:

- Framework preset: Vite
- Root directory: `customer-portal`
- Build command: `npm run build`
- Output directory: `dist`

This portal is designed to be hosted for free on Vercel as a static customer experience demo.
