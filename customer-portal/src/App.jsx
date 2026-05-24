import { useMemo, useState } from "react";
import {
  AlertTriangle,
  ArrowRight,
  BadgeCheck,
  Building2,
  CheckCircle2,
  CreditCard,
  FileText,
  Headphones,
  Landmark,
  LockKeyhole,
  MessageSquareText,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  TimerReset,
  TrendingUp,
  UserRound
} from "lucide-react";

const customer = {
  name: "Maya Chen",
  segment: "Premier Banking",
  customerId: "DEMO-CUST-1048",
  relationship: "8 years",
  onboarding: "KYC verified, mobile banking active",
  accounts: "All services healthy",
  requests: 2,
  fraudStatus: "No confirmed fraud"
};

const transactions = [
  {
    id: "txn-1001",
    merchant: "Metro Grocery",
    date: "Today",
    amount: "-$84.20",
    channel: "Debit card",
    location: "New York, NY",
    riskSignals: 1
  },
  {
    id: "txn-1002",
    merchant: "Northstar Electronics",
    date: "Yesterday",
    amount: "-$1,248.99",
    channel: "Online card",
    location: "Austin, TX",
    riskSignals: 3
  },
  {
    id: "txn-1003",
    merchant: "Payroll Deposit",
    date: "May 22",
    amount: "+$4,820.00",
    channel: "ACH",
    location: "Employer",
    riskSignals: 0
  },
  {
    id: "txn-1004",
    merchant: "City Transit",
    date: "May 21",
    amount: "-$32.00",
    channel: "Mobile wallet",
    location: "New York, NY",
    riskSignals: 1
  },
  {
    id: "txn-1005",
    merchant: "Global Digital Market",
    date: "May 20",
    amount: "-$672.40",
    channel: "Online card",
    location: "International",
    riskSignals: 4
  }
];

const recentRequests = [
  { id: "SR-5821", title: "Debit card replacement", status: "In progress", sla: "1 business day" },
  { id: "SR-5794", title: "Address update review", status: "Waiting on bank", sla: "Today" }
];

const dashboardCards = [
  {
    label: "Onboarding",
    value: "98%",
    detail: "Profile verified",
    icon: BadgeCheck,
    tone: "text-bank-green bg-emerald-50"
  },
  {
    label: "Service Health",
    value: "Healthy",
    detail: "Accounts, cards, and app online",
    icon: ShieldCheck,
    tone: "text-bank-blue bg-blue-50"
  },
  {
    label: "Support",
    value: "2 open",
    detail: "No overdue requests",
    icon: Headphones,
    tone: "text-violet-700 bg-violet-50"
  },
  {
    label: "Fraud Alerts",
    value: "Clear",
    detail: "Monitoring active",
    icon: LockKeyhole,
    tone: "text-amber-700 bg-amber-50"
  }
];

const timeline = [
  {
    label: "Digital onboarding",
    detail: "Identity, KYC, and profile preferences confirmed",
    status: "Complete"
  },
  {
    label: "Service monitoring",
    detail: "Account health and support SLA checked daily",
    status: "Active"
  },
  {
    label: "Support triage",
    detail: "Customer issue routed by category and urgency",
    status: "Ready"
  },
  {
    label: "Fraud review",
    detail: "Suspicious transaction workflow available on demand",
    status: "Protected"
  }
];

const categoryDepartments = {
  "Card issue": "Card Services",
  "Account access": "Digital Banking Support",
  "Payments or transfers": "Payments Operations",
  "Loan or mortgage": "Lending Service Desk",
  "Fraud concern": "Fraud Operations"
};

function getSupportResponse(form) {
  const isFraud = form.category === "Fraud concern";
  const isHighUrgency = form.urgency === "High";
  const isMediumUrgency = form.urgency === "Medium";
  const mentionsLock = /lock|blocked|stolen|fraud|unauthorized|unknown/i.test(form.description);

  const priority = isFraud || isHighUrgency || mentionsLock ? "High" : isMediumUrgency ? "Medium" : "Standard";
  const sla = priority === "High" ? "Within 2 hours" : priority === "Medium" ? "Same business day" : "1-2 business days";
  const department = categoryDepartments[form.category] || "Customer Care";
  const guidance =
    priority === "High"
      ? "We would prioritize this request, protect impacted services, and ask the customer to avoid retrying the transaction until a specialist reviews it."
      : "We would collect the key details, keep the customer updated in the portal, and route the request to the correct service team.";

  return { priority, sla, department, guidance };
}

