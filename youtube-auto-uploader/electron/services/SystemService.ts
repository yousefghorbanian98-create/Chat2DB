import { execFile } from 'node:child_process';
import { readdir, stat, statfs } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import type { AppPaths } from '../utils/paths';
import { sweepDirectory } from '../utils/cleanup';

export interface SystemProfile {
  os: string; cpu: string; logicalCores: number; totalMemory: number; freeMemory: number;
  gpu?: string; gpuMemory?: number; cudaAvailable: boolean;
  diskTotal: number; diskFree: number; modelBytes: number; temporaryBytes: number;
  recommendedProfile: 'fast'|'balanced'|'professional';
}

async function directorySize(directory:string):Promise<number>{let total=0;let entries;try{entries=await readdir(directory,{withFileTypes:true})}catch{return 0}for(const entry of entries){const target=path.join(directory,entry.name);try{if(entry.isDirectory())total+=await directorySize(target);else total+=(await stat(target)).size}catch{/* file changed during scan */}}return total}
function command(file:string,args:string[]):Promise<string>{return new Promise((resolve,reject)=>execFile(file,args,{windowsHide:true,timeout:8_000},(error,stdout)=>error?reject(error):resolve(stdout.trim())))}

export class SystemService {
  constructor(private readonly paths:AppPaths){}
  async profile():Promise<SystemProfile>{
    let gpu:string|undefined;let gpuMemory:number|undefined;
    try{const output=await command('nvidia-smi',['--query-gpu=name,memory.total','--format=csv,noheader,nounits']);const [name,memory]=output.split('\n')[0]?.split(',').map(value=>value.trim())??[];gpu=name;gpuMemory=Number(memory)*1_048_576}catch{/* NVIDIA is optional */}
    const disk=await statfs(this.paths.root);const diskTotal=Number(disk.blocks)*Number(disk.bsize);const diskFree=Number(disk.bavail)*Number(disk.bsize);
    const [modelBytes,temporaryBytes]=await Promise.all([directorySize(path.join(this.paths.cache,'local-ai','models')),directorySize(this.paths.temp)]);
    const totalMemory=os.totalmem();const professional=Boolean(gpuMemory&&gpuMemory>=8*1024**3&&totalMemory>=16*1024**3);
    const balanced=Boolean((gpuMemory&&gpuMemory>=4*1024**3)||totalMemory>=12*1024**3);
    return{os:`${os.type()} ${os.release()}`,cpu:os.cpus()[0]?.model??'Unknown CPU',logicalCores:os.cpus().length,totalMemory,freeMemory:os.freemem(),gpu,gpuMemory,cudaAvailable:Boolean(gpu),diskTotal,diskFree,modelBytes,temporaryBytes,recommendedProfile:professional?'professional':balanced?'balanced':'fast'};
  }
  async cleanup():Promise<{removed:number;temporaryBytes:number}>{const removed=await sweepDirectory(this.paths.temp,60*60*1000);return{removed,temporaryBytes:await directorySize(this.paths.temp)}}
}
