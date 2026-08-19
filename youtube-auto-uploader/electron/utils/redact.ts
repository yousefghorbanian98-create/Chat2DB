import os from 'node:os';
import type { AppPaths } from './paths';

export function redactDiagnosticText(value:string,paths:AppPaths):string{return value
  .replace(/hf_[A-Za-z0-9]+/g,'[REDACTED_TOKEN]')
  .replace(/(access_token|refresh_token|client_secret)["'=:\s]+[^\s,"'}]+/gi,'$1=[REDACTED]')
  .replaceAll(paths.root,'%APP_DATA%').replaceAll(os.homedir(),'%HOME%')
  .replace(/https?:\/\/[^\s"']+/g,'[REDACTED_URL]')}
