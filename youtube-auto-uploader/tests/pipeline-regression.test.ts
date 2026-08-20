import { describe, expect, it } from 'vitest';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { associateSpeakersWithFaces, ClipperEngine, multimodalMetadata } from '../electron/services/ClipperEngine';
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
  it('explains multimodal highlight scores from active signals',()=>{
    const result=multimodalMetadata({id:'h1',start_seconds:0,end_seconds:20,score:80,title:'Moment',transcript:'A complete useful moment',caption_path:'x.ass'},'Auto',{scenes:[4,9],silences:[],audioPeaks:[{time:5,score:.9}]},{trackCount:1,samples:[{track_id:1,time_seconds:5,x:.2,y:.2,width:.3,height:.3,confidence:.9,mouth_activity:.8}]},[{time:6,text:'wow amazing',sentiment:1}]);
    expect(result.finalScore).toBeGreaterThan(5);expect(result.reason).toContain('Multimodal:');expect(result.reason).toContain('Hook');
  });
  it('keeps recurring speakers associated with stable face tracks',()=>{
    const result=associateSpeakersWithFaces({speakers:['A','B'],turns:[{speaker:'A',start_seconds:0,end_seconds:2},{speaker:'B',start_seconds:2,end_seconds:4},{speaker:'A',start_seconds:4,end_seconds:6}]},{trackCount:2,samples:[{track_id:1,time_seconds:1,x:.1,y:.1,width:.3,height:.3,confidence:.9},{track_id:2,time_seconds:1,x:.6,y:.1,width:.2,height:.2,confidence:.9},{track_id:2,time_seconds:3,x:.6,y:.1,width:.3,height:.3,confidence:.9},{track_id:1,time_seconds:5,x:.1,y:.1,width:.3,height:.3,confidence:.9}]});
    expect(result.map(item=>item.track_id)).toEqual([1,2,1]);
  });
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
