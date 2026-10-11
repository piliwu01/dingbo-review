#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""產生：定伯賣鬼 段考複習手遊（闖關打怪）單一 HTML 檔"""
import ast, json

_src = open('gen_exam_v2.py', encoding='utf-8').read()
_tree = ast.parse(_src)
_vals = {}
for _node in _tree.body:
    if isinstance(_node, ast.Assign) and len(_node.targets) == 1 and isinstance(_node.targets[0], ast.Name):
        if _node.targets[0].id in ('QDATA', 'ORIGINAL', 'QTAGS', 'LETTERS'):
            _vals[_node.targets[0].id] = ast.literal_eval(_node.value)
QDATA, ORIGINAL = _vals['QDATA'], _vals['ORIGINAL']
LETTERS = ['A', 'B', 'C', 'D']

questions = []
for i, (stem, opts, ans, exp) in enumerate(QDATA, start=1):
    questions.append({'id': i, 'stem': stem, 'opts': opts, 'ans': ans, 'exp': exp})

stages = [
    {'name': '第一關：夜行逢鬼', 'monster': '遊魂小鬼', 'desc': '夜行遇鬼，臨危不亂。答對攻擊，答錯扣血。', 'qs': list(range(1, 11))},
    {'name': '第二關：鬥智渡水', 'monster': '渡水水鬼', 'desc': '驗證人鬼之別，套取弱點。', 'qs': list(range(11, 21))},
    {'name': '第三關：智縛鬼', 'monster': '咋咋厲鬼', 'desc': '近市縛鬼，緊抓不放。', 'qs': list(range(21, 31))},
    {'name': '最終關：宛市決戰', 'monster': '化羊大魔王', 'desc': '素養題組，直面恐懼，智勇同行。', 'qs': list(range(31, 41))},
]

