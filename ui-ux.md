# UI/UX Design Document — Fulfillment Hub

## HARD AESTHETIC RULES
1. NO purple/blue gradients. NO glassmorphism. NO emoji as icons.
2. Use ONLY the palette below. Do not introduce a colour not listed.
3. Reference vibe: Linear + operational SaaS. Match density and restraint, not a marketing landing page.

## Visual direction
The product should feel calm, dense, and operational. It should help users make decisions quickly without distraction. The interface must prioritize clarity, hierarchy, and actionability over decorative visuals.

## Core design system
### Colour palette
- Primary: #16324F
- Accent: #E66A2D
- Background: #FFFFFF
- Surface: #F5F7FA
- Text: #1D2430
- Muted: #6B7280

### Typography
- Headings: Space Grotesk 600
- Body: Inter 400/16px/1.6
- Monospace: JetBrains Mono
- Type scale: 12 / 14 / 16 / 20 / 28 / 40

### Spacing scale
- Base unit: 4px
- Allowed values: 4, 8, 12, 16, 24, 32, 48, 64
- No arbitrary spacing values beyond this system

### Radius and shadows
- Buttons: 6px
- Cards: 10px
- Inputs: 6px
- Avatars: full round
- Shadow: subtle card elevation only, not heavy overlays

## Layout philosophy
- Dashboard must focus on the operational question: What requires attention now?
- Use dense information display with consistent table layouts and status chips
- Prioritize scanability over storytelling
- Important issues should be visible without extra clicks

## Component states
### Button
- Default: filled accent or neutral dark
- Hover: slightly darker / stronger contrast
- Active: pressed state with minimal motion
- Disabled: low-contrast grey with no pointer affordance
- Loading: spinner with text preserved

### Input
- Default: standard border
- Focus: 2px accent ring
- Error: red border with message below field
- Disabled: muted background and grey text

### Card
- Static: quiet surface
- Hover: subtle lift with 150ms ease
- Selected: border or accent treatment without heavy emphasis

### Status chips
- High priority: accent flush / darker orange treatment
- Delayed: warm error tone
- Resolved: green/neutral success treatment
- Pending: muted neutral tone

## Dashboard structure
- Top row: 4 operational KPIs
- Middle row: risk list and status chart
- Lower row: operational exception table and active queue
- Tables should be dense, readable, and sortable
- Use filters for priority, status, and customer/order search

## UX rules
- Show the problem before the detail
- Present a single action for each major workflow
- Reduce user ambiguity with targeted status labels
- Use microcopy that is operational and precise, not playful
- Error states should explain the next step, not just the failure

## Example page tone
The app should feel like a modern operations tool: structured, calm, direct, and trustworthy. It should never feel like a consumer product or a marketing landing page.
