import i18n from '@/i18n';
import { CheckCircle2 } from 'lucide-react';
import { MOTION_PACKAGE_IDS, MOTION_PACKAGES } from './types';
import { useMotionPackage } from './MotionPackageProvider';

/**
 * Settings section: one-tap switch between the motion experience packages
 * (Data Cosmos / Hyperreal). Applied instantly and persisted automatically.
 */
const PACKAGE_LABEL_KEYS: Record<string, 'setting.motionPackage.cosmosLabel' | 'setting.motionPackage.hyperLabel'> = {
  cosmos: 'setting.motionPackage.cosmosLabel',
  hyper: 'setting.motionPackage.hyperLabel',
};

export default function MotionPackageSetting() {
  const { motionPackage, setMotionPackage } = useMotionPackage();

  return (
    <div className="motion-package-setting">
      <h3 className="motion-package-heading">{i18n('setting.motionPackage.title')}</h3>
      <p className="motion-package-sub">{i18n('setting.motionPackage.sub')}</p>

      <div className="motion-package-cards">
        {MOTION_PACKAGE_IDS.map((id) => {
          const pkg = MOTION_PACKAGES[id];
          const active = motionPackage === id;
          return (
            <button
              key={id}
              type="button"
              className={`motion-package-card${active ? ' active' : ''}`}
              data-package={id}
              onClick={() => setMotionPackage(id)}
            >
              <div className="motion-package-swatches">
                {pkg.swatches.map((color) => (
                  <span key={color} className="motion-package-swatch" style={{ background: color }} />
                ))}
              </div>
              <div className="motion-package-card-title">
                <b>{i18n(PACKAGE_LABEL_KEYS[id])}</b>
                <span className="motion-package-tagline">{pkg.tagline}</span>
              </div>
              <p className="motion-package-desc">{i18n(pkg.description as never)}</p>
              <span className="motion-package-state">
                {active ? (
                  <>
                    <CheckCircle2 size={13} /> {i18n('setting.motionPackage.active')}
                  </>
                ) : (
                  i18n('setting.motionPackage.tapToSwitch')
                )}
              </span>
            </button>
          );
        })}
      </div>

      <p className="motion-package-note">{i18n('setting.motionPackage.saved')}</p>
    </div>
  );
}
