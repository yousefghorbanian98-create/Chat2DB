/**
 * مجموعه‌ی آیکونِ داخلی — بدون وابستگیِ خارجی.
 *
 * چرا؟ رابط پیش از این هیچ آیکونی نداشت و همه چیز با متن بود؛ این باعث
 * می‌شد سلسله‌مراتبِ بصری شکل نگیرد. آیکون‌ها فقط با currentColor رنگ
 * می‌گیرند تا قاعده‌ی «رنگ فقط از توکن» (FE-4-G1) نشکند.
 *
 * همه روی شبکه‌ی ۲۴ واحدی با قلمِ ۱٫۶ ترسیم شده‌اند تا وزنِ بصری یکسان
 * بماند (قلمِ ظریف هم‌راستا با «بدون سایه، خطِ مویی» در DESIGN.md).
 */

export type IconName =
  | 'send'
  | 'sparkles'
  | 'plus'
  | 'sun'
  | 'moon'
  | 'message'
  | 'terminal'
  | 'copy'
  | 'check'
  | 'alert'
  | 'plug'
  | 'wrench'
  | 'close'
  | 'chevron'
  | 'search'
  | 'stack'
  | 'clock'
  | 'download'

const PATHS: Record<IconName, JSX.Element> = {
  send: (
    <>
      <path d="M4.5 12h14" />
      <path d="M12.5 5.5 19 12l-6.5 6.5" />
    </>
  ),
  sparkles: (
    <>
      <path d="M12 3.5 13.6 8.4 18.5 10 13.6 11.6 12 16.5 10.4 11.6 5.5 10 10.4 8.4Z" />
      <path d="M18.5 16.5 19.2 18.4 21 19.1 19.2 19.8 18.5 21.7 17.8 19.8 16 19.1 17.8 18.4Z" />
    </>
  ),
  plus: (
    <>
      <path d="M12 5.5v13" />
      <path d="M5.5 12h13" />
    </>
  ),
  sun: (
    <>
      <circle cx="12" cy="12" r="4" />
      <path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6 7 7M17 17l1.4 1.4M18.4 5.6 17 7M7 17l-1.4 1.4" />
    </>
  ),
  moon: <path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a7 7 0 1 0 10.5 10.5Z" />,
  message: <path d="M4.5 6.5h15v9h-8l-4.5 3.5v-3.5h-2.5Z" />,
  terminal: (
    <>
      <rect x="3.5" y="4.5" width="17" height="15" rx="2" />
      <path d="M7.5 9.5 10 12l-2.5 2.5M12.5 15h4" />
    </>
  ),
  copy: (
    <>
      <rect x="9" y="9" width="11" height="11" rx="2" />
      <path d="M15 6.5V6a1.5 1.5 0 0 0-1.5-1.5H6A1.5 1.5 0 0 0 4.5 6v7.5A1.5 1.5 0 0 0 6 15h.5" />
    </>
  ),
  check: <path d="M5 12.5 9.5 17 19 7.5" />,
  alert: (
    <>
      <path d="M12 4.5 21 19.5H3Z" />
      <path d="M12 10v4.5M12 17h.01" />
    </>
  ),
  plug: (
    <>
      <path d="M9 3.5v5M15 3.5v5" />
      <path d="M6.5 8.5h11v3a5.5 5.5 0 0 1-11 0Z" />
      <path d="M12 17v3.5" />
    </>
  ),
  wrench: (
    <path d="M15.5 3.5a5 5 0 0 0-4.3 7.5L4.8 17.4a2 2 0 0 0 2.8 2.8l6.4-6.4a5 5 0 0 0 6.5-6.9l-3 3-2.5-2.5 3-3a5 5 0 0 0-2.5-.9Z" />
  ),
  close: (
    <>
      <path d="M6 6l12 12" />
      <path d="M18 6 6 18" />
    </>
  ),
  chevron: <path d="M14.5 8.5 10 12l4.5 3.5" />,
  search: (
    <>
      <circle cx="11" cy="11" r="6" />
      <path d="M15.5 15.5 20 20" />
    </>
  ),
  stack: (
    <>
      <path d="M12 3.5 20.5 8 12 12.5 3.5 8Z" />
      <path d="M3.5 12.5 12 17l8.5-4.5" />
    </>
  ),
  clock: (
    <>
      <circle cx="12" cy="12" r="8" />
      <path d="M12 7.5V12l3 2" />
    </>
  ),
  download: (
    <>
      <path d="M12 4v10" />
      <path d="M8 10.5 12 14.5 16 10.5" />
      <path d="M5 18.5h14" />
    </>
  ),
}

interface Props {
  name: IconName
  size?: number
  className?: string
}

export default function Icon({ name, size = 16, className = '' }: Props) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.6}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
      focusable="false"
    >
      {PATHS[name]}
    </svg>
  )
}
