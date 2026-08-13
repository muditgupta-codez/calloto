# Calloto — Marketing Website Design

## Overview
The marketing website is the primary conversion engine. It must communicate the value proposition in <10 seconds, prove ROI instantly, and get businesses from landing to paid signup in <5 minutes.

**Primary goal:** Convert UK tradespeople to £19/month paid subscribers  
**Secondary goal:** Educate on call forwarding setup (reduce support burden)

---

## Information Architecture

### Pages
1. **Landing Page** (`/`) — Problem → Solution → Proof → CTA
2. **Signup** (`/signup`) — Account creation + payment
3. **Onboarding** (`/onboarding`) — 5-minute setup wizard
4. **Login** (`/login`) — Customer dashboard access
5. **Pricing** (`/pricing`) — Detailed pricing (can be section on landing)
6. **FAQ** (`/faq`) — Common questions (can be section on landing)

### Landing Page Sections (Top to Bottom)
1. **Hero** — Headline + subhead + CTA + live missed-call counter
2. **Problem** — "You're losing £X per month to missed calls"
3. **Solution** — How Calloto works (3-step visual)
4. **ROI Calculator** — Interactive: input missed calls → see £ recovered
5. **Social Proof** — Testimonials (once we have them), trust badges
6. **Features** — What you get (dashboard, WhatsApp, booking link)
7. **How It Works** — Call forwarding setup (iPhone/Android)
8. **Pricing** — £19/month, what's included, overage
9. **FAQ** — Common objections
10. **Final CTA** — "Start recovering missed calls in 5 minutes"

---

## Design Direction

### Visual Style
- **Tone:** Professional but approachable, not corporate. Tradespeople trust "built for you" over "enterprise solution"
- **Colors:**
  - Primary: `#2563EB` (blue-600) — trust, reliability
  - Accent: `#10B981` (emerald-500) — money, ROI, success
  - Background: `#F9FAFB` (gray-50) — clean, not sterile
  - Text: `#111827` (gray-900) — high contrast, readable
- **Typography:**
  - Headings: Inter Bold (or system font stack)
  - Body: Inter Regular (or system font stack)
  - Monospace: JetBrains Mono (for numbers/stats)
- **Imagery:**
  - Hero: Phone mockup showing missed call → text-back → booking (animated)
  - Features: Screenshots of dashboard (blurred sample data)
  - Icons: Simple line icons (Heroicons or similar)
  - No stock photos of "business people shaking hands" — keep it product-focused

