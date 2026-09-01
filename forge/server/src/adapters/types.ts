import type { AdapterStatus } from '../types'

/**
 * قرارداد مشترک همهٔ Adapterها.
 * قانون: health() هرگز پرتاب نمی‌کند. نبودِ وابستگی = missing، نه crash.
 */
export interface Adapter {
  readonly name: string
  health(): Promise<AdapterStatus>
}
