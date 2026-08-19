import { app } from 'electron';
import { readFile } from 'node:fs/promises';
import type Database from 'better-sqlite3';
import type { AppPaths } from '../utils/paths';
import type { HuggingFaceService } from './HuggingFaceService';
import type { LocalAIService } from './LocalAIService';
import type { OllamaService } from './OllamaService';
import type { SystemService } from './SystemService';
import { redactDiagnosticText } from '../utils/redact';

export class DiagnosticService{
  constructor(private readonly db:Database.Database,private readonly paths:AppPaths,private readonly system:SystemService,private readonly localAI:LocalAIService,private readonly ollama:OllamaService,private readonly huggingFace:HuggingFaceService){}
  async report():Promise<Record<string,unknown>>{
    let logs='';try{logs=await readFile(`${this.paths.logs}/app.log`,'utf8')}catch{/* no log yet */}
    const clipperJobs=this.db.prepare('SELECT status,COUNT(*) count FROM clipper_jobs GROUP BY status').all() as Array<{status:string;count:number}>;
    const uploadJobs=this.db.prepare('SELECT status,COUNT(*) count FROM synced_videos GROUP BY status').all() as Array<{status:string;count:number}>;
    const [hardware,localAI,ollama,huggingFace]=await Promise.all([this.system.profile(),this.localAI.status(),this.ollama.status(),this.huggingFace.state(false)]);
    return{generatedAt:new Date().toISOString(),application:{name:'VioletCut',version:app.getVersion(),packaged:app.isPackaged},runtime:{electron:process.versions.electron,node:process.versions.node,chrome:process.versions.chrome},hardware,engines:{localAI,ollama:{running:ollama.running,models:ollama.models,error:ollama.error},professionalModels:{configured:huggingFace.configured}},jobs:{clipping:clipperJobs,uploads:uploadJobs},recentLogs:redactDiagnosticText(logs.split(/\r?\n/).slice(-250).join('\n'),this.paths)};
  }
}