qjson = json.dumps(questions, ensure_ascii=False)
sjson = json.dumps(stages, ensure_ascii=False)
orig_js = json.dumps(ORIGINAL, ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>定伯賣鬼：段考複習手遊</title>
<style>
:root{--bg:#0f172a;--panel:#1e293b;--panel2:#273449;--acc:#f59e0b;--hp:#22c55e;--ehp:#ef4444;--txt:#f1f5f9;--mut:#94a3b8;}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
body{margin:0;background:radial-gradient(1200px 600px at 70% -10%,#1e3a5f,#0f172a 60%);color:var(--txt);font-family:"標楷體","KaiU","BiauKai","Noto Sans TC",serif;min-height:100vh;display:flex;justify-content:center;}
#app{width:min(1180px,100%);padding:14px;}
.screen{display:none;} .screen.on{display:block;}
.topbar{display:flex;align-items:center;gap:10px;background:var(--panel);border:1px solid #334155;border-radius:12px;padding:8px 12px;margin-bottom:10px;flex-wrap:wrap;}
.topbar .title{font-size:20px;font-weight:bold;color:var(--acc);}
.topbar .sp{flex:1;}
button{font-family:inherit;cursor:pointer;}
.btn{background:var(--acc);border:none;color:#1c1005;font-weight:bold;border-radius:10px;padding:10px 18px;font-size:16px;}
.btn:hover{filter:brightness(1.08);} .btn.ghost{background:#334155;color:var(--txt);}
.btn.big{font-size:19px;padding:14px 26px;}
.btn:disabled{opacity:.45;cursor:not-allowed;}
/* battle layout */
.battle{display:grid;grid-template-columns:minmax(300px,420px) 1fr;gap:12px;}
@media (max-width:820px){.battle{grid-template-columns:1fr;}}
.arena{background:linear-gradient(#16233d,#0f172a);border:1px solid #334155;border-radius:14px;padding:12px;text-align:center;position:relative;overflow:hidden;}
.hpRow{display:flex;align-items:center;gap:8px;margin:6px 0;font-size:14px;}
.hpRow .nm{width:110px;text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.bar{flex:1;height:16px;background:#0b1220;border:1px solid #475569;border-radius:99px;overflow:hidden;}
.bar>i{display:block;height:100%;width:100%;transition:width .35s;}
.bar.me>i{background:linear-gradient(90deg,#16a34a,#4ade80);}
.bar.foe>i{background:linear-gradient(90deg,#dc2626,#f87171);}
.monster{font-size:96px;line-height:1.2;user-select:none;transition:transform .12s;}
.monster.hit{animation:shake .35s;} @keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-14px) rotate(-6deg)}50%{transform:translateX(12px)}75%{transform:translateX(-6px)}}
.monster.atk{animation:lunge .35s;} @keyframes lunge{40%{transform:translateY(14px) scale(1.08)}}
.player{font-size:56px;}
.combo{font-size:15px;color:var(--acc);min-height:22px;font-weight:bold;}
.qcard{background:var(--panel);border:1px solid #334155;border-radius:14px;padding:14px;}
.qcard .meta{color:var(--mut);font-size:13px;margin-bottom:6px;}
.qcard .stem{font-size:19px;line-height:1.6;margin-bottom:12px;}
.opts{display:grid;gap:10px;}
.opt{background:var(--panel2);border:2px solid #3b4c63;color:var(--txt);border-radius:10px;padding:12px;font-size:17px;text-align:left;line-height:1.5;}
.opt:hover:not(:disabled){border-color:var(--acc);}
.opt.right{border-color:#22c55e;background:#14532d;}
.opt.wrong{border-color:#ef4444;background:#7f1d1d;}
.exp{display:none;background:#0b1220;border:1px dashed #475569;border-radius:10px;padding:10px;margin-top:10px;font-size:15px;line-height:1.6;}
.exp.show{display:block;}
.nextRow{margin-top:10px;text-align:right;}
/* menu */
.menu{background:var(--panel);border:1px solid #334155;border-radius:14px;padding:22px;text-align:center;}
.menu h1{margin:6px 0 2px;font-size:30px;color:var(--acc);}
.menu p{color:var(--mut);}
.stageGrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin:14px 0;}
.stage{background:var(--panel2);border:2px solid #3b4c63;border-radius:12px;padding:12px;color:var(--txt);}
.stage h3{margin:4px 0;} .stage small{color:var(--mut);}
.stage.lock{opacity:.45;}
.orig{max-height:150px;overflow:auto;background:#0b1220;border:1px solid #334155;border-radius:10px;padding:10px;font-size:14px;line-height:1.7;text-align:left;margin-top:12px;}
.resLine{font-size:19px;margin:8px 0;}
table.mist{width:100%;border-collapse:collapse;font-size:14px;} table.mist td,table.mist th{border:1px solid #475569;padding:6px;text-align:left;vertical-align:top;}
.badge{display:inline-block;background:#334155;border-radius:99px;padding:2px 12px;font-size:13px;color:var(--txt);}
.floatDmg{position:absolute;font-weight:bold;font-size:26px;pointer-events:none;animation:floatUp 1s forwards;}
@keyframes floatUp{to{transform:translateY(-70px);opacity:0;}}
.score{font-size:15px;}
</style>
</head>
<body>
<div id="app">
  <div class="topbar">
    <span class="title">定伯賣鬼：段考複習手遊</span>
    <span class="sp"></span>
    <span class="score" id="hudScore">分數 0</span>
    <button class="btn ghost" id="btnSound">音效：開</button>
    <button class="btn ghost" id="btnHome">回主選單</button>
  </div>

  <div class="screen on" id="scrMenu">
    <div class="menu">
      <div style="font-size:64px;">&#x9B3C;</div>
      <h1>直面恐懼・智勇同行</h1>
      <p>七年級國文・定伯賣鬼 40 題・共 4 關・答對攻擊魔王，答錯自己扣血</p>
      <div>最高分：<b id="bestScore">0</b>　<span class="badge" id="clearBadge">尚未破關</span></div>
      <div class="stageGrid" id="stageGrid"></div>
      <div style="text-align:left;font-size:14px;color:var(--mut);">破關規則：玩家血量 100，答錯扣 12；魔王血量依題數而定，答對造成傷害，3 連擊以上有加成。血量歸零可重打該關。通關後可看錯題複習。</div>
      <div class="orig" id="origBox"></div>
    </div>
  </div>

  <div class="screen" id="scrGame">
    <div class="battle">
      <div class="arena" id="arena">
        <div class="hpRow"><span class="nm" id="foeName">魔王</span><div class="bar foe"><i id="foeHp"></i></div><span id="foeHpT"></span></div>
        <div class="monster" id="monster">&#x9B3C;</div>
        <div class="combo" id="combo"></div>
        <div style="font-size:40px;">&#x2694;&#xFE0F;</div>
        <div class="player">&#x52C9;&#x58EB;</div>
        <div class="hpRow"><span class="nm">宋定伯（你）</span><div class="bar me"><i id="meHp"></i></div><span id="meHpT"></span></div>
        <div class="score" id="stageInfo"></div>
      </div>
      <div class="qcard">
        <div class="meta" id="qMeta"></div>
        <div class="stem" id="qStem"></div>
        <div class="opts" id="qOpts"></div>
        <div class="exp" id="qExp"></div>
        <div class="nextRow"><button class="btn" id="btnNext" style="display:none;">下一題</button></div>
      </div>
    </div>
  </div>

  <div class="screen" id="scrEnd">
    <div class="menu">
      <h1 id="endTitle">破關成功</h1>
      <div class="resLine" id="endStats"></div>
      <div id="mistWrap"></div>
      <p><button class="btn big" id="btnAgain">再打一次</button>
      <button class="btn ghost big" id="btnMenu2">回主選單</button></p>
    </div>
  </div>
</div>

<script>
const Q = __Q__;
const STAGES = __S__;
const MON_ICON = ["👹","🌊","😈","🐏"];
let sound = true, stageIdx = 0, qi = 0, meHP = 100, foeHP = 100, foeMax = 100;
let score = 0, combo = 0, maxCombo = 0, wrongList = [], answered = false;
const $ = id => document.getElementById(id);
const byId = {}; Q.forEach(q => byId[q.id] = q);

function beep(f, d){ if(!sound) return; try{
  const ctx = beep.ctx || (beep.ctx = new (window.AudioContext||window.webkitAudioContext)());
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.connect(g); g.connect(ctx.destination); o.frequency.value = f; o.type = "sine";
  g.gain.setValueAtTime(.18, ctx.currentTime); g.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + d);
  o.start(); o.stop(ctx.currentTime + d);
}catch(e){} }

function show(id){ document.querySelectorAll(".screen").forEach(s=>s.classList.remove("on")); $(id).classList.add("on"); }
function save(k,v){ try{localStorage.setItem("dingbo_"+k, JSON.stringify(v));}catch(e){} }
function load(k,d){ try{const v = localStorage.getItem("dingbo_"+k); return v==null?d:JSON.parse(v);}catch(e){ return d; } }

function renderMenu(){
  $("bestScore").textContent = load("best",0);
  const cleared = load("cleared",[]);
  $("clearBadge").textContent = cleared.length>=4 ? "四關全破・智勇雙全" : (cleared.length? "已破 "+cleared.length+" 關" : "尚未破關");
  const g = $("stageGrid"); g.innerHTML = "";
  STAGES.forEach((s,i)=>{
    const lock = i>0 && !cleared.includes(i-1);
    const b = document.createElement("button");
    b.className = "stage"+(lock?" lock":"");
    b.innerHTML = "<div style='font-size:34px;'>"+MON_ICON[i]+"</div><h3>"+s.name+"</h3><div>"+s.monster+"</div><small>"+s.desc+"</small><br><small>"+(lock?"需先通過前一關":"10 題")+"</small>";
    b.disabled = lock;
    b.onclick = ()=>startStage(i);
    g.appendChild(b);
  });
  $("origBox").textContent = "【課文回顧】" + __O__;
}

function startStage(i){
  stageIdx = i; qi = 0; meHP = 100; combo = 0; maxCombo = 0; wrongList = [];
  foeMax = STAGES[i].qs.length * 10; foeHP = foeMax;
  $("foeName").textContent = STAGES[i].monster;
  updateBars(); show("scrGame"); renderQ();
  $("stageInfo").textContent = STAGES[i].name + "・" + STAGES[i].qs.length + " 題";
}
function updateBars(){
  $("meHp").style.width = Math.max(0,meHP)+"%"; $("meHpT").textContent = Math.max(0,meHP);
  $("foeHp").style.width = (100*Math.max(0,foeHP)/foeMax)+"%"; $("foeHpT").textContent = Math.max(0,foeHP)+"/"+foeMax;
  $("hudScore").textContent = "分數 "+score;
}
function floatText(txt, color){
  const a = $("arena"), s = document.createElement("span");
  s.className = "floatDmg"; s.textContent = txt; s.style.color = color;
  s.style.left = (30+Math.random()*50)+"%"; s.style.top = "38%";
  a.appendChild(s); setTimeout(()=>s.remove(), 1000);
}
function renderQ(){
  answered = false;
  const qid = STAGES[stageIdx].qs[qi], q = byId[qid];
  $("monster").textContent = MON_ICON[stageIdx];
  $("qMeta").textContent = "第 "+(qi+1)+" / "+STAGES[stageIdx].qs.length+" 題・題號 "+qid;
  $("qStem").textContent = q.stem;
  $("qExp").className = "exp"; $("qExp").textContent = "";
  $("btnNext").style.display = "none"; $("combo").textContent = combo>=2 ? "COMBO x"+combo : "";
  const box = $("qOpts"); box.innerHTML = "";
  q.opts.forEach((t,oi)=>{
    const b = document.createElement("button");
    b.className = "opt"; b.textContent = "("+"ABCD"[oi]+") "+t;
    b.onclick = ()=>answer(oi, b);
    box.appendChild(b);
  });
}
function answer(oi, btn){
  if(answered) return; answered = true;
  const qid = STAGES[stageIdx].qs[qi], q = byId[qid];
  const btns = $("qOpts").children;
  [...btns].forEach(b=>b.disabled = true);
  btns[q.ans].classList.add("right");
  if(oi === q.ans){
    combo++; maxCombo = Math.max(maxCombo, combo);
    const dmg = 10 + Math.min(10, combo*2);
    foeHP -= dmg; score += 100 + combo*20;
    $("monster").classList.remove("hit"); void $("monster").offsetWidth; $("monster").classList.add("hit");
    floatText("-"+dmg, "#fbbf24"); beep(660,.15); setTimeout(()=>beep(880,.15),120);
  } else {
    btn.classList.add("wrong"); combo = 0;
    meHP -= 12;
    const m = $("monster"); m.classList.remove("atk"); void m.offsetWidth; m.classList.add("atk");
    floatText("你 -12", "#f87171"); beep(200,.25);
    wrongList.push(qid);
  }
  $("qExp").textContent = "解析："+q.exp+"（正確答案 "+ "ABCD"[q.ans] +"）";
  $("qExp").className = "exp show";
  updateBars();
  $("btnNext").style.display = "";
  $("btnNext").textContent = (qi+1 >= STAGES[stageIdx].qs.length) ? "結算" : "下一題";
}
$("btnNext").onclick = ()=>{
  if(meHP <= 0){ gameOver(false); return; }
  if(foeHP <= 0 || qi+1 >= STAGES[stageIdx].qs.length){ stageClear(); return; }
  qi++; renderQ();
};
function stageClear(){
  const cleared = load("cleared",[]);
  if(!cleared.includes(stageIdx)){ cleared.push(stageIdx); save("cleared",cleared); }
  const best = load("best",0); if(score>best) save("best",score);
  if(stageIdx>=3){ gameOver(true); return; }
  gameOver(true, true);
}
function gameOver(win, cont){
  show("scrEnd");
  $("endTitle").textContent = !win ? "血量歸零・再接再厲" : (stageIdx>=3 ? "四關全破・賣鬼成功" : STAGES[stageIdx].name+" 通過");
  const acc = STAGES[stageIdx].qs.length - wrongList.length;
  $("endStats").innerHTML = "本關答對 "+acc+" / "+STAGES[stageIdx].qs.length+"・最高連擊 x"+maxCombo+"・總分 "+score;
  const w = $("mistWrap");
  if(!wrongList.length){ w.innerHTML = "<p>全部答對，太厲害了。</p>"; }
  else{
    let h = "<h3>錯題複習（"+wrongList.length+" 題）</h3><table class='mist'><tr><th>題</th><th>題目與解析</th></tr>";
    wrongList.forEach(id=>{ const q = byId[id];
      h += "<tr><td>"+id+"."+ "ABCD"[q.ans] +"</td><td>"+q.stem+"<br>選項："+q.opts.map((t,i)=>"("+"ABCD"[i]+")"+t).join("／")+"<br>解析："+q.exp+"</td></tr>"; });
    w.innerHTML = h+"</table>";
  }
  const again = $("btnAgain");
  if(!win){ again.textContent = "重打本關"; again.onclick = ()=>{ resetRun(); startStage(stageIdx); }; }
  else if(cont){ again.textContent = "挑戰下一關"; again.onclick = ()=>{ resetRun(); startStage(stageIdx+1); }; }
  else { again.textContent = "再打一次"; again.onclick = ()=>{ resetRun(); startStage(0); }; }
}
function resetRun(){ score = 0; $("hudScore").textContent = "分數 0"; }
$("btnAgain").onclick = ()=>{};
$("btnMenu2").onclick = ()=>{ renderMenu(); show("scrMenu"); };
$("btnHome").onclick = ()=>{ renderMenu(); show("scrMenu"); };
$("btnSound").onclick = e=>{ sound=!sound; e.target.textContent = "音效："+(sound?"開":"關"); };
renderMenu();
</script>
</body>
</html>'''

html = html.replace('__Q__', qjson).replace('__S__', sjson).replace('__O__', orig_js)
out = '定伯賣鬼_複習手遊.html'
open(out, 'w', encoding='utf-8').write(html)
print('saved:', out, len(html))
