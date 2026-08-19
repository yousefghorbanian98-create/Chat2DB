import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import path from 'node:path';

const read=(file:string):string=>readFileSync(path.resolve(file),'utf8');

describe('navigation and editor UI regressions',()=>{
  it('has a routed page for every sidebar destination',()=>{
    const sidebar=read('src/components/Sidebar.tsx');const app=read('src/App.tsx');
    for(const route of ['/upload','/channel','/sync','/clipper','/pending','/history','/settings']){
      expect(sidebar).toContain(`'${route}'`);expect(app).toContain(`path="${route.slice(1)}"`);
    }
  });
  it('connects every visible editor tab to real state',()=>{
    const editor=read('src/pages/Clipper.tsx');
    for(const tab of ['media','audio','text','ai']){
      expect(editor).toContain(`activeAssetTab==='${tab}'`);expect(editor).toContain(`['${tab}',`);
    }
    expect(editor).toContain('onClick={()=>setActiveAssetTab(id)}');
  });
  it('does not cancel processing when the editor unmounts',()=>{
    const editor=read('src/pages/Clipper.tsx');const main=read('electron/main.ts');
    const cleanup=editor.match(/return \(\) => \{([^}]+)\}/)?.[1]??'';
    expect(cleanup).not.toContain('cancel(');
    expect(main).toContain('backgroundThrottling:false');
  });
  it('respects reduced-motion accessibility',()=>{expect(read('src/index.css')).toContain('prefers-reduced-motion:reduce')});
});
