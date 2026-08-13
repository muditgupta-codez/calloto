#!/usr/bin/env python3
"""Generate Calloto Marketing Plan PDF (reportlab, brand-styled)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether,
                                HRFlowable)

# ---------------- Fonts ----------------
FD = os.path.expanduser("~/.local/chromium/fonts/fonts/Open_Sans")
pdfmetrics.registerFont(TTFont("OS", f"{FD}/OpenSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("OS-B", f"{FD}/OpenSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("OS-I", f"{FD}/OpenSans-Italic.ttf"))

# ---------------- Brand palette ----------------
DARK   = colors.HexColor("#0b1110")
CARD   = colors.HexColor("#14211d")
BORDER = colors.HexColor("#1f352e")
TEXT   = colors.HexColor("#12201b")
MUTED  = colors.HexColor("#5d6f68")
ACCENT = colors.HexColor("#0e9f7e")   # darkened brand accent for print on white
ACCENT_L = colors.HexColor("#2dd4a7")
GREEN  = colors.HexColor("#34d399")
RED    = colors.HexColor("#e0534f")
AMBER  = colors.HexColor("#b8860b")
LIGHT  = colors.HexColor("#f2f7f5")
ROW    = colors.HexColor("#eaf3f0")

PAGE_W, PAGE_H = A4
MARGIN = 16 * mm
USABLE = PAGE_W - 2 * MARGIN

# ---------------- Styles ----------------
def st(name, **kw):
    base = dict(fontName="OS", fontSize=9.5, leading=14, textColor=TEXT,
                alignment=TA_LEFT, spaceAfter=5)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
    "body":    st("body", alignment=TA_JUSTIFY),
    "body-c":  st("body-c", alignment=TA_CENTER),
    "small":   st("small", fontSize=8.2, leading=11.5, textColor=MUTED),
    "small-w": st("small-w", fontSize=8.2, leading=11.5, textColor=colors.HexColor("#bfd4cc")),
    "h1":      st("h1", fontName="OS-B", fontSize=26, leading=32, textColor=colors.white),
    "h2":      st("h2", fontName="OS-B", fontSize=15, leading=19, textColor=ACCENT, spaceBefore=6, spaceAfter=3),
    "h3":      st("h3", fontName="OS-B", fontSize=10.5, leading=14, textColor=DARK, spaceBefore=4, spaceAfter=2),
    "bullet":  st("bullet", alignment=TA_JUSTIFY, leftIndent=11, bulletIndent=2, spaceAfter=3),
    "num":     st("num", fontName="OS-B", fontSize=9.5, leading=14),
    "tcell":   st("tcell", fontSize=8.6, leading=12),
    "tcell-b": st("tcell-b", fontName="OS-B", fontSize=8.6, leading=12, textColor=colors.white),
    "tcell-h": st("tcell-h", fontName="OS-B", fontSize=8.8, leading=12, textColor=DARK),
    "caption": st("caption", fontSize=7.8, leading=10.5, textColor=MUTED, spaceBefore=2),
    "quote":   st("quote", fontName="OS-I", fontSize=11, leading=16, textColor=ACCENT, alignment=TA_CENTER),
}

def B(txt):  # bold inline
    return f"<b>{txt}</b>"
def I(txt):
    return f"<i>{txt}</i>"
def GR(txt):  # accent inline
    return f'<font color="#0e9f7e">{txt}</font>'

def bullets(items, style="bullet"):
    out = []
    for it in items:
        out.append(Paragraph(it, S[style], bulletText="•"))
    return out

def section(num, title, tag="h2"):
    return [Spacer(1, 10), Paragraph(f"<font color='#0e9f7e'>{num}</font>&nbsp;&nbsp;{title}", S[tag]),
            HRFlowable(width="100%", thickness=0.7, color=BORDER, spaceBefore=2, spaceAfter=8)]

def callout(title, body, bg=GREEN, bar=ACCENT, title_color=None):
    inner = [Paragraph(f"<b>{title}</b>", st("co-t", fontName="OS-B", fontSize=9.3, leading=13,
                                             textColor=title_color or TEXT, spaceAfter=3))]
    inner += [Paragraph(p, st("co-b", fontSize=8.8, leading=12.5, textColor=TEXT)) for p in body]
    t = Table([[inner]], colWidths=[USABLE])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t

def datatable(header, rows, widths=None, align_map=None, fontsize=8.6):
    data = [[Paragraph(c, S["tcell-h"]) for c in header]]
    for r in rows:
        data.append([Paragraph(str(c), S["tcell"]) for c in r])
    if widths is None:
        widths = [USABLE / len(header)] * len(header)
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    t.setStyle(TableStyle(style))
    return t

# ---------------- Page furniture ----------------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    canvas.setFont("OS", 7.5); canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 8 * mm, "Calloto — Marketing Plan · v1.0 · Confidential")
    canvas.drawRightString(PAGE_W - MARGIN, 8 * mm, f"Page {doc.page}")
    canvas.restoreState()

def cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK); canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # subtle accent glow
    canvas.setFillColor(colors.HexColor("#102a22"))
    canvas.ellipse(PAGE_W/2 - 130*mm, PAGE_H - 130*mm, PAGE_W/2 + 130*mm, PAGE_H + 60*mm, stroke=0, fill=1)
    canvas.restoreState()

def build():
    doc = BaseDocTemplate(
        "/workspace/calloto/docs/Calloto-Marketing-Plan.pdf",
        pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=16*mm, bottomMargin=18*mm,
        title="Calloto Marketing Plan", author="Calloto",
    )
    frame = Frame(MARGIN, 18*mm, USABLE, PAGE_H - 16*mm - 18*mm, id="main")
    cover_frame = Frame(MARGIN, 18*mm, USABLE, PAGE_H - 16*mm - 18*mm, id="cover")
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=cover),
        PageTemplate(id="Body", frames=[frame], onPage=footer),
    ])
    E = []
    from reportlab.platypus import NextPageTemplate

    # ================= COVER =================
    E.append(NextPageTemplate("Body"))
    E.append(Spacer(1, 90*mm))
    E.append(Paragraph("Call<span fontname='OS-B' color='#2dd4a7'>oto</span>", st("logo", fontName="OS-B", fontSize=40, leading=44, textColor=colors.white)))
    E.append(Spacer(1, 6*mm))
    E.append(Paragraph("MARKETING PLAN", st("mk", fontName="OS-B", fontSize=17, leading=22, textColor=ACCENT_L)))
    E.append(Spacer(1, 4*mm))
    E.append(Paragraph("Never lose a customer to a missed call.", st("tag", fontName="OS-I", fontSize=12.5, leading=18, textColor=colors.HexColor("#bfd4cc"))))
    E.append(Spacer(1, 14*mm))
    E.append(Paragraph("Missed-call text-back for UK businesses · £19/mo · Trades first", st("cv", fontSize=9.5, leading=14, textColor=colors.HexColor("#96a8a0"))))
    E.append(Spacer(1, 40*mm))
    E.append(Paragraph("Version 1.0 · August 2026 · Prepared for Mudit Gupta", st("cv2", fontSize=8.5, leading=12, textColor=colors.HexColor("#6b7f76"))))
    E.append(PageBreak())

    # ================= 1. EXEC SUMMARY =================
    E += section("1", "Executive Summary")
    E.append(Paragraph(
        "Calloto turns missed calls into booked jobs for UK businesses that can't always answer. When a customer calls "
        "while a business is on a job, in a meeting, or on the road — a plumber up a ladder, a salon mid-appointment, a "
        "clinic with patients — Calloto detects the missed call in seconds and texts the customer back automatically: "
        "the business's name, a rough price range, and a one-tap booking link. The customer books on the spot instead of "
        "calling the next business. <b>£19/month, no contracts, 5-minute setup, works with the existing number.</b>", S["body"]))
    E.append(Spacer(1, 4))
    E.append(Paragraph(
        "The business is currently in validation: a live landing page and waitlist (early-bird £19/mo locked for "
        "signups), built on the founder's existing Voxvaani voice/WhatsApp stack — which gives Calloto a real moat: "
        "WhatsApp-native, DLT-compliant text-back, not a generic SMS gateway.", S["body"]))
    E.append(Spacer(1, 4))
    E.append(callout("Strategy in one sentence",
        ["Own the 'missed call → booked job' moment for UK businesses — trades as the flagship wedge, every other "
         "call-heavy vertical as expansion — at a price a single job pays for, distributed where businesses actually "
         "are: search, Facebook trade groups, local directories, and word of mouth."]))
    E.append(Spacer(1, 8))
    E.append(datatable(
        ["Element", "Position"],
        [
            ["Product", "Missed-call auto text-back + booking link for any business (SMS & WhatsApp); trades are the flagship vertical"],
            ["Market", "UK micro businesses that live by the phone: trades first (plumbers, electricians, builders), then salons, clinics, estate agents, repair services"],
            ["Price", "£19/mo early-bird, per trade business; one missed job (£200–£1,000) pays for a year"],
            ["Stage", "Validation — landing live, waitlist open, gate = 50+ real signups in 3 weeks"],
            ["North star", "Number of paid businesses"],
            ["Moat", "Voxvaani stack: WhatsApp Business API, DLT-compliant templates, virtual-number call detection"],
            ["90-day goal", "20+ paying businesses, ~£380 MRR, CAC under £40, payback under 2 months"],
        ],
        widths=[30*mm, USABLE-30*mm]))
    E.append(Paragraph("Note: all forward numbers in this plan are planning targets based on industry benchmarks — they are hypotheses to be replaced by actuals, not predictions of performance.", S["caption"]))
    E.append(PageBreak())

    # ================= 2. PRODUCT & POSITIONING =================
    E += section("2", "Product & Positioning")
    E.append(Paragraph(B("Value proposition"), S["h3"]))
    E.append(Paragraph(
        "For UK businesses that lose customers because they can't always answer, Calloto is the automatic receptionist "
        "that replies to every missed call with a text — name, price, booking link — so the customer books before they "
        "can call anyone else. Trades are the flagship use case (their pain is loudest and most measurable); the same "
        "flow serves salons, clinics, estate agents and repair services with per-industry message templates. Unlike "
        "lead-generation marketplaces that charge per lead or CRMs that require new workflows, Calloto is a flat-fee "
        "service that pays for itself with one job.", S["body"]))
    E.append(Paragraph(B("Five product pillars"), S["h3"]))
    E += bullets([
        f"<b>Catch</b> — missed call detected in seconds. No app to keep open, no new number.",
        f"<b>Reply</b> — instant auto text-back: trader's name, 'thanks for calling', rough price range they set.",
        f"<b>Book</b> — one-tap booking link with live availability; customer books while the trader is still on the ladder.",
        f"<b>See</b> — missed-call feed: every call, every reply, every booked job in one dashboard.",
        f"<b>Fit</b> — works with the existing number, 5-minute setup, quiet-hours control, WhatsApp text-back option, per-industry message templates.",
    ])
    E.append(Paragraph(B("Positioning statement"), S["h3"]))
    E.append(callout("For / Who / That / Unlike / Ours",
        ["<b>For</b> UK micro businesses that lose customers to unanswered calls — trades first, then salons, clinics, estate agents and repair services, "
         "<b>who</b> are on a job, in a meeting, mid-appointment, or on the road when the phone rings, "
         "<b>Calloto</b> is a missed-call text-back service that replies to customers instantly with the business's name, a rough price and a booking link, "
         "<b>unlike</b> per-lead marketplaces (Checkatrade, Bark) and heavyweight field-service CRMs, "
         "<b>because</b> it is flat-fee, WhatsApp-native, and set up in five minutes with no new number."],
        bg=ROW, bar=ACCENT))
    E.append(Paragraph(B("Competitive whitespace"), S["h3"]))
    E.append(datatable(
        ["Option trades use today", "How it works", "Cost", "The gap Calloto fills"],
        [
            ["Nothing / voicemail", "Call goes to voicemail, callback later", "£0 — lost jobs", "Customer has already booked elsewhere by callback"],
            ["Lead-gen marketplaces (Checkatrade, MyBuilder, Bark, TrustATrader)", "Pay per lead or subscription for lead flow", "£10–£50+ per lead; heavy competition", "Own the leads you already get — no bidding war, no per-lead fee"],
            ["Generic missed-call SMS (TeleMessage, TextMagic, etc.)", "SMS alert/auto-reply via gateway", "£20–£60/mo + per-message", "No WhatsApp-native reply, no booking link, clunky setup"],
            ["Field-service CRMs (Jobber, Housecall Pro, Tradify)", "Full job management suite", "£25–£60+/mo, complexity", "Overkill — 90% of features unused; Calloto is one job, one flow"],
            ["Calloto", "Missed call → instant text-back + booking link", "£19/mo flat, unlimited missed calls", "Instant time-to-value, WhatsApp-native, price of one job pays for a year"],
        ],
        widths=[44*mm, 44*mm, 38*mm, USABLE-126*mm]))
    E.append(PageBreak())

    # ================= 3. MARKET =================
    E += section("3", "Market Analysis")
    E.append(Paragraph(B("Market size & shape"), S["h3"]))
    E += bullets([
        f"UK construction and trades employ well over <b>1.5M</b> people, the large majority in businesses of 1–10 people — sole traders and micro firms dominate.",
        f"~<b>140k</b> plumbers/heating engineers, ~<b>220k</b> electricians, plus roofers, locksmiths, gardeners, cleaners and builders — each a segment that lives and dies by inbound calls.",
        f"Adjacent call-heavy verticals expand the platform TAM: ~<b>40k</b> salons & barbers, ~<b>15k</b> dental practices, thousands of estate agents, mobile mechanics and repair services — all miss calls they can't answer.",
        f"Across trades + adjacent verticals the addressable base is <b>400k+ UK micro businesses</b> that lose revenue to unanswered calls.",
        f"One missed call is typically <b>£200–£1,000 of work</b> for a trade, or a full booking for a salon/clinic — so £19/mo is a rounding error against a single recovered customer (landing page copy: 'one missed job pays for a year').",
    ])
    E.append(Paragraph(B("The pain is structural, not occasional"), S["h3"]))
    E += bullets([
        "Trades are physically unable to answer while working — hands dirty, up a ladder, driving.",
        "Customers call several traders to get a quote; the first to respond wins the job. Speed-to-response is the single biggest factor in conversion.",
        "Lead-generation platforms are expensive and bid-driven; trades resent paying for leads they feel they should have won anyway.",
        "Existing solutions are either too simple (no booking, no WhatsApp) or too complex (full CRM).",
    ])
    E.append(Paragraph(B("Why now"), S["h3"]))
    E += bullets([
        "WhatsApp Business API + DLT templates are now accessible to small builders at realistic cost — the moat is reachable.",
        "UK trades are digitally responsive: they live in Facebook trade groups, use booking links from Checkatrade, and adopt simple tools fast.",
        "The founder already operates Voxvaani (voice & WhatsApp automation) — the delivery stack exists; the marginal cost of adding Calloto is product work, not infra.",
    ])
    E.append(PageBreak())

    # ================= 4. AUDIENCE =================
    E += section("4", "Target Audience & Segments")
    E.append(Paragraph(B("Ideal customer profile (ICP)"), S["h3"]))
    E += bullets([
        f"<b>Who:</b> UK micro business (1–5 people) that lives by the phone — sole trader trade, salon, clinic, estate agency; typically 30–60.",
        f"<b>Behaviour:</b> takes calls all day, misses several per week, quotes/books by phone, loses customers to whoever answers first.",
        f"<b>Current spend:</b> pays Checkatrade/Bark for leads (trades), or relies on word of mouth and Google reviews (everyone).",
        f"<b>Tech profile:</b> smartphone-first, not SaaS-savvy; wants to set it up in minutes and forget it.",
        f"<b>Trigger event:</b> 'I was on a job and missed a call — they booked someone else.' Heard from the van, the salon chair, the trade group.",
        f"<b>Platform rule:</b> one generic flow + per-industry message templates. The waitlist's segment picker records demand per vertical, so the data — not opinion — picks the next beachhead after trades.",
    ])
    E.append(Paragraph(B("Persona — 'Paul the Plumber'"), S["h3"]))
    E.append(callout("Paul, 44, sole trader heating engineer, West Midlands",
        ["Works alone in a van, 6 days a week. Misses 5–10 calls a week while on jobs — a mix of new customers, insurance call-outs and emergency repairs. Spends ~£150/mo on lead platforms and hates it. Lost a £1,800 boiler swap last month because the customer called the next guy while Paul was under a sink.",
         "Paul's bar for adopting a tool: set up in one evening, nothing to install on his phone, no new number to print on the van. Calloto's pitch — 'texts them back with your name and a price while you're still working' — maps exactly to the £1,800 job he just lost."],
        bg=ROW, bar=AMBER))
    E.append(Paragraph(B("Segments & prioritisation"), S["h3"]))
    E.append(datatable(
        ["Priority", "Segment", "Why / behaviour", "Entry angle"],
        [
            ["P1 — wedge", "Plumbers & heating engineers", "Highest call volume, emergencies, winter spikes, already pay for leads", "Boiler emergency angle: 'customer needs a fix now, not later'"],
            ["P1 — wedge", "Electricians", "High inbound, fast-moving quotes, many solo traders", "'First to respond wins the rewire'"],
            ["P2", "Roofers & locksmiths", "Urgent, high-value, poor response = lost job", "Emergency repair angle"],
            ["P2", "Gardeners, cleaners, window cleaners", "Lower ticket but very high call volume, price-sensitive", "Volume angle: 'every missed call is a quote gone'"],
            ["P2 — expand", "Salons & barbers", "Missed booking calls = silent churn; appointment culture", "Booking angle: 'turn a missed call into a booked chair'"],
            ["P2 — expand", "Clinics & dentists", "Rescheduling-heavy; patients call back anywhere", "Care angle: 'never keep a patient waiting in voicemail'"],
            ["P2 — expand", "Estate & letting agents", "Enquiries are time-critical; agents are often out", "Viewing angle: 'answer every enquiry, even mid-viewing'"],
            ["P3", "Builders & general contractors", "Longer sales cycles, fewer calls, referral-heavy", "Keep warm via content; not launch focus"],
        ],
        widths=[24*mm, 40*mm, USABLE-64*mm-32*mm, 32*mm]))
    E.append(PageBreak())

    # ================= 5. MESSAGING =================
    E += section("5", "Messaging Framework")
    E.append(Paragraph(B("Hero message"), S["h3"]))
    E.append(Paragraph("Never lose a customer to a missed call.", S["quote"]))
    E.append(Spacer(1, 4))
    E.append(Paragraph(
        "A customer calls while you're on a job, in a meeting, or on the road. Calloto texts them back instantly — your "
        "name, a rough price, and a booking link. They choose you, not the next business that picks up.", S["body-c"]))
    E.append(Spacer(1, 6))
    E.append(Paragraph(B("Message variants by channel"), S["h3"]))
    E.append(datatable(
        ["Channel", "Message angle"],
        [
            ["Google Search ad", "'Missed calls costing you customers? Calloto texts them back with your price & booking link — £19/mo. 5-min setup.'"],
            ["Facebook / Instagram", "Video: POV you're on a job and the phone rings — cut to the customer's phone getting your text. 'They book. You never knew.'"],
            ["Trade group post", "'Genuinely annoying how many jobs I lost to missed calls. Now calls text themselves back. £19/mo, no contract — happy to show anyone who asks.'"],
            ["Salon/clinic community post", "'How many no-shows actually started as a missed call? Ours text back now with a booking link. Game changer for £19/mo.'"],
            ["Directory listing", "'Missed-call text-back for UK businesses. Instant reply with your name, price and booking link. One missed job pays for a year.'"],
            ["Waitlist email", "Subject: 'The customer you lost last week' — story-driven, early-bird £19 locked, area-launch urgency."],
        ],
        widths=[40*mm, USABLE-40*mm]))
    E.append(Paragraph(B("Features → benefits"), S["h3"]))
    E.append(datatable(
        ["Feature", "Benefit"],
        [
            ["Missed call detected in seconds", "Customer hears back while you're still working — they never have time to call the next guy"],
            ["Auto text-back with your name & rough price", "Feels personal, sets price expectations, filters out tyre-kickers"],
            ["One-tap booking link", "Customer books instead of 'calling back later' — later never happens"],
            ["Works with existing number", "No new number on the van, the shop window, or the website — customers keep calling the number they know"],
            ["Missed-call feed", "Know exactly what you missed and what you recovered — the ROI is visible"],
            ["WhatsApp text-back", "Reaches the customer in the app they actually check"],
            ["Per-industry templates", "Salons, clinics, agents and trades each get message defaults that match how their customers talk"],
            ["Quiet hours", "Business controls when the bot answers — no calls from mum at 11pm get the boiler price"],
        ],
        widths=[55*mm, USABLE-55*mm]))
    E.append(Paragraph(B("Objection handling"), S["h3"]))
    E.append(datatable(
        ["Objection", "Response"],
        [
            ["'Do my customers need an app?'", "No — they get a normal text or WhatsApp message on any phone. Nothing to install."],
            ["'Do I need a new number?'", "No — it attaches to your existing number via call forwarding. You keep taking calls the same way; we just catch the misses."],
            ["'What if I'm not on a job and just don't want to answer?'", "Set your hours and quiet time — outside them, calls go straight to auto-text-back."],
            ["'Isn't this just for plumbers?'", "No — any business that misses calls: salons, clinics, estate agents, repair services and more. Trades get early access first; others onboard by demand."],
            ["'Why £19? What's the catch?'", "Early-bird pricing, locked for everyone on the waitlist. One recovered job pays for the year. No contracts, cancel anytime."],
        ],
        widths=[48*mm, USABLE-48*mm]))
    E.append(PageBreak())

    # ================= 6. GO-TO-MARKET =================
    E += section("6", "Go-to-Market Plan")
    E.append(Paragraph(
        "Three phases, each with an explicit go/no-go decision. The validation gate (Phase 0) protects the build from "
        "being wasted on a market that isn't reaching for the product.", S["body"]))
    E.append(datatable(
        ["Phase", "Timeline", "Objective", "Go/no-go"],
        [
            ["0 — Validate", "Weeks 1–3", "50+ real waitlist signups from targeted outreach; BetaList live; first social proof", "50+ signups → build the beta. Under 50 → re-evaluate messaging/segment before spending on the product"],
            ["1 — Launch", "Weeks 4–12", "First 10–20 installs as free beta; first 20+ paying businesses; referral loop running", "Activation ≥40% of cohort & first 5 paying → open paid marketing"],
            ["2 — Scale", "Months 3–6", "Winning channels at £15–25/day; £380→£1,500+ MRR; partnerships (associations, suppliers)", "CAC < £40 and payback < 2 months → scale spend; otherwise kill the channel"],
        ],
        widths=[26*mm, 30*mm, USABLE-56*mm-34*mm, 34*mm]))
    E.append(Spacer(1, 6))
    E.append(Paragraph(B("Phase 0 priorities (this week)"), S["h3"]))
    E += bullets([
        "Submit to BetaList (package already prepared in docs/betalist-submission.md).",
        "Seed the waitlist: founder posts in 5–10 UK trade Facebook groups, r/Plumbing, r/DIYUK, Indie Hackers — story-led, no hard sell.",
        "Install basic analytics on the landing page (page views, form drop-off) so signup conversion is measurable from day one.",
        "Capture signup source (UTM on each channel link) so we know where the 50 signups came from.",
        "Prepare the waitlist nurture email sequence (3 emails: story → early-bird lock → launch announcement).",
    ])
    E.append(Paragraph(B("Phase 1 launch checklist"), S["h3"]))
    E += bullets([
        "Convert waitlist → beta cohort: 10–20 installs, 14-day free trial, concierge onboarding (set up their message & price range with them).",
        "Launch referral program: 1 month free for every business that brings a paying signup.",
        "Switch on Google Search Ads (small test) on high-intent terms — see Channel Plan.",
        "Collect 5–10 customer stories / screenshots of recovered jobs for social proof.",
        "Watch every activation: first text-back received within 24h of setup is the 'aha' to optimise toward.",
    ])
    E.append(PageBreak())

    # ================= 7. CHANNELS =================
    E += section("7", "Channel Plan")
    E.append(Paragraph(
        "Channels are hypotheses. The 90-day job is to test each with real spend/effort, keep the winners, and kill the "
        "losers by week 6 — before budget bleeds. A lean solo-founder budget of ~£300/month is enough to get signal.", S["body"]))
    E.append(datatable(
        ["Channel", "Role", "Budget (90d)", "Target CAC", "How to win"],
        [
            ["BetaList + launch directories", "First cold traffic + press/backlinks", "£0", "£0 (organic)", "Strong listing, 3 screenshots, category Communication/Business Tools, status 'Beta — waitlist'"],
            ["Google Search Ads", "High-intent buyers ('missed call text back', 'auto reply missed calls', 'callcatch alternative')", "£450 (£15/day)", "≤ £35", "Exact/phrase match, 5–8 ads, landing → waitlist with UTM; add competitor terms"],
            ["Facebook / Instagram", "Trades are heavy FB users; interest + radius targeting; retargeting", "£300 (£10/day)", "≤ £40", "Video-first (ladder POV), 10-mile radius around target postcodes, retarget waitlist visitors"],
            ["Trade communities (FB groups, Reddit, forums)", "Trusted, free, founder-led demand", "£0", "£0", "Genuine participation + story posts, not spam; DM follow-ups; screenshots of recovered jobs"],
            ["Local SEO & Google Business Profile", "Long-term organic capture ('plumber near me' → answer the call better)", "£0", "£0", "GBP posts, review generation, keyword-tuned landing copy"],
            ["Referral programme", "Trades know trades — highest-trust channel", "1 month credit/ref", "£19 (credit)", "In-app 'Refer a trade' + concierge ask at activation"],
            ["Content (TikTok/Reels)", "Brand + inbound over months 2–6", "£0", "£0", "2–3 clips/week: POV, 'jobs I recovered this week', trade humour; link in bio"],
            ["Waitlist nurture email", "Convert existing signups — the cheapest revenue", "£0", "£0", "3-email sequence + launch-day blast with early-bird deadline"],
            ["Partnerships (NICEIC, CIPHE, FMB, Plumb Center/Screwfix trade counters)", "Credibility + volume in months 4+", "£0 (time)", "Low", "Offer member-discount; trade-counter flyers with QR to waitlist"],
        ],
        widths=[44*mm, 52*mm, 26*mm, 20*mm, USABLE-142*mm]))
    E.append(Spacer(1, 4))
    E.append(callout("Channel discipline",
        ["Week 1–3: only free channels (communities, BetaList, email) — they also produce the 50-signup gate.",
         "Week 4–6: start Search Ads (highest intent) + one social test at ~£10/day.",
         "Week 6: kill list — any paid channel without at least 2 waitlist signups per £10 spent gets paused.",
         "Month 3: put 70% of budget into the single winning channel; keep one testing slot."],
        bg=ROW, bar=RED))
    E.append(PageBreak())

    # ================= 8. FUNNEL =================
    E += section("8", "Funnel & Conversion Plan")
    E.append(Paragraph(
        "The funnel is short: visitor → waitlist → beta install → activation (first text-back) → paying. Every stage "
        "has a benchmark target; the job is to measure and beat them.", S["body"]))
    E.append(datatable(
        ["Stage", "Definition", "Target rate (benchmark-based)", "Leverage"],
        [
            ["Visit → waitlist", "Landing page visit to email signup", "2–4%", "Copy, social proof counter, early-bird lock, mobile UX"],
            ["Waitlist → beta install", "Signup to taking a 14-day trial", "≥ 40%", "Concierge onboarding, launch-day email, referral credit"],
            ["Beta → paid", "14-day trial to paying £19/mo", "≥ 30%", "Activation in first 24h, 'recovered job' screenshots, renewal email"],
            ["Monthly churn", "Paying businesses lost / month", "< 5%", "Value emails, referral credit, product velocity"],
            ["CAC (paid)", "Ad spend / new paying customer", "≤ £40", "Search intent terms, retargeting, referral mix"],
            ["Payback", "Months of revenue to recover CAC", "< 2 months", "Front-load activation; annual option at 2 months free"],
        ],
        widths=[38*mm, 52*mm, 38*mm, USABLE-128*mm]))
    E.append(Spacer(1, 6))
    E.append(callout("Worked example (planning, not prediction)",
        ["1,000 visitors in a month at 3% → 30 signups. At 40% activation → 12 trials. At 30% → ~4 paying. "
         "That path alone is slow — which is why referral (free) and Search (intent) are the growth engines, "
         "and why the activation rate is the single most important number to optimise: moving activation 40% → 55% "
         "adds ~2 paying customers per 100 signups."],
        bg=ROW, bar=ACCENT))
    E.append(Paragraph(B("Activation is the 'aha'"), S["h3"]))
    E += bullets([
        "A trader's first text-back received (a real customer replying or booking) within 24 hours of setup is the strongest predictor of retention — optimise everything toward it.",
        "Concierge onboarding in Phase 1: set up their name/message/price range with them over a 10-minute call.",
        "Show ROI weekly in the missed-call feed: 'This week you recovered 3 jobs worth ~£600.'",
    ])
    E.append(PageBreak())

    # ================= 9. BUDGET =================
    E += section("9", "Budget — 90 Days (Lean)")
    E.append(Paragraph(
        "Deliberately small. This budget buys signal, not scale: enough to identify the one channel that works before "
        "committing real money. All figures in GBP.", S["body"]))
    E.append(datatable(
        ["Line item", "90-day spend", "Notes"],
        [
            ["Google Search Ads", "£450", "£15/day weeks 4–12; pause any ad group with 0 signups after £60"],
            ["Facebook / Instagram ads", "£300", "£10/day one test campaign; retargeting after week 6"],
            ["Tools (email, analytics, landing)", "£60", "Free tiers where possible (email via Voxvaani/own stack, GA/Plausible, no paid landing builder)"],
            ["Screenshots / creative", "£20", "Mock customer-phone images for ads & social"],
            ["Contingency", "£70", "Unexpected test (one more channel or boosted post)"],
            ["Total", "£900 (~£300/mo)", "≈ 47 months' revenue of one paying customer — deliberate asymmetry"],
        ],
        widths=[52*mm, 28*mm, USABLE-80*mm]))
    E.append(Spacer(1, 4))
    E.append(callout("Spend guardrails",
        ["Stop any channel after 3 weeks of spend if CAC ≥ £40 or no signups.",
         "The 50-signup gate is achievable at £0 spend via communities + BetaList — paid channels are for scaling proof, not for reaching the gate.",
         "Every £1 of ad spend must be traceable to a signup via UTM + waitlist source field."],
        bg=ROW, bar=RED))
    E.append(PageBreak())

    # ================= 10. KPIs =================
    E += section("10", "KPIs & 90-Day Targets")
    E.append(Paragraph(B("North star"), S["h3"]))
    E.append(Paragraph("Number of paying trade businesses.", S["quote"]))
    E.append(Spacer(1, 6))
    E.append(datatable(
        ["KPI", "Now", "Day 30 (gate)", "Day 60", "Day 90", "Why it matters"],
        [
            ["Waitlist signups", "0–20", "50+", "120+", "250+", "Validation gate + launch fuel"],
            ["Landing → signup rate", "—", "≥ 2%", "≥ 2.5%", "≥ 3%", "Copy/messaging health"],
            ["Beta installs (cumulative)", "0", "0", "15–25", "30–45", "Funnel reach"],
            ["Activation rate (first text-back)", "—", "—", "≥ 40%", "≥ 50%", "Retention predictor"],
            ["Paying businesses", "0", "0", "5–10", "20+", "North star"],
            ["MRR", "£0", "£0", "£95–190", "£380+", "Revenue engine"],
            ["Churn", "—", "—", "< 5%/mo", "< 5%/mo", "LTV assumption"],
            ["CAC (paid mix)", "—", "—", "≤ £40", "≤ £35", "Unit economics"],
            ["Payback", "—", "—", "< 2 mo", "< 2 mo", "Cash-flow safety"],
        ],
        widths=[40*mm, 20*mm, 24*mm, 24*mm, 24*mm, USABLE-132*mm]))
    E.append(Spacer(1, 4))
    E.append(Paragraph(
        "These are targets derived from benchmark ranges for B2B SaaS micro-products — they will be replaced by "
        "actuals as data arrives. No figure here is a promise of performance; the 90-day review re-baselines "
        "everything against real numbers.", S["caption"]))
    E.append(PageBreak())

    # ================= 11. ROADMAP =================
    E += section("11", "Roadmap — 30 / 60 / 90")
    E.append(datatable(
        ["Window", "Focus", "Key actions"],
        [
            ["Days 0–30", "Validate & prepare", "BetaList submission; 5–10 trade-group/Reddit posts; UTM + analytics live; 3-email nurture sequence; first 50 signups tracked by source; no product spend until gate is met"],
            ["Days 31–60", "Launch beta & first revenue", "Convert waitlist → 10–20 beta installs with concierge onboarding; referral programme live; Search Ads test (£15/day); first 5–10 paying; 5 customer screenshots; kill-list review at week 6"],
            ["Days 61–90", "Scale the winner", "70% budget into the winning channel; GBPs + local SEO pass; partnerships outreach (associations, trade counters); 20+ paying / £380+ MRR; 90-day review: re-baseline targets, decide scale vs refine"],
        ],
        widths=[26*mm, 32*mm, USABLE-58*mm]))
    E.append(Spacer(1, 8))
    E.append(Paragraph(B("Decision rules that end the experiment cleanly"), S["h3"]))
    E += bullets([
        "<b>Gate miss:</b> under 50 signups at day 30 → the message or the segment is wrong. Re-interview 10 signups/non-signups, re-run 2 weeks, then decide build/hold.",
        "<b>Activation wall:</b> beta installs but <40% get a first text-back → onboarding or delivery (call forwarding) is broken; fix before scaling ads.",
        "<b>Unit economics fail:</b> CAC > £40 with payback > 2 months at day 90 → product is the constraint, not marketing.",
    ])
    E.append(PageBreak())

    # ================= 12. RISKS =================
    E += section("12", "Risks & Mitigations")
    E.append(datatable(
        ["Risk", "Likelihood", "Impact", "Mitigation"],
        [
            ["'Works with existing number' fails on some UK networks (conditional forwarding support varies)", "Medium", "High — core promise", "Test on the 4 major networks before launch; ship virtual-number fallback (Voxvaani stack) that keeps the same customer UX; position setup as '5 minutes with our help'"],
            ["WhatsApp Business API / DLT template approval delays or rejections", "Medium", "High", "Start template pre-approval early; SMS text-back as the always-on fallback so delivery never depends on one channel"],
            ["Carrier/SMS spam filtering on text-backs", "Medium", "Medium", "Use registered sender IDs, keep messages short and non-spammy, monitor delivery receipts, WhatsApp-first where possible"],
            ["Lead-gen marketplaces out-spend and out-brand (Checkatrade etc.)", "High", "Medium", "Don't compete on lead flow — compete on owning the trader's own missed calls; price and message are complementary, not head-on"],
            ["Generic copycats (SMS gateway + Zapier) emerge at lower price", "Medium", "Medium", "Moat = WhatsApp-native DLT compliance + booking-link UX + trades-specialist positioning; move fast in launch window"],
            ["Seasonality — heating call volume collapses in summer", "Medium", "Low", "Launch into winter (peak for plumbers); multi-segment mix (electricians, roofers) smooths the curve"],
            ["Solo-founder bandwidth (Voxvaani + Calloto + support)", "High", "Medium", "One channel at a time; concierge onboarding is also the feedback loop; automate activation emails and referral crediting from day one"],
        ],
        widths=[52*mm, 20*mm, 20*mm, USABLE-92*mm]))
    E.append(Spacer(1, 6))
    E.append(callout("Technical honesty (for the build decision)",
        ["The 'existing number' promise is the highest-risk feature. The landing page sells it, so the beta must prove it "
         "across UK networks before charging anyone. If forwarding is flaky, the fallback is a Voxvaani virtual number "
         "that the customer dials — same text-back experience, slightly different setup story. Decide this in beta, not "
         "after the first 100 paying customers."],
        bg=ROW, bar=AMBER))

    # ================= 13. ASSETS =================
    E += section("13", "Launch Assets Checklist")
    E.append(datatable(
        ["Asset", "Status", "Owner / notes"],
        [
            ["Landing page + waitlist (waitlist API, position counter, industry segment picker)", "DONE", "Live at sslip.io URL; segment data decides next vertical; add /data volume before real signups"],
            ["BetaList submission package", "DONE", "docs/betalist-submission.md — submit this week"],
            ["Analytics on landing (views, form events, UTM)", "TODO", "Install before Phase 0 outreach"],
            ["Waitlist nurture emails (3-email sequence)", "TODO", "Story → early-bird lock → launch; from Voxvaani sender"],
            ["Demo video (30–60s, phone screenshots)", "TODO", "Customer phone POV: call → text → booked"],
            ["Google Business Profile for 'Calloto' brand page", "TODO", "Long-term organic; also for GBP review engine"],
            ["Facebook page + 5 trade-group participation", "TODO", "Founder-led, story-first"],
            ["Referral mechanic (1 month credit)", "TODO", "Launch with Phase 1"],
            ["Case-study template + recovered-job screenshots", "TODO", "First 5 customers → social proof pack"],
        ],
        widths=[62*mm, 22*mm, USABLE-84*mm]))
    E.append(Spacer(1, 8))
    E.append(Paragraph(
        "Calloto — marketing plan v1.0. Prepared for Mudit Gupta, August 2026. All targets are planning hypotheses "
        "pending real data. Re-baseline at the day-30 gate and the day-90 review.", S["small"]))

    doc.build(E)
    print("PDF built")

build()