### Mobile-First
- 80%+ of tradespeople will view on phone (they're on the job, not at a desk)
- All CTAs must be thumb-friendly (min 44px tap target)
- ROI calculator must work on mobile (no hover states)
- Call forwarding instructions must be mobile-optimized (they'll set it up on their phone)

---

## Section-by-Section Design

### 1. Hero Section
**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  [Logo]                                    [Login]      │
│                                                         │
│  Turn missed calls into booked jobs                     │
│                                                         │
│  When you can't answer, Calloto instantly texts your    │
│  caller back with a booking link. £19/month.            │
│                                                         │
│  [Start 5-minute setup →]                               │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  [Phone mockup animation]                       │   │
│  │                                                 │   │
│  │  Incoming call: 07700 900123                    │   │
│  │  ↓                                              │   │
│  │  Text sent: "Hi! ABC Plumbing missed your       │   │
│  │  call. Rough price £80-150. Book here: [link]"  │   │
│  │  ↓                                              │   │
│  │  Booking confirmed: Tomorrow 2pm                │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  🟢 247 missed calls recovered this week                │
└─────────────────────────────────────────────────────────┘
```

**Copy:**
- Headline: "Turn missed calls into booked jobs"
- Subhead: "When you can't answer, Calloto instantly texts your caller back with a booking link. £19/month."
- CTA: "Start 5-minute setup →"
- Social proof: "🟢 247 missed calls recovered this week" (live counter, starts at seed number)

**Animation:** Phone mockup shows incoming call → text-back → booking confirmation (3-second loop)

### 2. Problem Section
**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  You're losing money every time your phone rings        │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │     27%      │  │     85%      │  │   £200-500   │ │
│  │              │  │              │  │              │ │
│  │ of calls go  │  │ of callers   │  │ lost per     │ │
│  │ unanswered   │  │ never call   │  │ missed call  │ │
│  │              │  │ back         │  │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
│  If you miss 10 calls a week, that's £8,000-20,000/yr   │
│  in lost jobs.                                          │
└─────────────────────────────────────────────────────────┘
```

**Copy:**
- Headline: "You're losing money every time your phone rings"
- Stats:
  - 27% of calls go unanswered (industry average)
  - 85% of callers never call back — they call the next business
  - £200-500 lost per missed call (typical job value)
- Bottom line: "If you miss 10 calls a week, that's £8,000-20,000/yr in lost jobs."

### 3. Solution Section
**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  Calloto texts them back. Instantly.                    │
│                                                         │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐       │
│  │   1     │  →   │   2     │  →   │   3     │       │
│  │         │      │         │      │         │       │
│  │ Caller  │      │ Calloto │      │ Caller  │       │
│  │ calls   │      │ texts   │      │ books   │       │
│  │ you     │      │ them    │      │ online  │       │
│  │         │      │ back    │      │         │       │
│  └─────────┘      └─────────┘      └─────────┘       │
│                                                         │
│  Your caller gets a text in 5 seconds with your name,   │
│  price range, and a booking link. They book instead of  │
│  calling the next plumber.                              │
└─────────────────────────────────────────────────────────┘
```

**Copy:**
- Headline: "Calloto texts them back. Instantly."
- 3 steps:
  1. Caller calls you (you're busy, can't answer)
  2. Calloto texts them back in 5 seconds
  3. Caller books online instead of calling the next business
- Bottom line: "Your caller gets a text in 5 seconds with your name, price range, and a booking link. They book instead of calling the next plumber."

### 4. ROI Calculator
**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  See how much you'll recover                            │
│                                                         │
│  How many calls do you miss per week?                   │
│  [──────●────────────────] 10                           │
│                                                         │
│  What's your average job value?                         │
│  [──────────●──────────] £200                           │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  You miss:          10 calls/week               │   │
│  │  Recovery rate:     30% (conservative)          │   │
│  │  Jobs recovered:    3/week = 12/month           │   │
│  │  £ recovered:       £2,400/month                │   │
│  │                                                 │   │
│  │  Calloto cost:      £19/month                   │   │
│  │  Your ROI:          126x                        │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  [Start recovering missed calls →]                      │
└─────────────────────────────────────────────────────────┘
```

**Interactive elements:**
- Slider: "How many calls do you miss per week?" (1-50, default 10)
- Slider: "What's your average job value?" (£50-£1000, default £200)
- Live calculation:
  - Recovery rate: 30% (conservative, based on industry data)
  - Jobs recovered: (missed calls × 0.3 × 4.3 weeks)
  - £ recovered: jobs × avg job value
  - ROI: £ recovered / £19
- CTA: "Start recovering missed calls →"

**Mobile:** Sliders must be thumb-friendly, calculation updates in real-time

### 5. Social Proof
**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  Trusted by UK tradespeople                             │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  "I recovered 3 jobs in the first week. Paid    │   │
│  │  for 6 months of Calloto."                      │   │
│  │                                                 │   │
│  │  — Dave, plumber, Manchester                    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  "Set it up in 5 minutes. Got a booking the     │   │
│  │  same day."                                     │   │
│  │                                                 │   │
│  │  — Sarah, electrician, Birmingham               │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  🟢 500+ missed calls recovered this month              │
└─────────────────────────────────────────────────────────┘
```

**Copy:**
- Headline: "Trusted by UK tradespeople"
- Testimonials: 2-3 quotes (once we have real customers, use real quotes)
- Live counter: "🟢 500+ missed calls recovered this month"

**Note:** For validation stage, use placeholder testimonials or remove this section until we have real customers.

### 6. Features Section
**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  Everything you need to recover missed calls            │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  📱          │  │  💬          │  │  📅          │ │
│  │              │  │              │  │              │ │
│  │  Instant     │  │  WhatsApp    │  │  Booking     │ │
│  │  text-back   │  │  or SMS      │  │  link        │ │
│  │              │  │              │  │              │ │
│  │  Caller gets │  │  We text via │  │  Caller taps │ │
│  │  a text in   │  │  WhatsApp or │  │  link, picks │ │
│  │  5 seconds   │  │  SMS         │  │  time, done  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  📊          │  │  💷          │  │  🛡️          │ │
│  │              │  │              │  │              │ │
│  │  ROI         │  │  £19/month   │  │  No app      │ │
│  │  dashboard   │  │  flat        │  │  required    │ │
│  │              │  │              │  │              │ │
│  │  See every   │  │  100 texts   │  │  Works with  │ │
│  │  call, text, │  │  included,   │  │  your existing│ │
│  │  booking     │  │  5p/ea after │  │  number      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Copy:**
- Headline: "Everything you need to recover missed calls"
- Features:
  1. **Instant text-back** — Caller gets a text in 5 seconds
  2. **WhatsApp or SMS** — We text via WhatsApp or SMS (your choice)
  3. **Booking link** — Caller taps link, picks time, done
  4. **ROI dashboard** — See every call, text, booking, £ recovered
  5. **£19/month flat** — 100 texts included, 5p each after
  6. **No app required** — Works with your existing number

### 7. How It Works (Call Forwarding)
**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  Set up call forwarding in 2 minutes                    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  iPhone                                         │   │
│  │                                                 │   │
│  │  1. Settings → Phone → Call Forwarding          │   │
│  │  2. Forward when unanswered → enter your        │   │
│  │     Calloto number                              │   │
│  │  3. Done                                        │   │
│  │                                                 │   │
│  │  [Show me →]                                    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Android                                        │   │
│  │                                                 │   │
│  │  1. Phone app → Menu → Settings → Call          │   │
│  │     forwarding                                   │   │
│  │  2. Forward when unanswered → enter your        │   │
│  │     Calloto number                              │   │
│  │  3. Done                                        │   │
│  │                                                 │   │
│  │  [Show me →]                                    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Or dial: **61*<your-calloto-number>#                   │
└─────────────────────────────────────────────────────────┘
```

**Copy:**
- Headline: "Set up call forwarding in 2 minutes"
- iPhone instructions (with screenshots)
- Android instructions (with screenshots)
- Dial code shortcut: `**61*<your-calloto-number>#`
- CTA: "Show me →" (opens modal with detailed screenshots)

**Mobile:** This section is critical — users will set up forwarding on their phone while reading this page

### 8. Pricing Section
**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  Simple, transparent pricing                            │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  £19/month                                      │   │
│  │                                                 │   │
│  │  ✅ Unlimited missed calls                      │   │
│  │  ✅ 100 text-backs included                     │   │
│  │  ✅ WhatsApp or SMS                             │   │
│  │  ✅ ROI dashboard                               │   │
│  │  ✅ Booking link                                │   │
│  │  ✅ No contracts, cancel anytime                │   │
│  │                                                 │   │
│  │  Overage: 5p per text after 100                 │   │
│  │                                                 │   │
│  │  [Start 5-minute setup →]                       │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Annual: £190/year (2 months free)                      │
└─────────────────────────────────────────────────────────┘
```

**Copy:**
- Headline: "Simple, transparent pricing"
- Price: £19/month
- Includes:
  - Unlimited missed calls
  - 100 text-backs included
  - WhatsApp or SMS
  - ROI dashboard
  - Booking link
  - No contracts, cancel anytime
- Overage: 5p per text after 100
- Annual: £190/year (2 months free)
- CTA: "Start 5-minute setup →"

### 9. FAQ Section
**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  Common questions                                       │
│                                                         │
│  ▼ Do I need a new phone number?                        │
│    No. Keep your existing number. Calloto gives you a   │
│    UK number to forward unanswered calls to.            │
│                                                         │
│  ▼ What if the caller doesn't have WhatsApp?            │
│    We'll send an SMS instead. You choose the default.   │
│                                                         │
│  ▼ Can I customize the text-back message?               │
│    Yes. Use your business name, price range, booking    │
│    link. We provide a template, you customize.          │
│                                                         │
│  ▼ What about withheld/private numbers?                 │
│    We can't text withheld numbers. They'll show as      │
│    "not texted" in your dashboard.                      │
│                                                         │
│  ▼ How do I set up call forwarding?                     │
│    2 minutes on iPhone or Android. We walk you through  │
│    it during signup.                                    │
│                                                         │
│  ▼ Can I cancel anytime?                                │
│    Yes. No contracts. Cancel from your dashboard.       │
└─────────────────────────────────────────────────────────┘
```

**Copy:**
- Headline: "Common questions"
- Accordion-style FAQ (6-8 questions)
- See `prd.md` for full FAQ list

### 10. Final CTA
**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Start recovering missed calls in 5 minutes             │
│                                                         │
│  [Start 5-minute setup →]                               │
│                                                         │
│  No credit card required. Cancel anytime.               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Copy:**
- Headline: "Start recovering missed calls in 5 minutes"
- CTA: "Start 5-minute setup →"
- Subtext: "No credit card required. Cancel anytime."

---

## Signup Flow

### Step 1: Account Creation
```
┌─────────────────────────────────────────────────────────┐
│  Create your account                                    │
│                                                         │
│  Business name: [________________]                      │
│  Your email:    [________________]                      │
│  Phone number:  [________________]                      │
│  Trade:         [Plumbing ▼]                            │
│                                                         │
│  [Continue →]                                           │
└─────────────────────────────────────────────────────────┘
```

**Fields:**
- Business name (required)
- Email (required, used for login)
- Phone number (required, their existing business number)
- Trade vertical (dropdown: Plumbing, Electrical, Roofing, Building, Locksmith, Other)

### Step 2: Payment
```
┌─────────────────────────────────────────────────────────┐
│  Choose your plan                                       │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  ○ Monthly: £19/month                           │   │
│  │                                                 │   │
│  │  ○ Annual: £190/year (save £38)                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  [Continue to payment →]                                │
│                                                         │
│  → Redirects to Paddle/Lemon Squeezy checkout           │
└─────────────────────────────────────────────────────────┘
```

**Flow:**
1. User selects monthly or annual
2. Click "Continue to payment"
3. Redirect to Paddle/Lemon Squeezy hosted checkout
4. Payment complete → webhook fires → account activated
5. Redirect to onboarding

### Step 3: Onboarding (5 minutes)
```
┌─────────────────────────────────────────────────────────┐
│  Welcome! Let's set up Calloto in 5 minutes             │
│                                                         │
│  Step 1 of 4: Your message template                     │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  "Hi! {business_name} missed your call.         │   │
│  │  Rough price {price_range}. Book your job       │   │
│  │  here: {booking_link}"                          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Business name:  [ABC Plumbing______]                   │
│  Price range:    [£80-150__________]                    │
│  Booking link:   [https://calendly.com/abc__]           │
│                                                         │
│  [Continue →]                                           │
└─────────────────────────────────────────────────────────┘
```

**Onboarding steps:**
1. **Message template** — Customize text-back message (pre-filled with business name, price range, booking link)
2. **Call forwarding** — Set up forwarding on iPhone/Android (with screenshots)
3. **Test text-back** — Call your number from another phone, receive test text
4. **Done** — Dashboard access, first missed call is live

---

## Conversion Optimization

### Above the Fold
- Headline must communicate value in <5 seconds
- Live missed-call counter (social proof)
- Clear CTA: "Start 5-minute setup →"
- Phone mockup animation (show product in action)

### Trust Signals
- "No contracts, cancel anytime"
- "100 text-backs included"
- "Works with your existing number"
- Live counter: "X missed calls recovered this week"
- Testimonials (once we have them)

### Objection Handling
- "Do I need a new number?" → No, keep your existing number
- "What about withheld numbers?" → Show as "not texted" in dashboard
- "How long to set up?" → 5 minutes
- "Can I cancel?" → Yes, anytime, no contracts

### Mobile Optimization
- All CTAs must be thumb-friendly (min 44px)
- ROI calculator sliders must work on touch
- Call forwarding instructions must be mobile-optimized
- Signup flow must work on mobile (no desktop-only forms)

---

## Technical Implementation

### Stack
- **Frontend:** Vanilla HTML/JS (no build step)
- **Styling:** Tailwind CSS (via CDN) or custom CSS
- **Animation:** CSS animations + minimal JS (no heavy libraries)
- **Hosting:** Static files served by FastAPI from `/static` directory

### Performance
- Page load <2 seconds (critical for conversion)
- No external images (use CSS/SVG for icons)
- Lazy-load below-fold sections
- Mobile-first responsive design

### Analytics
- Track signup funnel: landing → signup → payment → onboarding → activated
- Track ROI calculator usage (engagement signal)
- Track call forwarding setup completion (onboarding success)
- UTM parameters for source tracking (Google Maps scrape, Facebook, etc.)

---

## Next Steps
1. Build landing page HTML/CSS (static, served by FastAPI)
2. Implement ROI calculator (vanilla JS)
3. Build signup flow (FastAPI routes + Paddle/LS integration)
4. Build onboarding wizard (FastAPI + frontend)
5. Test on mobile (critical — 80%+ of tradespeople will use phone)
6. Deploy to calloto.com
7. A/B test headlines and CTAs once we have traffic
