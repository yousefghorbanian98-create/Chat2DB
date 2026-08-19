import { describe, expect, it } from 'vitest';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { ClipperEngine } from '../electron/services/ClipperEngine';
import type { ClipInput, JobProgress } from '../electron/types';

const input: ClipInput = { model:'mock',whisperModel:'tiny',language:'auto',analysisMode:'local',processingProfile:'fast',previewOnly:true,count:1,maxLength:30,category:'Auto',aspect:'9:16',captions:true,smartZoom:false,music:false,blurBackground:true };

function fixture(): { engine: ClipperEngine; sql: string[]; progress: JobProgress[]; root: string } {
  const sql:string[]=[];const progress:JobProgress[]=[];const root=mkdtempSync(path.join(tmpdir(),'violetcut-regression-'));
  const db={prepare:(statement:string)=>({all:()=>[],get:()=>({start_time:0,end_time:30}),run:()=>{sql.push(statement);return{lastInsertRowid:1}}})};
  const emit=(channel:string,value:unknown):void=>{if(channel==='job:progress')progress.push(value as JobProgress)};
  const engine=new ClipperEngine(db as never,{} as never,{} as never,{} as never,{} as never,{} as never,root,undefined,root,emit);
  return{engine,sql,progress,root};
}

describe('pipeline regressions',()=>{
  it('never allows a later engine to move progress backwards',()=>{
    const {engine,progress,root}=fixture();
    const handle=engine.start(input);
    const internal=engine as unknown as {progress:(id:string,phase:string,percent:number,message?:string)=>void};
    internal.progress(handle.jobId,'speaker-diarization',70);
    internal.progress(handle.jobId,'ollama',45);
    expect(progress.slice(-2).map(item=>item.percent)).toEqual([70,70]);
    rmSync(root,{recursive:true,force:true});
  });

  it('whitelists editable database columns',()=>{
    const {engine,sql,root}=fixture();
    engine.update(1,{suggested_title:'safe',...({"status='hacked'":'bad'} as Record<string,string>)});
    const update=sql.find(statement=>statement.startsWith('UPDATE clips SET'))??'';
    expect(update).toContain('suggested_title=?');
    expect(update).not.toContain('hacked');
    rmSync(root,{recursive:true,force:true});
  });
});
