export type MotionPackageId = 'cosmos' | 'hyper';

export interface MotionPackageInfo {
  id: MotionPackageId;
  label: string;
  tagline: string;
  description: string;
  swatches: string[];
  /** CSS custom properties applied to :root when this package is active */
  cssVars: Record<string, string>;
}

export const MOTION_PACKAGE_STORAGE_KEY = 'chat2db.motionPackage';

export const MOTION_PACKAGES: Record<MotionPackageId, MotionPackageInfo> = {
  cosmos: {
    id: 'cosmos',
    label: 'Data Cosmos',
    tagline: 'cinematic · deep space',
    description: 'setting.motionPackage.cosmosDesc',
    swatches: ['#0a2a5e', '#1e1b4b', '#312e81', '#60a5fa'],
    cssVars: {
      '--mp-accent': '#3b82f6',
      '--mp-accent-2': '#8b5cf6',
      '--mp-glow': 'rgba(59, 130, 246, 0.55)',
      '--mp-bg': '#05070d',
    },
  },
  hyper: {
    id: 'hyper',
    label: 'Hyperreal',
    tagline: 'luxury · neon glass',
    description: 'setting.motionPackage.hyperDesc',
    swatches: ['#3b0764', '#7c2d12', '#0f172a', '#a78bfa'],
    cssVars: {
      '--mp-accent': '#a78bfa',
      '--mp-accent-2': '#f97316',
      '--mp-glow': 'rgba(167, 139, 250, 0.55)',
      '--mp-bg': '#0a0714',
    },
  },
};

export const MOTION_PACKAGE_IDS = Object.keys(MOTION_PACKAGES) as MotionPackageId[];

export function isMotionPackageId(value: unknown): value is MotionPackageId {
  return value === 'cosmos' || value === 'hyper';
}