function getFraudResult(transaction) {
  const score = Math.min(96, 28 + transaction.riskSignals * 17);
  const riskLevel = score >= 80 ? "High" : score >= 55 ? "Medium" : "Low";
  const nextAction =
    riskLevel === "High"
      ? "Temporarily lock the card, open a fraud case, and contact the customer through verified channels."
      : riskLevel === "Medium"
        ? "Request customer confirmation and monitor related card activity for 24 hours."
        : "Keep monitoring. No service restriction is recommended for this demo transaction.";
  const safetyMessage =
    riskLevel === "High"
      ? "Do not share one-time passcodes or online banking credentials. Bank staff will never ask for your password."
      : "Review merchant details and report anything you do not recognize. Your account monitoring remains active.";

  return { score, riskLevel, nextAction, safetyMessage };
}

function App() {
  const [enteredPortal, setEnteredPortal] = useState(false);
  const [supportForm, setSupportForm] = useState({
    category: "Card issue",
    urgency: "Medium",
    description: ""
  });
  const [supportResponse, setSupportResponse] = useState(null);
  const [selectedTxnId, setSelectedTxnId] = useState(transactions[1].id);
  const [fraudResult, setFraudResult] = useState(null);

  const selectedTransaction = useMemo(
    () => transactions.find((transaction) => transaction.id === selectedTxnId),
    [selectedTxnId]
  );

  const handleSupportSubmit = (event) => {
    event.preventDefault();
    setSupportResponse(getSupportResponse(supportForm));
  };

  const handleFraudAnalysis = () => {
    setFraudResult(getFraudResult(selectedTransaction));
  };

  return (
    <div className="min-h-screen bg-slate-50 text-ink">
      <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/90 backdrop-blur">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-bank-blue text-white">
              <Landmark size={21} aria-hidden="true" />
            </span>
            <div>
              <p className="text-sm font-semibold leading-tight">BankAssist AI</p>
              <p className="text-xs text-slate-500">Customer Portal</p>
            </div>
          </div>
          <button
            type="button"
            onClick={() => setEnteredPortal(true)}
            className="inline-flex items-center gap-2 rounded-lg bg-ink px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-bank-cyan"
          >
            Enter demo
            <ArrowRight size={16} aria-hidden="true" />
          </button>
        </nav>
      </header>

      {!enteredPortal ? (
        <Landing onEnter={() => setEnteredPortal(true)} />
      ) : (
        <main className="mx-auto max-w-7xl px-5 py-8 sm:py-10">
          <PortalHeader />
          <Dashboard />
          <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_1fr]">
            <SupportRequest
              form={supportForm}
              setForm={setSupportForm}
              onSubmit={handleSupportSubmit}
              response={supportResponse}
            />
            <FraudReport
              selectedTxnId={selectedTxnId}
              setSelectedTxnId={setSelectedTxnId}
              onAnalyze={handleFraudAnalysis}
              result={fraudResult}
            />
          </div>
          <ServiceTimeline />
        </main>
      )}
    </div>
  );
}

function Landing({ onEnter }) {
  return (
    <main>
      <section className="relative overflow-hidden bg-[radial-gradient(circle_at_top_left,#E0F2FE_0,#F8FAFC_36%,#FFFFFF_68%)]">
        <div className="mx-auto grid max-w-7xl gap-10 px-5 py-16 sm:py-20 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
          <div>
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-200 bg-white px-3 py-1 text-sm font-medium text-bank-blue">
              <Sparkles size={16} aria-hidden="true" />
              Public static demo, mock banking data only
            </div>
            <h1 className="max-w-3xl text-4xl font-semibold tracking-normal text-ink sm:text-5xl lg:text-6xl">
              BankAssist AI Customer Portal
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600">
              A customer-facing retail banking self-service demo for digital onboarding, support triage,
              service recovery, and suspicious transaction reporting.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <button
                type="button"
                onClick={onEnter}
                className="inline-flex items-center justify-center gap-2 rounded-lg bg-bank-blue px-5 py-3 text-sm font-semibold text-white shadow-fintech transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-bank-cyan"
              >
                Enter demo portal
                <ArrowRight size={17} aria-hidden="true" />
              </button>
              <a
                href="#experience"
                className="inline-flex items-center justify-center rounded-lg border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-bank-blue hover:text-bank-blue"
              >
                View experience
              </a>
            </div>
          </div>

          <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-fintech">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div>
                <p className="text-sm font-semibold text-slate-900">Customer service snapshot</p>
                <p className="text-xs text-slate-500">Simulated AI-assisted guidance</p>
              </div>
              <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-bank-green">
                Online
              </span>
            </div>
            <div className="mt-5 grid gap-4 sm:grid-cols-2">
              {dashboardCards.map((card) => (
                <MetricCard key={card.label} {...card} />
              ))}
            </div>
            <div className="mt-5 rounded-lg bg-slate-900 p-5 text-white">
              <div className="flex items-start gap-3">
                <MessageSquareText className="mt-1 text-bank-cyan" size={22} aria-hidden="true" />
                <div>
                  <p className="font-semibold">AI-style support guidance</p>
                  <p className="mt-2 text-sm leading-6 text-slate-300">
                    Rule-based demo responses explain priority, SLA, routing, and safe next steps without
                    calling any external AI service.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="experience" className="mx-auto max-w-7xl px-5 py-12">
        <div className="grid gap-5 md:grid-cols-3">
          <Feature icon={UserRound} title="Customer profile" text="A demo customer view with onboarding, account health, support, and fraud alert context." />
          <Feature icon={Headphones} title="Self-service support" text="Customers can raise a mock support request and receive instant rule-based guidance." />
          <Feature icon={ShieldAlert} title="Fraud reporting" text="Customers can select a recent transaction and simulate fraud risk analysis." />
        </div>
      </section>
    </main>
  );
}

