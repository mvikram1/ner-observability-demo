# Wells Fargo NER Customer Segmentation Demo
**Google Slides Ready Outline - 9 Slides**

Copy each slide section below directly into Google Slides. Formatting guidance is in brackets.

---

## SLIDE 1: OPENING & CONTEXT

**Title:** Named Entity Recognition for Customer Segmentation: The Observability Problem

**Slide Content:**
[Left side - large text]
Named Entity Recognition for Customer Segmentation:
The Observability Problem

[Right side - small subtitle]
A production case study in cross-stack monitoring

**Speaker Notes:**

"I want to start with a problem I worked on at a previous company—building NER models to help financial services companies like yours segment customers by entity types: individuals, organizations, high-net-worth accounts, etc. 

One of our clients was a compliance-focused financial institution. What we learned is that NER in production is surprisingly fragile, and traditional observability—infrastructure monitoring, model monitoring, data quality checks—they all operate in silos. When something goes wrong, you're manually connecting three different systems to figure out what happened.

I want to walk you through that use case, show you what we recommended at the time, and then we can play through the decision-making together. By the end, you'll understand three fundamentally different approaches to solving this, and when each one makes sense.

Let's start with the reality of what most financial services companies have today."

---

## SLIDE 2: THE BROWNFIELD REALITY

**Title:** What Wells Fargo Likely Has Today

**Slide Content:**

[Create a table with 3 columns: Component | Current State | Problem]

Infrastructure Monitoring | Datadog (mature) | Shows latency/availability, but not model-specific signals

Model Monitoring | Custom Python dashboards (daily/weekly checks) | Reactive, not predictive; lag in detection

Data Quality | Basic checks (null rates, schema validation) | Incomplete; doesn't catch entity distribution drift

Incident Response | ServiceNow rules (static routing) | Slow triage; can't determine root cause quickly

Compliance/Audit | Locked-down security controls | Good for security; complicates tool choices

[Below table, bold text]
**The Gap:**
When NER accuracy drops 3%, you can't quickly answer: Is it the model? The data? Infrastructure? All three?

**Speaker Notes:**

"Let me paint a realistic picture. Wells Fargo has Datadog running—probably for a while now. It's mature, it works, it tells you when infrastructure is healthy or not. 

But when we talk about NER models in production, Datadog doesn't understand model-specific signals. It doesn't know if the model is recognizing entities correctly.

You probably have custom Python scripts or dashboards checking accuracy daily or weekly. That works, but it's reactive. You only know something's wrong after it's already degraded for hours or days.

Data quality checks? You probably have some—null rates, schema validation. But they're incomplete. You're not catching entity type distribution shifts, which is actually one of the biggest failure modes for NER.

When an incident happens, ServiceNow routes it somewhere, but the triage is slow because nobody has a unified picture.

Here's the real problem: these three systems—infrastructure, model, data—are all monitoring the same production system, but they're not talking to each other. When NER accuracy drops 3%, you have to manually correlate data from three systems. That's the core problem we're trying to solve."

---

## SLIDE 3: DISCOVERY QUESTIONS

**Title:** Understanding Your Constraints

**Slide Content:**

[Use a simple bullet list format - these are the questions, not answers yet]

• How much engineering capacity do you have available for this?

• What's your timeline? When do you need this working?

• Do you have strict data residency or GDPR requirements?

• What's your stance on open source vs. commercial software?

• When a model incident happens, how long does triage currently take?

• How mature is your current data quality monitoring?

• What's your risk tolerance around adopting new tooling?

**Speaker Notes:**

"These seven questions are critical. The answers determine everything—which path makes sense, how long it takes, what it costs, how much you maintain long-term.

Let me walk through each one, because I want to show you how discovery shapes the recommendation. It's not 'one solution fits all'—it's 'here's your situation, here's what makes sense.'

First: engineering capacity. If you have one engineer available, that rules out some paths entirely. If you have three engineers for months, that opens up options.

