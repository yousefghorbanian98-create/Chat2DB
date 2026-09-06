import { useEffect, useState } from 'react';
import QRCode from 'qrcode';

import { MotionButton } from '../../components/MotionButton';
import { useCheckinQr } from '../../hooks/useCheckinQr';
import { cardSection, cardTitle, muted, noteSmall } from '../../styles/blocks';

const FRAME: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  gap: 'var(--space-md)',
  padding: 'var(--space-lg)',
};
const QR_IMG: React.CSSProperties = {
  width: 208,
  height: 208,
  borderRadius: 'var(--radius-md)',
  background: '#fff',
  padding: 10,
};

/** The glass frame every athlete card shares. */
function Card({ children }: { children: React.ReactNode }) {
  return (
    <section className="glass" style={cardSection} data-testid="client-checkin">
      <h3 style={cardTitle}>ورود به باشگاه</h3>
      {children}
    </section>
  );
}

/** Rasterise the signed payload locally; jsdom has no canvas, so this can fail. */
function useQrImage(payload: string | null) {
  const [dataUrl, setDataUrl] = useState<string | null>(null);
  const [renderError, setRenderError] = useState<string | null>(null);

  useEffect(() => {
    if (payload === null) return;
    let alive = true;
    void QRCode.toDataURL(payload, { width: 416, margin: 1, errorCorrectionLevel: 'M' })
      .then((url) => {
        if (alive) {
          setDataUrl(url);
          setRenderError(null);
        }
      })
      .catch(() => {
        if (alive) setRenderError('ساخت تصویر کد ناموفق بود');
      });
    return () => {
      alive = false;
    };
  }, [payload]);

  return { dataUrl, renderError };
}

/** The rendered symbol plus its countdown, once both are ready. */
function QrPanel({
  dataUrl,
  secondsLeft,
  onRefresh,
}: {
  dataUrl: string;
  secondsLeft: number;
  onRefresh: () => void;
}) {
  return (
    <div style={FRAME}>
      <img src={dataUrl} alt="کد QR ورود به باشگاه" style={QR_IMG} data-testid="checkin-qr-img" />
      <p className="numeric" style={noteSmall} data-testid="checkin-countdown">
        اعتبار تا {secondsLeft} ثانیهٔ دیگر
      </p>
      <p style={muted}>این کد را جلوی دستگاه ورود نشان دهید.</p>
      <MotionButton variant="ghost" onClick={onRefresh}>
        کد جدید
      </MotionButton>
    </div>
  );
}

/**
 * Self check-in: a signed 60-second code the athlete holds up at the kiosk.
 *
 * The symbol is rendered locally from the server-signed payload, so no image
 * ever leaves the phone and the code cannot be forged without the core's key.
 */
export function CheckinQrCard({ active }: { active: boolean }) {
  const { payload, secondsLeft, error, refresh } = useCheckinQr(active);
  const { dataUrl, renderError } = useQrImage(payload);

  if (error !== null) {
    return (
      <Card>
        <div role="alert">
          <p style={{ color: 'var(--color-destructive)' }}>{error}</p>
          <MotionButton onClick={refresh}>تلاش دوباره</MotionButton>
        </div>
      </Card>
    );
  }

  if (renderError !== null) {
    return (
      <Card>
        <p role="alert" style={{ color: 'var(--color-destructive)' }}>
          {renderError}
        </p>
      </Card>
    );
  }

  return (
    <Card>
      {payload === null || dataUrl === null ? (
        <p style={muted}>در حال ساخت کد ورود…</p>
      ) : (
        <QrPanel dataUrl={dataUrl} secondsLeft={secondsLeft} onRefresh={refresh} />
      )}
    </Card>
  );
}

export default CheckinQrCard;
