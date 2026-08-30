import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import ClientApp from './ClientApp';
import { registerServiceWorker } from './sw-register';
import './styles/tokens.css';

const container = document.getElementById('root');
if (!container) {
  throw new Error('#root missing from client.html — renderer cannot mount');
}

registerServiceWorker();

createRoot(container).render(
  <StrictMode>
    <ClientApp />
  </StrictMode>,
);
