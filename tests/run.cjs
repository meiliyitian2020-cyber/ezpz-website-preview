const {spawn}=require('child_process');
const path=require('path');
const children=[];
async function ensureServer(port,directory){
 try{const r=await fetch(`http://127.0.0.1:${port}/`);if(r.ok)return;}catch{}
 const p=spawn('python',['-m','http.server',String(port),'--bind','127.0.0.1','--directory',directory],{stdio:'ignore',windowsHide:true});children.push(p);
 for(let i=0;i<50;i++){try{const r=await fetch(`http://127.0.0.1:${port}/`);if(r.ok)return;}catch{}await new Promise(r=>setTimeout(r,100));}
 throw Error('Preview server did not start: '+port);
}
(async()=>{
 await ensureServer(8766,path.resolve('dist'));
 await ensureServer(8767,process.env.BASELINE_DIRECTORY||'G:/26.11.05-官网优化/ola-hosted-preview/dist');
 const test=spawn(process.execPath,['tests/verify.cjs'],{stdio:'inherit',windowsHide:true});
 const code=await new Promise(r=>test.once('exit',r));
 children.forEach(p=>p.kill());process.exitCode=code||0;
})().catch(e=>{children.forEach(p=>p.kill());console.error(e);process.exit(1)});
