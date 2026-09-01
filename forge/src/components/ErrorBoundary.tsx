import { Component, type ErrorInfo, type ReactNode } from 'react'
import Icon from './Icon.tsx'

interface Props {
  children: ReactNode
}

interface State {
  error: Error | null
}

/**
 * چرا لازم است؟ بدونِ آن، یک خطای زمانِ اجرا در هر کامپوننتی کلِ پنجره را
 * سفید می‌کند و کاربرِ برنامه‌ی دسکتاپ نمی‌فهمد چه شده. اینجا خطا دیده
 * می‌شود و راهِ برگشت نشان داده می‌شود.
 */
export default class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null }

  static getDerivedStateFromError(error: Error): State {
    return { error }
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    console.error('[forge] خطای رابط:', error, info.componentStack)
  }

  render(): ReactNode {
    const { error } = this.state
    if (!error) return this.props.children

    return (
      <div className="flex h-full items-center justify-center p-8">
        <div className="w-full max-w-md rounded-card border border-hairline bg-canvas-soft p-6 text-center">
          <span className="mx-auto flex size-11 items-center justify-center rounded-card border border-hairline bg-surface text-error">
            <Icon name="alert" size={20} />
          </span>
          <h2 className="mt-4 text-title-md text-ink">مشکلی پیش آمد</h2>
          <p className="mt-2 text-body-sm leading-relaxed text-muted">
            بخشی از رابط نتوانست نمایش داده شود. داده‌های شما (نشست‌ها) روی دیسک
            مانده‌اند و با بارگذاریِ دوباره برمی‌گردند.
          </p>
          <pre
            dir="ltr"
            className="mt-4 overflow-x-auto rounded-md border border-hairline bg-canvas p-3 text-left text-code text-muted"
          >
            {error.message}
          </pre>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 w-full rounded-lg px-4 py-2.5 text-button text-ink transition-opacity hover:opacity-90"
            style={{ backgroundColor: 'var(--color-brand)' }}
          >
            بارگذاریِ دوباره
          </button>
        </div>
      </div>
    )
  }
}