Second: timeline. This is often a forcing function. If you need this working in six weeks, that changes what's possible.

Third: GDPR and data residency. This one's important for financial services. If customer data can't leave your infrastructure, that's a hard constraint. If you're EU-based and processing EU customer data—which you are with NER—GDPR is probably a concern.

Fourth: open source preference. Some organizations have strong preferences here. That's a valid preference, and it shapes the recommendation.

Fifth: how bad is the problem today? How long does it take to triage an incident? If you're spending four hours manually debugging, you're in more pain than if you're spending 30 minutes with a structured process.

Sixth: data quality maturity. If you already have sophisticated data quality monitoring, we can build on that. If you're starting from scratch, that's different.

Seventh: risk tolerance. Some teams want to build everything themselves (control). Some teams want to buy proven solutions (speed). Both are valid.

I'm going to ask you these questions in a moment, and based on your answers, I'll walk you through why a particular path makes sense for your situation."

---

## SLIDE 4: THE THREE PATHS (High-Level Comparison)

**Title:** Three Fundamentally Different Approaches

**Slide Content:**

[Create a comparison table with 4 columns: Dimension | Path 1: Custom | Path 2: Hybrid | Path 3: InsightFinder]

Timeline | 16-20 weeks | 6-8 weeks | 4-6 weeks

Engineering Effort | 2-3 FTE for 4+ months | 1 FTE for 6-8 weeks | Minimal (SaaS)

Data Residency | On-prem (everything) | On-prem (ingestion) + Cloud (analysis) | Cloud only

GDPR Compliance | ✓ Full | ✓ Full | ✗ Problematic

Total Cost (5yr) | $$$$ | $$$ | $$

Ops Burden | Very High | Moderate | Low

Causal Inference | You build it (hard) | InsightFinder provides | InsightFinder provides

Best For | Maximum control, long timeline | Balance of speed & control, compliance | Speed, low capacity

**Speaker Notes:**

"Here's the executive summary. Three different approaches, very different tradeoffs.

Path 1 is pure custom: you build everything on-prem. Maximum control, nobody owns your data, but it takes 16-20 weeks and requires 2-3 engineers full-time for months. And you're taking on the ops burden for years.

Path 2 is hybrid: you build a simple ingestion layer that lives on your infrastructure, and you use InsightFinder for the hard part—correlation and analysis. Still four months of engineering, but only one person. You keep data on-prem, so GDPR compliant. Faster to value.

Path 3 is pure InsightFinder SaaS: fastest, lowest engineering lift, but data goes to cloud. That's great if GDPR isn't a concern, but for a financial institution processing customer text, it's usually problematic.

Notice that Path 2 is kind of the goldilocks zone: not too fast, not too slow; not too cheap, not too expensive; balance of speed and control.

Let me walk through each path in detail."

---

## SLIDE 5: PATH 1 — PURE CUSTOM ON-PREM

**Title:** Option 1: Build Everything Yourself

**Slide Content:**

[Create a simple architecture diagram description]
Architecture:
NER System → Custom Python Service (on-prem) → Grafana Dashboard → ServiceNow

[Bullet points for Pros]
Pros:
• Maximum control (no vendor lock-in)
• Fully GDPR compliant (nothing leaves on-prem)
• Can customize rules exactly as you want
• Aligns with security-first culture

