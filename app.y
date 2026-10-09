
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Super Jump Adventure</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#70d8ff;font-family:Arial;text-align:center}
h2{color:#173a70}
canvas{width:min(96vw,900px);height:auto;border:4px solid white;border-radius:8px}
p{font-weight:bold}
button{padding:12px 20px;margin:5px;border:0;border-radius:10px;
background:#ffce32;font-size:18px;font-weight:bold}
</style>
</head>
<body>
<h2>🍄 SUPER JUMP ADVENTURE</h2>
<p>Điểm: <span id="score">0</span> | Xu: <span id="coins">0</span></p>
<canvas id="game" width="900" height="500"></canvas>
<div>
<button onclick="keys.left=true">⬅️</button>
<button onclick="jump()">NHẢY ⬆️</button>
<button onclick="keys.right=true">➡️</button>
<button onclick="restart()">🔄 Chơi lại</button>
</div>
<p>Máy tính: ← → để chạy, Space hoặc ↑ để nhảy.</p>

<script>
const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");
const W=900,H=500;
let keys={left:false,right:false};
let player,platforms,coins,enemies,score,coinCount,camera,over,win;

function restart(){
 player={x:50,y:300,w:30,h:40,vx:0,vy:0,onGround:false};
 platforms=[
  {x:0,y:450,w:500,h:50},
  {x:560,y:450,w:250,h:50},
  {x:870,y:450,w:350,h:50},
  {x:300,y:350,w:100,h:18},
  {x:620,y:340,w:100,h:18},
  {x:930,y:360,w:120,h:18},
  {x:1120,y:320,w:100,h:18},
  {x:1300,y:450,w:500,h:50}
 ];
 coins=[
  {x:320,y:310,got:false},{x:360,y:310,got:false},
  {x:650,y:300,got:false},{x:700,y:300,got:false},
  {x:960,y:320,got:false},{x:1150,y:280,got:false},
  {x:1400,y:400,got:false},{x:1460,y:400,got:false}
 ];
 enemies=[
  {x:390,y:420,vx:1.1,alive:true},
  {x:700,y:310,vx:1,alive:true},
  {x:1020,y:420,vx:1.3,alive:true},
  {x:1510,y:420,vx:1.2,alive:true}
 ];
 score=0;coinCount=0;camera=0;over=false;win=false;
}
restart();

function jump(){
 if(player.onGround&&!over&&!win){
  player.vy=-12;
  player.onGround=false;
 }
}
document.addEventListener("keydown",e=>{
 if(["ArrowLeft","ArrowRight","ArrowUp"," "].includes(e.key))e.preventDefault();
 if(e.repeat)return;
 if(e.key==="ArrowLeft")keys.left=true;
 if(e.key==="ArrowRight")keys.right=true;
 if(e.key==="ArrowUp"||e.key===" ")jump();
});
document.addEventListener("keyup",e=>{
 if(e.key==="ArrowLeft")keys.left=false;
 if(e.key==="ArrowRight")keys.right=false;
});

function hit(a,b){
 return a.x<b.x+b.w&&a.x+a.w>b.x&&
 a.y<b.y+b.h&&a.y+a.h>b.y;
}

function update(){
 if(over||win)return;

 player.vx=keys.right?4:keys.left?-4:0;
 player.x+=player.vx;

 let oldY=player.y;
 player.vy+=.55;
 player.y+=player.vy;
 player.onGround=false;

 for(const p of platforms){
  const obj={x:p.x,y:p.y,w:p.w,h:p.h};
  if(hit(player,obj)&&player.vy>=0&&oldY+player.h<=p.y+8){
   player.y=p.y-player.h;
   player.vy=0;
   player.onGround=true;
  }
 }

 // Không cho nhân vật đi xuyên cạnh trái
 player.x=Math.max(0,player.x);

 // Thu thập xu
 for(const c of coins){
  if(!c.got&&hit(player,{x:c.x,y:c.y,w:18,h:18})){
   c.got=true;coinCount++;score+=10;
  }
 }

 // Quái vật đi qua lại trên đường
 for(const e of enemies){
  if(!e.alive)continue;
  e.x+=e.vx;
  if(e.x<e.min||e.x>e.max){
   e.vx*=-1;
  }
  if(!e.min){e.min=e.x-60;e.max=e.x+60;}

  const enemyBox={x:e.x,y:e.y,w:30,h:30};
  if(hit(player,enemyBox)){
   if(player.vy>0&&oldY+player.h<=e.y+12){
    e.alive=false;player.vy=-8;score+=50;
   }else{
    over=true;
   }
  }
 }

 if(player.y>H+100)over=true;
 score+=0.02;
 camera=Math.max(0,player.x-250);

 if(player.x>1700)win=true;

 document.getElementById("score").textContent=Math.floor(score);
 document.getElementById("coins").textContent=coinCount;
}

function draw(){
 ctx.clearRect(0,0,W,H);
 ctx.save();
 ctx.translate(-camera,0);

 // Bầu trời và mây
 ctx.fillStyle="#70d8ff";ctx.fillRect(camera,0,W,H);
 for(let x=100;x<2000;x+=300){
  ctx.fillStyle="#fff";
  ctx.beginPath();ctx.arc(x,90,22,0,Math.PI*2);
  ctx.arc(x+25,80,30,0,Math.PI*2);
  ctx.arc(x+55,92,22,0,Math.PI*2);ctx.fill();
 }

 // Nền đất
 for(const p of platforms){
  ctx.fillStyle="#9b572c";ctx.fillRect(p.x,p.y,p.w,p.h);
  ctx.fillStyle="#39bb45";ctx.fillRect(p.x,p.y,p.w,9);
  ctx.strokeStyle="#70401f";ctx.strokeRect(p.x,p.y,p.w,p.h);
 }

 // Gạch trang trí
 for(let x=0;x<1800;x+=40){
  ctx.fillStyle="#d58a50";
  ctx.fillRect(x,470,38,25);
 }

 // Ống xanh
 for(const x of [180,750,1080]){
  ctx.fillStyle="#159b35";
  ctx.fillRect(x,390,50,60);
  ctx.fillRect(x-6,383,62,15);
  ctx.strokeStyle="#087b29";
  ctx.strokeRect(x,390,50,60);
 }

 // Xu
 for(const c of coins){
  if(c.got)continue;
  ctx.fillStyle="#ffdf24";
  ctx.beginPath();ctx.arc(c.x+9,c.y+9,9,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle="#f19d00";ctx.lineWidth=3;ctx.stroke();
 }

 // Quái vật
 for(const e of enemies){
  if(!e.alive)continue;
  ctx.fillStyle="#9b4f28";
  ctx.fillRect(e.x,e.y,30,28);
  ctx.fillStyle="#fff";
  ctx.fillRect(e.x+5,e.y+6,7,8);
  ctx.fillRect(e.x+19,e.y+6,7,8);
  ctx.fillStyle="#222";
  ctx.fillRect(e.x+8,e.y+8,3,4);
  ctx.fillRect(e.x+21,e.y+8,3,4);
 }

 // Nhân vật
 ctx.fillStyle="#e83428";ctx.fillRect(player.x,player.y,30,12);
 ctx.fillStyle="#ffbd83";ctx.fillRect(player.x+5,player.y+12,22,12);
 ctx.fillStyle="#df3424";ctx.fillRect(player.x+3,player.y+24,24,8);
 ctx.fillStyle="#1858c8";ctx.fillRect(player.x+4,player.y+32,10,8);
 ctx.fillRect(player.x+17,player.y+32,10,8);
 ctx.fillStyle="#222";
 ctx.fillRect(player.x+20,player.y+15,3,3);

 // Đích
 ctx.fillStyle="#fff";ctx.fillRect(1740,330,8,120);
 ctx.fillStyle="#e93636";ctx.fillRect(1748,330,60,35);
 ctx.fillStyle="#fff";ctx.fillRect(1748,347,60,8);

 ctx.restore();

 if(over||win){
  ctx.fillStyle="#14243ddd";ctx.fillRect(200,170,500,150);
  ctx.fillStyle="#fff";ctx.textAlign="center";
  ctx.font="bold 36px Arial";
  ctx.fillText(win?"🏆 CHIẾN THẮNG!":"GAME OVER",450,225);
  ctx.font="22px Arial";
  ctx.fillText("Điểm: "+Math.floor(score)+" | Xu: "+coinCount,450,270);
  ctx.fillText("Nhấn Chơi lại để thử tiếp",450,300);
 }
}

function loop(){
 update();draw();requestAnimationFrame(loop);
}
loop();
</script>
</body>
</html>
