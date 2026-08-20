import { spawn } from 'node:child_process';
import path from 'node:path';
import { binaryPath } from '../bin';

export interface MediaAnalysis {
  scenes: number[];
  silences: Array<{ start: number; end: number }>;
  audioPeaks: Array<{ time: number; score: number }>;
}

export interface RenderOptions {
  aspect: string;
  captionsPath?: string;
  fontsDirectory?: string;
  smartZoom: boolean;
  blurBackground: boolean;
  musicPath?: string;
  musicVolume?: number;
  encoder?: 'h264_nvenc' | 'libx264';
  sourceStart?: number;
  faceSamples?: Array<{ track_id: number; time_seconds: number; x: number; width: number }>;
  activeFaces?: Array<{start_seconds:number;end_seconds:number;track_id:number|null;confidence:number}>;
  audioMuteRanges?: Array<{start:number;end:number}>;
  broll?: {at:number;duration:number;sourceStart:number};
  multiFaceTrackIds?: number[];
  jobId?: string;
}

function subtitlePath(file: string): string {
  return file.replaceAll('\\', '/').replace(/^([A-Za-z]):/, '$1\\:').replaceAll("'", "\\'");
}

function dynamicFaceCrop(samples: NonNullable<RenderOptions['faceSamples']>, start: number, duration: number, activeFaces:RenderOptions['activeFaces']): string | undefined {
  const segments=(activeFaces??[]).filter(item=>item.track_id!==null&&item.end_seconds>=start&&item.start_seconds<=start+duration);
  const inRange=samples.filter((sample)=>sample.time_seconds>=start&&sample.time_seconds<=start+duration);
  const switched=inRange.filter(sample=>{const active=segments.filter(item=>sample.time_seconds>=item.start_seconds&&sample.time_seconds<=item.end_seconds).sort((a,b)=>b.confidence-a.confidence)[0];return !active||active.track_id===sample.track_id});
  const relevant=switched.length?switched:inRange;
  if (!relevant.length) return undefined;
  const counts = new Map<number, number>();
  for (const sample of relevant) counts.set(sample.track_id, (counts.get(sample.track_id) ?? 0) + 1);
  const primary = [...counts].sort((left, right) => right[1] - left[1])[0]?.[0];
  const selected=segments.length?relevant:relevant.filter((sample)=>sample.track_id===primary);
  const track = selected.filter((_, index) => index % 4 === 0).slice(0, 60);
  if (!track.length) return undefined;
  const position = (sample: typeof track[number]): string => `max(0\\,min(iw-ih*9/16\\,${String(Math.max(0, Math.min(1, sample.x + sample.width / 2)))}*iw-ih*9/32))`;
  let expression = position(track.at(-1) as typeof track[number]);
  for (let index = track.length - 2; index >= 0; index--) {
    const sample = track[index];
    if (!sample) continue;
    const relative = Math.max(0, sample.time_seconds - start + 0.3);
    expression = `if(lt(t\\,${relative.toFixed(3)})\\,${position(sample)}\\,${expression})`;
  }
  return expression;
}

function multiFaceFilter(samples:NonNullable<RenderOptions['faceSamples']>,ids:number[],width:number,height:number):string|undefined{
  const selected=[...new Set(ids)].slice(0,3);if(selected.length<2)return undefined;
  const center=(id:number):number|undefined=>{const track=samples.filter(sample=>sample.track_id===id);if(!track.length)return undefined;return track.reduce((sum,item)=>sum+item.x+item.width/2,0)/track.length};
  const centers=selected.map(center);if(centers.some(value=>value===undefined))return undefined;
  const crop=(label:string,c:number,out:string,w:number,h:number,ratio:string)=>`[${label}]crop=w='min(iw\\,ih*${ratio})':h='min(ih\\,iw/${ratio})':x='max(0\\,min(iw-ow\\,${c.toFixed(5)}*iw-ow/2))':y='max(0\\,(ih-oh)/2)',scale=${w}:${h}[${out}]`;
  if(selected.length===2){return `[0:v]split=3[first][second][bg];[bg]scale=${width}:${height}:force_original_aspect_ratio=increase,crop=${width}:${height},boxblur=24:1[base];${crop('first',centers[0] as number,'top',width,Math.floor(height/2),'9/8')};${crop('second',centers[1] as number,'bottom',width,Math.floor(height/2),'9/8')};[base][top]overlay=0:0[half];[half][bottom]overlay=0:${Math.floor(height/2)}[composite]`}
  const half=Math.floor(width/2),bottomHeight=Math.floor(height/2);
  return `[0:v]split=4[first][second][third][bg];[bg]scale=${width}:${height}:force_original_aspect_ratio=increase,crop=${width}:${height},boxblur=24:1[base];${crop('first',centers[0] as number,'top',width,bottomHeight,'9/8')};${crop('second',centers[1] as number,'left',half,bottomHeight,'9/16')};${crop('third',centers[2] as number,'right',half,bottomHeight,'9/16')};[base][top]overlay=0:0[topmix];[topmix][left]overlay=0:${bottomHeight}[leftmix];[leftmix][right]overlay=${half}:${bottomHeight}[composite]`;
}