[Bullet points for Cons]
Cons:
• High engineering investment (2-3 FTE × 16-20 weeks)
• Building causal inference is non-trivial (hard ML/stats problem)
• Ongoing maintenance burden (1.5-2 FTE long-term)
• Risk of gaps (what you didn't think to monitor)

[Bold text]
**When This Path Makes Sense:**
You have 2+ engineers available for 16+ weeks, strict security/GDPR requirements, prefer open source, flexible timeline, and team has ML/statistics expertise.

**Speaker Notes:**

"This path: you own everything. You build a Python service that pulls model metrics from your database, infrastructure metrics from CloudWatch, data quality signals. You run correlation logic—and this is where it gets hard—you have to figure out: when accuracy drops and data distribution shifted, is that causally related? Or coincidence?

That's a non-trivial problem. You're solving unsupervised anomaly detection plus causal inference. Doable, but requires real expertise.

Pros are clear: you control everything, no vendor dependency, fully compliant with GDPR because nothing leaves.

But the cons are real too. You're committing 2-3 engineers for four months. And then someone has to maintain it forever. That's 1.5 FTE indefinitely. If your lead engineer leaves, who maintains it? That's a risk.

This path makes sense if you have the capacity, you want maximum control, and your timeline is flexible."

---

## SLIDE 6: PATH 2 — HYBRID (CUSTOM + INSIGHTFINDER)

**Title:** Option 2: Build Ingestion, Buy Analysis

**Slide Content:**

[Architecture description]
Architecture:
NER System (on-prem) → Custom Python Ingestion (you build) → InsightFinder Cloud → Root Cause Analysis

[Key differentiator - bold]
**What's Special About This Path:**
You keep raw customer data on-prem. Custom layer anonymizes and sends only metrics/signals to InsightFinder. InsightFinder does causal inference.

[Pros bullets]
Pros:
• Faster to value (6-8 weeks vs. 16-20 weeks)
• Lower engineering investment (1 FTE instead of 2-3)
• You get causal inference for free (15 years of research, hard to build)
• GDPR compliant (data stays on-prem, signals go to cloud)
• Lower ongoing ops burden (0.5 FTE long-term)

[Cons bullets]
Cons:
• Depends on InsightFinder's correlation logic (less control)
• SaaS dependency (if service goes down, lose analysis; not data)
• Ingestion layer maintenance (0.5 FTE ongoing)

[Bold text]
**When This Path Makes Sense:**
You need GDPR/data residency compliance, 1-2 engineers available for 6-8 weeks, want to balance speed and control, want causal inference without building it yourself, timeline is 8-12 weeks.

**Speaker Notes:**

"This is the path we recommended at my previous company. And I think it's the right call for Wells Fargo.

Here's the key insight: causal inference is hard. Building it yourself takes months and requires real expertise. But InsightFinder has spent 15 years solving this problem. Why duplicate that effort?

So instead: you build a simple Python service. Maybe 2,000-3,000 lines of code. It pulls your model metrics—accuracy, confidence scores, entity type distribution. It pulls infrastructure metrics from CloudWatch. It pulls data quality signals. Then it sends all of that to InsightFinder.

But here's the important part: you don't send raw customer data. You send anonymized signals. The actual NER text, the customer information—that stays on-prem. You're just sending: 'model accuracy is 87%, entity distribution shifted 5%, latency spiked 10%.'

InsightFinder receives those signals and runs their causal inference engine. 'Accuracy dropped AND entity distribution shifted AND latency was stable. Root cause: data quality issue, specifically entity type distribution changed.'

GDPR compliant, because raw data never leaves.

One engineer builds the ingestion layer in 6-8 weeks. You've got causal inference. You're not maintaining a complex system long-term—just the ingestion layer, which is straightforward.

This is the path I'd recommend for your situation."

---

## SLIDE 7: PATH 3 — PURE INSIGHTFINDER CLOUD

**Title:** Option 3: Full SaaS, Minimal Engineering

**Slide Content:**

[Architecture description]
Architecture:
NER System → InsightFinder SDK → InsightFinder Cloud (SaaS, managed) → Root Cause Analysis + Alerts

[Pros bullets]
Pros:
• Fastest time to value (4-6 weeks)
• Lowest engineering effort (minimal integration work)
• Lowest ongoing ops burden (SaaS managed service)
• Full platform (everything included)
• Best-in-class causal inference (15 years of research)

[Cons bullets]
Cons:
• Data residency / GDPR issue (customer data goes to cloud)
• Less control over raw data
• SaaS vendor dependency
• **Probably not viable for this use case** (compliance constraints)

[Bold text]
**When This Path Makes Sense:**
You have no GDPR/data residency requirements, urgent timeline (4-6 weeks), minimal engineering capacity, comfortable with SaaS vendor dependency, want the full proven platform.

**Speaker Notes:**

"This is the fastest path. You integrate InsightFinder's SDK into your NER pipeline, and they handle everything. Full platform, fully managed, you don't run anything.

Pros are obvious: fastest, simplest, lowest ops burden. You get the full platform, including everything I'll explain in a moment.

But here's the problem for financial services: data goes to cloud. We're talking about NER models analyzing customer documents, customer transactions, customer information. That's PII. GDPR says if you're processing EU customer data, it has to stay in EU. Sending it to a cloud SaaS vendor—even one with data centers in EU—requires data processing agreements, compliance certifications, probably approval from your legal team.

For most financial institutions, this is a non-starter. So I mention it for completeness, but it's probably not viable here."

---

## SLIDE 8: DECISION FRAMEWORK & RECOMMENDATION

**Title:** How to Choose: Decision Tree + Our Recommendation

**Slide Content:**

[Decision tree format - can be text or simple diagram]
START: Do you have GDPR/data residency requirements?
│
├─ YES → Path 2 or Path 1 preferred
│        └─ Do you have 1+ FTE available for 6-8 weeks?
│           ├─ YES → Path 2 (Hybrid) ✓ RECOMMENDED
│           └─ NO → Path 1 (Custom)
│
└─ NO → Path 2 or Path 3
         └─ What's your timeline?
            ├─ < 4 weeks → Path 3
            ├─ 6-12 weeks → Path 2
            └─ 16+ weeks → Path 1

[Bold recommendation]
**Our Recommendation for Wells Fargo: PATH 2 (Hybrid)**

[Rationale bullets]
Rationale:
• GDPR compliance is non-negotiable (data stays on-prem)
• 6-8 week timeline fits business urgency
• 1 FTE engineering capacity is realistic
• Causal inference is InsightFinder's 15-year moat (don't reinvent)
• Lower long-term ops burden (0.5 FTE vs. 1.5-2 FTE)

