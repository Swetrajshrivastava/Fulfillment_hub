# UI/UX Design Document — Fulfillment Hub

## HARD AESTHETIC RULES
1. NO purple/blue gradients. NO glassmorphism. NO emoji as icons.
2. Use ONLY the palette below. Do not introduce any other colours.
3. Reference vibe: Linear + operational dashboard. Practical, calm, dense, no consumer-brand decoration.

## Design goal
The interface should help a warehouse team make quick decisions without reading large instruction text. The layout should be readable at a glance, prioritize risk, and maintain clarity even under time pressure.

## Colour palette
- Primary: #16324F
- Accent: #E66A2D
- Background: #FFFFFF
- Surface: #F5F7FA
- Text: #1D2430
- Muted: #6B7280
- Success: #1F8A5D
- Error: #C0392B

## Typography
- Headings: Space Grotesk 600
- Body: Inter 400 / 16px / 1.6
- Mono: JetBrains Mono
- Scale: 12 / 14 / 16 / 20 / 28 / 40

## Spacing and structure
- Base unit: 4px
- Allowed spacing values: 4, 8, 12, 16, 24, 32, 48, 64
- Cards: 10px radius
- Buttons: 6px radius
- Inputs: 6px radius
- Shadows: subtle, not decorative

## Layout principles
- Dashboard should lead with urgency: metrics first, exceptions second, workflow detail third
- Tables should be compact and scanable
- Critical statuses should stand out using colour and placement, not noise
- The interface should feel like a control panel, not a consumer app

## Component states
### Button
- Default: filled primary or neutral dark
- Hover: slightly darker contrast
- Active: pressed state
- Disabled: muted grey
- Loading: spinner while preserving label text

### Input
- Default: neutral border
- Focus: accent ring
- Error: red border with helper text
- Disabled: low contrast

### Cards
- Static: subtle surface
- Hover: minimal lift
- Selected: border emphasis without heavy styling

### Status chips
- High priority: warm accent treatment
- Delayed: error tone
- Resolved: green tone
- Pending: neutral grey

## UX rules
- Show the operational problem before the detail
- Use direct labels like “Delayed”, “Needs attention”, and “Awaiting pickup” instead of vague language
- Keep actions single-purpose and obvious for non-technical warehouse users
- Error states should explain the next step, not just the failure

## Example tone
The product should feel trustworthy, efficient, and operationally serious. The user should feel like they are in a control room managing real freight movement—not browsing a general consumer dashboard.