export class FFmpegService {
  private encoderCheck?: Promise<'h264_nvenc' | 'libx264'>;
  private readonly processes=new Map<string,ReturnType<typeof spawn>>();
  private readonly cancelled=new Set<string>();

  private capture(command: string, args: string[]): Promise<string> {
    return new Promise((resolve, reject) => {
      const child = spawn(command, args, { windowsHide: true });
      let output = '';
      child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8');
      child.stdout.on('data', (value: string) => { output += value; });
      child.stderr.on('data', (value: string) => { output += value; });
      child.once('error', reject);
      child.once('close', (code) => code === 0 ? resolve(output) : reject(new Error(`${command} exited with code ${String(code)}`)));
    });
  }

  cancel(jobId:string):boolean{this.cancelled.add(jobId);const child=this.processes.get(jobId);if(!child)return false;const stopped=child.kill();this.processes.delete(jobId);return stopped}

  preferredEncoder(): Promise<'h264_nvenc' | 'libx264'> {
    this.encoderCheck ??= Promise.all([
      this.capture('nvidia-smi', ['--query-gpu=name', '--format=csv,noheader']),
      this.capture(binaryPath('ffmpeg'), ['-hide_banner', '-encoders'])
    ]).then(([, encoders]) => encoders.includes('h264_nvenc') ? 'h264_nvenc' as const : 'libx264' as const)
      .catch(() => 'libx264' as const);
    return this.encoderCheck;
  }

  async run(args: string[], onLine?: (line: string) => void,jobId?:string): Promise<void> {
    await new Promise<void>((resolve, reject) => {
      const child = spawn(binaryPath('ffmpeg'), ['-hide_banner', '-y', ...args], { windowsHide: true });
      if(jobId)this.processes.set(jobId,child);
      child.stderr.setEncoding('utf8');
      child.stderr.on('data', (value: string) => onLine?.(value));
      child.once('error',error=>{if(jobId)this.processes.delete(jobId);reject(error)});
      child.once('close',(code)=>{if(jobId)this.processes.delete(jobId);if(code===0)resolve();else reject(new Error(`ffmpeg exited with code ${String(code)}`))});
    });
  }

  async probe(file: string): Promise<{ duration: number; width: number; height: number }> {
    return await new Promise((resolve, reject) => {
      const child = spawn(binaryPath('ffprobe'), ['-v', 'error', '-show_entries', 'format=duration:stream=width,height', '-of', 'json', file], { windowsHide: true });
      let output = '';
      child.stdout.on('data', (chunk) => { output += String(chunk); });
      child.once('error', reject);
      child.once('close', (code) => {
        if (code !== 0) { reject(new Error('ffprobe failed')); return; }
        const data = JSON.parse(output) as { format: { duration: string }; streams: Array<{ width?: number; height?: number }> };
        resolve({ duration: Number(data.format.duration), width: data.streams[0]?.width ?? 0, height: data.streams[0]?.height ?? 0 });
      });
    });
  }

  async analyze(file: string): Promise<MediaAnalysis> {
    let log = '';
    await this.run(['-i', file, '-vf', "select='gt(scene,0.35)',showinfo", '-an', '-f', 'null', '-'], (line) => { log += line; });
    try {
      await this.run(['-i', file, '-vn', '-af', 'silencedetect=n=-30dB:d=0.8,astats=metadata=1:reset=1,ametadata=print', '-f', 'null', '-'], (line) => { log += line; });
    } catch { /* A silent video still has useful scene analysis. */ }
    const scenes = [...log.matchAll(/showinfo[^\n]*pts_time:([\d.]+)/g)].map((match) => Number(match[1])).filter(Number.isFinite);
    const starts = [...log.matchAll(/silence_start:\s*([\d.]+)/g)].map((match) => Number(match[1]));
    const ends = [...log.matchAll(/silence_end:\s*([\d.]+)/g)].map((match) => Number(match[1]));
    const silences = starts.map((start, index) => ({ start, end: ends[index] ?? start + 0.8 }));
    const times = [...log.matchAll(/pts_time:([\d.]+)/g)].map((match) => Number(match[1]));
    const rms = [...log.matchAll(/lavfi\.astats\.Overall\.RMS_level=([-\d.]+)/g)].map((match) => Number(match[1]));
    const audioPeaks = rms.map((level, index) => ({ time: times[index] ?? index, score: Math.max(0, Math.min(1, (level + 45) / 45)) }));
    return { scenes: [...new Set(scenes)].sort((a, b) => a - b), silences, audioPeaks };
  }

