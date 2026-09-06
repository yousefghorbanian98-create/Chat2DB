# Page override — Kiosk Check-in

## One job
Scan membership QR → show success/deny → return to idle.

## Layout
- Centered scanner frame with emerald corners
- Live count: “N members training now”
- Huge success/deny state (color + icon + text, not color alone)
- Auto-reset to idle after 4s
- Hidden admin exit: long-press logo + PIN

## Deny reasons (member-visible, short)
- Membership expired
- Account inactive
- Invalid / forged QR signature
- Already checked in (optional policy)

## Do not
- No access to member list, finance, or settings chrome
- No AI
- No screenshots of other PII on success beyond first name + member code