function PortalHeader() {
  return (
    <section className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p className="text-sm font-semibold uppercase tracking-wide text-bank-blue">Demo customer workspace</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-normal text-ink sm:text-4xl">
          Welcome back, {customer.name}
        </h1>
        <p className="mt-3 max-w-3xl text-slate-600">
          Review service health, manage support requests, and report suspicious activity using mock data.
        </p>
      </div>
      <div className="rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm shadow-sm">
        <p className="font-semibold text-slate-900">{customer.segment}</p>
        <p className="text-slate-500">{customer.customerId}</p>
      </div>
    </section>
  );
}

function Dashboard() {
  return (
    <section className="mt-8 grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
      <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="flex h-11 w-11 items-center justify-center rounded-lg bg-blue-50 text-bank-blue">
            <UserRound size={22} aria-hidden="true" />
          </span>
          <div>
            <h2 className="text-lg font-semibold">Demo customer profile</h2>
            <p className="text-sm text-slate-500">Synthetic profile for product demonstration</p>
          </div>
        </div>
        <dl className="mt-5 grid gap-4 text-sm">
          <ProfileRow label="Relationship" value={customer.relationship} />
          <ProfileRow label="Onboarding status" value={customer.onboarding} />
          <ProfileRow label="Account health" value={customer.accounts} />
          <ProfileRow label="Fraud alert status" value={customer.fraudStatus} />
        </dl>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {dashboardCards.map((card) => (
          <MetricCard key={card.label} {...card} />
        ))}
      </div>

      <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm xl:col-span-2">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <h2 className="text-lg font-semibold">Open support requests</h2>
            <p className="text-sm text-slate-500">Current mock service cases</p>
          </div>
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
            {customer.requests} open
          </span>
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          {recentRequests.map((request) => (
            <div key={request.id} className="rounded-lg border border-slate-200 p-4">
              <div className="flex items-center justify-between gap-3">
                <p className="font-semibold">{request.title}</p>
                <span className="text-xs font-semibold text-bank-blue">{request.id}</span>
              </div>
              <p className="mt-2 text-sm text-slate-600">{request.status}</p>
              <p className="mt-3 inline-flex items-center gap-2 text-sm text-slate-500">
                <TimerReset size={16} aria-hidden="true" />
                SLA: {request.sla}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function SupportRequest({ form, setForm, onSubmit, response }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-violet-50 text-violet-700">
          <Headphones size={21} aria-hidden="true" />
        </span>
        <div>
          <h2 className="text-lg font-semibold">Raise support request</h2>
          <p className="text-sm text-slate-500">Rule-based triage simulation</p>
        </div>
      </div>

      <form className="mt-5 grid gap-4" onSubmit={onSubmit}>
        <label className="grid gap-2 text-sm font-medium text-slate-700">
          Issue category
          <select
            value={form.category}
            onChange={(event) => setForm({ ...form, category: event.target.value })}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 outline-none focus:border-bank-blue focus:ring-2 focus:ring-blue-100"
          >
            {Object.keys(categoryDepartments).map((category) => (
              <option key={category}>{category}</option>
            ))}
          </select>
        </label>

        <label className="grid gap-2 text-sm font-medium text-slate-700">
          Urgency
          <select
            value={form.urgency}
            onChange={(event) => setForm({ ...form, urgency: event.target.value })}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 outline-none focus:border-bank-blue focus:ring-2 focus:ring-blue-100"
          >
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
          </select>
        </label>

        <label className="grid gap-2 text-sm font-medium text-slate-700">
          Description
          <textarea
            value={form.description}
            onChange={(event) => setForm({ ...form, description: event.target.value })}
            rows="4"
            placeholder="Describe the issue using demo details only."
            className="resize-none rounded-lg border border-slate-300 px-3 py-2 text-slate-900 outline-none focus:border-bank-blue focus:ring-2 focus:ring-blue-100"
          />
        </label>

        <button
          type="submit"
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-bank-blue px-4 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-bank-cyan"
        >
          Submit request
          <FileText size={17} aria-hidden="true" />
        </button>
      </form>

      {response && (
        <ResultPanel
          title="Simulated support response"
          rows={[
            ["Priority", response.priority],
            ["Estimated SLA", response.sla],
            ["Recommended department", response.department],
            ["Customer guidance", response.guidance]
          ]}
        />
      )}
    </section>
  );
}

function FraudReport({ selectedTxnId, setSelectedTxnId, onAnalyze, result }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700">
          <ShieldAlert size={21} aria-hidden="true" />
        </span>
        <div>
          <h2 className="text-lg font-semibold">Report suspicious transaction</h2>
          <p className="text-sm text-slate-500">Mock fraud risk scoring</p>
        </div>
      </div>

      <div className="mt-5 grid gap-3">
        {transactions.map((transaction) => (
          <label
            key={transaction.id}
            className={`flex cursor-pointer items-center justify-between gap-3 rounded-lg border p-4 transition ${
              selectedTxnId === transaction.id
                ? "border-bank-blue bg-blue-50"
                : "border-slate-200 bg-white hover:border-slate-300"
            }`}
          >
            <span className="flex min-w-0 items-center gap-3">
              <input
                type="radio"
                name="transaction"
                value={transaction.id}
                checked={selectedTxnId === transaction.id}
                onChange={(event) => setSelectedTxnId(event.target.value)}
                className="h-4 w-4 accent-bank-blue"
              />
              <span className="min-w-0">
                <span className="block truncate text-sm font-semibold text-slate-900">{transaction.merchant}</span>
                <span className="block text-xs text-slate-500">
                  {transaction.date} · {transaction.channel} · {transaction.location}
                </span>
              </span>
            </span>
            <span className="shrink-0 text-sm font-semibold">{transaction.amount}</span>
          </label>
        ))}
      </div>

      <button
        type="button"
        onClick={onAnalyze}
        className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-bank-cyan"
      >
        Analyze Fraud Risk
        <AlertTriangle size={17} aria-hidden="true" />
      </button>

      {result && (
        <ResultPanel
          title="Simulated fraud analysis"
          rows={[
            ["Risk level", result.riskLevel],
            ["Fraud score", `${result.score}/100`],
            ["Recommended next action", result.nextAction],
            ["Customer safety message", result.safetyMessage]
          ]}
        />
      )}
    </section>
  );
}

function ServiceTimeline() {
  return (
    <section className="mt-8 rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-cyan-50 text-cyan-700">
          <TrendingUp size={21} aria-hidden="true" />
        </span>
        <div>
          <h2 className="text-lg font-semibold">Service status timeline</h2>
          <p className="text-sm text-slate-500">Onboarding, support, and fraud workflow steps</p>
        </div>
      </div>

      <ol className="mt-6 grid gap-4 lg:grid-cols-4">
        {timeline.map((step, index) => (
          <li key={step.label} className="relative rounded-lg border border-slate-200 p-4">
            <div className="flex items-center gap-3">
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-bank-blue text-sm font-semibold text-white">
                {index + 1}
              </span>
              <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-bank-green">
                {step.status}
              </span>
            </div>
            <h3 className="mt-4 font-semibold">{step.label}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-600">{step.detail}</p>
          </li>
        ))}
      </ol>
    </section>
  );
}

function MetricCard({ label, value, detail, icon: Icon, tone }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-500">{label}</p>
          <p className="mt-2 text-2xl font-semibold text-slate-900">{value}</p>
          <p className="mt-1 text-sm text-slate-600">{detail}</p>
        </div>
        <span className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${tone}`}>
          <Icon size={21} aria-hidden="true" />
        </span>
      </div>
    </div>
  );
}

function Feature({ icon: Icon, title, text }) {
  return (
    <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <span className="flex h-11 w-11 items-center justify-center rounded-lg bg-slate-100 text-bank-blue">
        <Icon size={22} aria-hidden="true" />
      </span>
      <h2 className="mt-4 text-lg font-semibold">{title}</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600">{text}</p>
    </article>
  );
}

function ProfileRow({ label, value }) {
  return (
    <div className="flex items-start justify-between gap-4 border-b border-slate-100 pb-3 last:border-0 last:pb-0">
      <dt className="text-slate-500">{label}</dt>
      <dd className="text-right font-semibold text-slate-900">{value}</dd>
    </div>
  );
}

function ResultPanel({ title, rows }) {
  return (
    <div className="mt-5 rounded-lg border border-slate-200 bg-slate-50 p-4">
      <div className="mb-3 flex items-center gap-2">
        <CheckCircle2 size={18} className="text-bank-green" aria-hidden="true" />
        <h3 className="font-semibold">{title}</h3>
      </div>
      <dl className="grid gap-3">
        {rows.map(([label, value]) => (
          <div key={label} className="rounded-lg bg-white p-3">
            <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</dt>
            <dd className="mt-1 text-sm leading-6 text-slate-800">{value}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}

export default App;