  async render(source: string, start: number, end: number, output: string, options: RenderOptions): Promise<void> {
    const duration = Math.max(1, end - start);
    const square = options.aspect === '1:1';
    const landscape = options.aspect === '16:9';
    const width = landscape ? 1920 : 1080;
    const height = square ? 1080 : landscape ? 1080 : 1920;
    const foregroundWidth = landscape ? 1920 : square ? 1080 : 900;
    const splitLayout=!landscape&&!square&&options.faceSamples&&options.multiFaceTrackIds?multiFaceFilter(options.faceSamples,options.multiFaceTrackIds,width,height):undefined;
    const faceCrop = !splitLayout&&!landscape && !square && options.faceSamples ? dynamicFaceCrop(options.faceSamples, options.sourceStart ?? start, duration, options.activeFaces) : undefined;
    const background = splitLayout??(faceCrop
      ? `[0:v]crop=w='ih*9/16':h='ih':x='${faceCrop}':y=0,scale=${String(width)}:${String(height)}[composite]`
      : options.blurBackground
        ? `[0:v]split[orig][bg];[bg]scale=${String(width)}:${String(height)}:force_original_aspect_ratio=increase,crop=${String(width)}:${String(height)},boxblur=20:1[base];[orig]scale=${String(foregroundWidth)}:-2[fg];[base][fg]overlay=(W-w)/2:(H-h)/2[composite]`
        : `[0:v]scale=${String(width)}:${String(height)}:force_original_aspect_ratio=decrease,pad=${String(width)}:${String(height)}:(ow-iw)/2:(oh-ih)/2:black[composite]`);
    const effects: string[] = [];
    if (options.smartZoom && !faceCrop && !splitLayout) effects.push(`scale=w='iw*(1+0.10*t/${String(duration)})':h='ih*(1+0.10*t/${String(duration)})':eval=frame,crop=${String(width)}:${String(height)}`);
    if (options.captionsPath) {
      const fonts = options.fontsDirectory ? `:fontsdir='${subtitlePath(options.fontsDirectory)}'` : '';
      const style = options.captionsPath.toLowerCase().endsWith('.ass') ? '' : ":force_style='FontName=Vazirmatn,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=1,MarginV=110,Alignment=2'";
      effects.push(`subtitles='${subtitlePath(options.captionsPath)}'${fonts}${style}`);
    }
    const mainLabel=options.broll?'main':'video';
    const baseFilter=`${background};[composite]${effects.length ? effects.join(',') : 'null'}[${mainLabel}]`;
    const brollFilter=options.broll?`;[1:v]scale=${String(width)}:${String(height)}:force_original_aspect_ratio=increase,crop=${String(width)}:${String(height)}[broll];[main][broll]overlay=enable='between(t,${options.broll.at.toFixed(3)},${(options.broll.at+options.broll.duration).toFixed(3)})'[video]`:'';
    const filter=`${baseFilter}${brollFilter}`;
    const muteFilters=(options.audioMuteRanges??[]).filter(item=>item.end>=start&&item.start<=end).map(item=>`volume=enable='between(t,${Math.max(0,item.start-start+.3).toFixed(3)},${Math.max(0,item.end-start+.3).toFixed(3)})':volume=0`);
    const speechFilter=muteFilters.length?muteFilters.join(','):'anull';
    const args = ['-ss', String(Math.max(0, start - 0.3)), '-i', source];
    if(options.broll)args.push('-ss',String(options.broll.sourceStart),'-i',source);
    const musicInput=options.broll?2:1;
    if (options.musicPath) args.push('-stream_loop', '-1', '-i', options.musicPath);
    args.push('-t', String(duration + 0.6), '-filter_complex', options.musicPath
      ? `${filter};[${musicInput}:a]volume=${String(options.musicVolume ?? 0.12)},asplit=2[musicduck][musicmix];[0:a]${speechFilter}[speech];[speech][musicduck]sidechaincompress=threshold=0.1:ratio=4[ducked];[ducked][musicmix]amix=inputs=2:duration=first:weights='1 0.15'[mixed];[mixed]loudnorm=I=-14:TP=-1.5:LRA=11[audio]`
      : filter, '-map', '[video]');
    if (options.musicPath) args.push('-map', '[audio]'); else args.push('-map', '0:a?', '-af', `${speechFilter},loudnorm=I=-14:TP=-1.5:LRA=11`);
    const encoder = options.encoder ?? await this.preferredEncoder();
    const encoding = encoder === 'h264_nvenc'
      ? ['-c:v', 'h264_nvenc', '-preset', 'p5', '-cq', '21']
      : ['-c:v', 'libx264', '-preset', 'medium', '-crf', '20'];
    args.push(...encoding, '-c:a', 'aac', '-b:a', '192k', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', output);
    try {
      await this.run(args,undefined,options.jobId);
    } catch (error: unknown) {
      if(options.jobId&&this.cancelled.has(options.jobId))throw new Error('Rendering cancelled by user');
      if (encoder !== 'h264_nvenc') throw error;
      const codecIndex = args.indexOf('-c:v');
      args.splice(codecIndex, 6, '-c:v', 'libx264', '-preset', 'medium', '-crf', '20');
      await this.run(args,undefined,options.jobId);
    }
  }

  async frame(source: string, time: number, output: string): Promise<void> {
    await this.run(['-ss', String(time), '-i', source, '-frames:v', '1', '-q:v', '2', output]);
  }
}

export function outputFor(source: string, name: string): string { return path.join(path.dirname(source), name); }
