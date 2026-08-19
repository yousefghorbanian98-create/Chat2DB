import { app } from 'electron';
import { autoUpdater, type UpdateInfo } from 'electron-updater';
import { copyFile, mkdir } from 'node:fs/promises';
import path from 'node:path';

export interface UpdateState {status:'idle'|'checking'|'available'|'not-available'|'downloading'|'downloaded'|'error';currentVersion:string;availableVersion?:string;percent?:number;transferred?:number;total?:number;message?:string;canAutoInstall:boolean}

export class UpdateService{
  private stateValue:UpdateState;
  constructor(private readonly database:string,private readonly backupDirectory:string,private readonly emit:(channel:string,value:unknown)=>void){
    const portable=Boolean(process.env.PORTABLE_EXECUTABLE_FILE);this.stateValue={status:'idle',currentVersion:app.getVersion(),canAutoInstall:app.isPackaged&&!portable};
    autoUpdater.autoDownload=false;autoUpdater.autoInstallOnAppQuit=false;autoUpdater.allowPrerelease=false;
    autoUpdater.on('checking-for-update',()=>this.set({status:'checking'}));
    autoUpdater.on('update-available',(info:UpdateInfo)=>this.set({status:'available',availableVersion:info.version}));
    autoUpdater.on('update-not-available',()=>this.set({status:'not-available'}));
    autoUpdater.on('download-progress',(progress)=>this.set({status:'downloading',percent:progress.percent,transferred:progress.transferred,total:progress.total}));
    autoUpdater.on('update-downloaded',(info:UpdateInfo)=>this.set({status:'downloaded',availableVersion:info.version,percent:100}));
    autoUpdater.on('error',(error)=>this.set({status:'error',message:error.message.replace(/https?:\/\/\S+/g,'[update source]')}));
  }
  private set(patch:Partial<UpdateState>):void{this.stateValue={...this.stateValue,...patch,currentVersion:app.getVersion()};this.emit('update:state',this.stateValue)}
  state():UpdateState{return this.stateValue}
  async check():Promise<UpdateState>{if(!app.isPackaged){this.set({status:'not-available',message:'Update checks run in installed builds'});return this.stateValue}this.set({status:'checking',message:undefined});await autoUpdater.checkForUpdates();return this.stateValue}
  async download():Promise<UpdateState>{if(!this.stateValue.canAutoInstall)throw new Error('Automatic installation is available in the installed version only');this.set({status:'downloading',percent:0});await autoUpdater.downloadUpdate();return this.stateValue}
  private async backup():Promise<void>{await mkdir(this.backupDirectory,{recursive:true});const stamp=new Date().toISOString().replace(/[:.]/g,'-');for(const suffix of ['','-wal','-shm']){try{await copyFile(`${this.database}${suffix}`,path.join(this.backupDirectory,`app-${stamp}.db${suffix}`))}catch{/* optional SQLite sidecar may not exist */}}}
  async install():Promise<void>{if(this.stateValue.status!=='downloaded')throw new Error('Download the update before installing');await this.backup();setImmediate(()=>autoUpdater.quitAndInstall(false,true))}
  scheduleInitialCheck():void{if(app.isPackaged)setTimeout(()=>{void this.check().catch(()=>undefined)},15_000)}
}