**Timeline:** 6-8 weeks to full observability
**Cost:** Engineering (1 FTE × 8w) + InsightFinder SaaS (~$X/month)
**Risk:** Low (you control data, InsightFinder controls analysis)

**Speaker Notes:**

"Given your situation—you need GDPR compliance, you have realistic engineering capacity, you need this in the next quarter—Path 2 is the right call.

Here's why:

First, GDPR is non-negotiable. You're processing EU customer data. That has to stay on-prem. Path 3 is off the table.

Second, you don't have 2-3 engineers for 16-20 weeks. You have one or two engineers. Path 1 would crush your capacity.

Third, building causal inference yourself is reinventing the wheel. InsightFinder has spent 15 years on this. They've built it once, and it's proven in production. Why spend four months building something that already exists?

Fourth, the long-term ops burden. Path 1 requires 1.5-2 FTE indefinitely. Path 2 requires 0.5 FTE—just maintaining the ingestion layer. That's a huge difference over five years.

So Path 2: you build the ingestion layer, you integrate with InsightFinder, you get causal inference, you stay GDPR compliant, you ship in six to eight weeks.

That's the recommendation."

---

## SLIDE 9: INSIGHTFINDER COMPONENTS & NEXT STEPS

**Title:** What You Actually Use From InsightFinder + How We Move Forward

**Slide Content:**

[Table: Component | Used in Path 2? | Why]

Core (Causal Inference + Unsupervised Learning) | ✓ Critical | Figures out root cause (data vs. model vs. infrastructure)

Infrastructure Correlation | ✓ Critical | Shows how model behavior correlates with infrastructure changes (unique)

Data Observability | ✓ Optional | Enhances custom data quality checks

