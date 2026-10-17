const fs = require('node:fs');
const vm = require('node:vm');
const cp = require('node:child_process');
const assert = require('node:assert/strict');
const test = require('node:test');
const root = require('node:path').resolve(__dirname, '..');
const baseRef = process.env.GRIDLAS_BASE_REF || 'origin/main';
const route = 'tools/data-center-estimator/index.html';
const html = fs.readFileSync(root + '/' + route, 'utf8');
const baseline = cp.execFileSync('git', ['-C', root, 'show', baseRef + ':' + route], {encoding:'utf8'});
function boot(source) {
  const elements = new Map();
  function element(id) {
    return {id, value:'', textContent:'', innerHTML:'', className:'', style:{}, handlers:{}, options:[],
      addEventListener(name,fn){ (this.handlers[name] ||= []).push(fn); },
      appendChild(o){ this.options.push(o); },
      querySelector(selector){ assert.equal(selector,'.cv'); assert.ok(source.includes('id="'+id+'"><div class="ct">')); return this.cv ||= {textContent:''}; },
      setAttribute(name,value){ this[name]=value; }, getAttribute(name){return this[name];}
    };
  }
  for (const m of source.matchAll(/\bid="([^"]+)"/g)) elements.set(m[1], element(m[1]));
  const buttons = [...source.matchAll(/<button data-c="([^"]+)" aria-pressed="([^"]+)"/g)].map(m=>Object.assign(element('cool-'+m[1]),{'data-c':m[1],'aria-pressed':m[2]}));
  assert.equal(buttons.length,2);
  const document={
    getElementById(id){assert.ok(elements.has(id),'Unknown markup id '+id); return elements.get(id);},
    createElement(tag){assert.equal(tag,'option'); return element('option');},
    querySelectorAll(sel){assert.equal(sel,'#cooling button'); return buttons;},
    querySelector(sel){assert.equal(sel,'.gate'); return null;}
  };
  const context = {document,window:{},location:{pathname:'/'+route},console, URLSearchParams,
    fetch(){throw new Error('Unexpected network call');},setTimeout(){throw new Error('Unexpected timer');}};
  vm.createContext(context);
  const scripts=[...source.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)].filter(m=>!m[1].includes('application/ld+json')&&!m[1].includes('src='));
  assert.equal(scripts.length,1);
  vm.runInContext(scripts[0][2],context);
  return {c:context,e:elements,buttons};
}
function dispatch(el,name){ for(const fn of el.handlers[name]||[])fn.call(el,{preventDefault(){}}); }

test('national fallback does not estimate a data-center connection date',()=>{
 const {c,e}=boot(html); c.state.market='national';c.render();
 assert.equal(e.get('rWait').textContent,'Not estimated');
 assert.match(e.get('rWaitD').textContent,/utility/);
 assert.doesNotMatch(e.get('verdict').innerHTML,/Grid wait:|~5 years/);
});
test('all markets show qualitative context rather than a countdown',()=>{
 const {c,e}=boot(html);
 for(const m of c.MARKETS){c.state.market=m.id;c.render();assert.equal(e.get('rWait').textContent,'Not estimated',m.id); assert.doesNotMatch(e.get('chipGrid').cv.textContent,/Years|Months/);}
});
test('on-site options are not guaranteed queue bypasses',()=>{
 const {c,e}=boot(html);
 for(const m of c.MARKETS){c.state.market=m.id;c.render();assert.doesNotMatch(e.get('verdict').innerHTML,/Expect an|skip the queue/); assert.match(e.get('verdict').innerHTML,/permits/);}
});
test('energy water and comparison calculations match baseline for every market and cooling mode',()=>{
 const a=boot(html),b=boot(baseline);let scenarios=0;
 for(const m of a.c.MARKETS) for(const cool of ['evap','air']) for(const mw of [1,100,250,2000]){
  for(const s of [a,b]){Object.assign(s.c.state,{market:m.id,cool,mw});s.c.render();}
  for(const id of ['rPower','rPowerD','rEnergy','rEnergyD','rHomes','rHomesD','rReact','rReactD','rWater','rWaterD']){
   assert.equal(a.e.get(id).textContent,b.e.get(id).textContent,id); assert.equal(a.e.get(id).innerHTML,b.e.get(id).innerHTML,id);
  } scenarios++;
 } console.log('Preserved numeric scenarios:',scenarios);
});
test('real input handlers continue to update results',()=>{
 const {e,buttons}=boot(html);
 e.get('mw').value='100';dispatch(e.get('mw'),'input');assert.match(e.get('rPower').innerHTML,/120 /);
 dispatch(buttons[1],'click');assert.match(e.get('rPower').innerHTML,/140 /);
 e.get('market').value='national';dispatch(e.get('market'),'change');assert.equal(e.get('rWait').textContent,'Not estimated');
});
function assertCapturePreserved(before,after){
 const marker='/* ================= Klaviyo capture (same as landing page) ================= */';
 const beforeOffset=before.indexOf(marker), afterOffset=after.indexOf(marker);
 assert.ok(beforeOffset>=0,'capture marker missing from current source');
 assert.ok(afterOffset>=0,'capture marker missing from baseline');
 assert.equal(before.slice(beforeOffset),after.slice(afterOffset));
}
test('lead capture implementation is byte-identical',()=>{
 assertCapturePreserved(html,baseline);
});
test('capture preservation rejects missing markers in both versions',()=>{
 assert.throws(()=>assertCapturePreserved('unrelated\n','different\n'));
});
test('capture preservation rejects a marker missing from either version',()=>{
 assert.throws(()=>assertCapturePreserved('missing\n',baseline));
 assert.throws(()=>assertCapturePreserved(html,'missing\n'));
});