Model Monitoring | ✓ Partial | Accuracy tracking, confidence distribution

Alert Routing / Triage | ✓ Nice-to-Have | Automates incident routing to ServiceNow

ARI (Autonomous Remediation) | ✗ No | Too risky for compliance (no autonomous fixes in financial services)

[Bold section]
**What You Own:**
• Python ingestion service (you build and maintain)
• Raw data security/residency

**What InsightFinder Owns:**
• Core (causal inference) ← The hard part
• Infrastructure correlation ← The unique part
• Data observability and alert routing ← The nice-to-haves

[Bold heading]
**Next Steps:**

Let's walk through this together. I'm going to ask you the discovery questions I mentioned earlier. Based on your answers, I'll show you how we get to 'Path 2 is the right call for your situation.'

This demonstrates how discovery shapes recommendations, and shows you what the real conversation would look like.

Ready?

**Speaker Notes:**

"Before we do the interactive walkthrough, let me show you what you're actually getting from InsightFinder in Path 2.

The core—unsupervised learning plus causal inference—that's what you're paying for. That's the thing that's hard to build and that InsightFinder is best-in-class at.

Infrastructure correlation—that's also unique. Most tools don't do this. They monitor infrastructure or they monitor models. InsightFinder shows the relationship between them.

Data observability, model monitoring, alert routing—those are nice-to-haves. You might build some of these yourself, or you might use InsightFinder's versions. Either way.

ARI—autonomous remediation—that's a thing InsightFinder offers. But in a financial services context, you probably don't want automation making changes to production models. Too risky. So you'd leave that off.

So in Path 2: you own the data and the ingestion layer. InsightFinder owns the hard part—figuring out what's actually wrong when your system is broken.

Now I want to show you how this actually works. Let's do a discovery conversation. I'm going to ask you the questions from Slide 3. Based on your answers, we'll walk through the decision logic and show why Path 2 makes sense.

This shows you how we think about the problem and adapt the recommendation to your specific constraints."

---

## SPEAKER NOTES SUMMARY (For Your Reference)

**Slide 1 Opening:** Set context—you've done this before, show the siloed monitoring problem

**Slide 2 Brownfield:** Paint realistic picture of Wells Fargo's current state (Datadog, custom dashboards, incomplete checks, ServiceNow)

**Slide 3 Discovery:** Explain why these seven questions matter and how they shape recommendations

**Slide 4 Paths Overview:** Give executive summary of three approaches, note that Path 2 is "goldilocks"

**Slide 5 Path 1:** Talk about control vs. maintenance burden, when it makes sense

**Slide 6 Path 2:** This is the main one. Emphasize: you get causal inference without building it, GDPR compliant, reasonable timeline

**Slide 7 Path 3:** Acknowledge it exists, explain why GDPR makes it non-viable

**Slide 8 Decision Framework:** Walk through the logic of why Path 2 is recommended for Wells Fargo specifically

**Slide 9 Components:** Show what they're actually paying for, transition to interactive walkthrough

---

## COPY-PASTE INSTRUCTIONS FOR GOOGLE SLIDES

1. Create a new Google Slides presentation
2. For each slide above:
   - Create a new slide
   - Copy the "Slide Content" section into the slide
   - Paste "Speaker Notes" into the speaker notes section (View → Speaker notes)
   - Use formatting guidance (bullets, tables, bold, etc.) from the content
3. Download the presentation theme/design you like
4. Add a title slide at the beginning
5. You're done—ready to present tomorrow

Total setup time: 15-20 minutes

---

## VISUAL DESIGN SUGGESTIONS

**Color scheme:** Professional (blues + grays + white)
**Font:** Sans-serif (Roboto or similar)
**Tables:** Light borders, readable font
**Emphasis:** Use bold for key phrases, not excessive colors
**Diagrams:** Simple, clear (arrows show data flow)

Google Slides default templates will work fine. Don't over-design—focus on clarity.

