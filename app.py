
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cậu Bé Và Chú Chó 3D</title>
<style>
*{box-sizing:border-box}
body{margin:0;overflow:hidden;background:#8bdfff;font-family:Arial}
#ui{position:fixed;top:12px;left:12px;z-index:2;
background:#17243ddd;color:white;padding:12px 16px;
border-radius:14px;line-height:1.7;font-size:16px}
#message{position:fixed;top:42%;width:100%;text-align:center;
font-size:25px;font-weight:bold;color:white;
text-shadow:2px 3px 5px #222;pointer-events:none}
#controls{position:fixed;bottom:14px;width:100%;display:flex;
justify-content:center;gap:7px;flex-wrap:wrap}
button{border:0;border-radius:12px;padding:12px 16px;
font-size:16px;font-weight:bold;background:#ffd43b}
</style>
</head>
<body>
<div id="ui">
🏃 CẬU BÉ CHẠY TRỐN<br>
📏 Quãng đường: <span id="distance">0</span> m<br>
🪙 Xu: <span id="coins">0</span><br>
⚡ Tăng tốc: <span id="boost">Chưa có</span><br>
🛵 Xe máy: <span id="bikeStatus">Chưa mở khóa</span>
</div>
<div id="message">CHẠY THÔI! CHÓ ĐANG ĐUỔI! 🐕</div>
<div id="controls">
<button onclick="changeLane(-1)">⬅️ Trái</button>
<button onclick="doJump()">⬆️ Nhảy</button>
<button onclick="changeLane(1)">➡️ Phải</button>
<button onclick="slide()">⬇️ Trượt</button>
<button onclick="rideBike()">E - Lên xe</button>
<button onclick="restart()">🔄 Chơi lại</button>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x8bdfff);
scene.fog = new THREE.Fog(0x8bdfff, 35, 140);

const camera = new THREE.PerspectiveCamera(
 65, innerWidth/innerHeight, 0.1, 400
);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;
document.body.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xffffff,0x557044,2));
const sun = new THREE.DirectionalLight(0xffffff,2.2);
sun.position.set(-5,15,8);
sun.castShadow=true;
scene.add(sun);

const material = c => new THREE.MeshStandardMaterial({color:c});
const mats={
 road:material(0x414957),grass:material(0x39a852),
 white:material(0xffffff),skin:material(0xffc18b),
 shirt:material(0x168de0),pants:material(0x24334c),
 shoe:material(0xf4f4f4),hair:material(0x3d281b),
 dog:material(0xb8783c),dark:material(0x20232b),
 gold:material(0xffcf27),red:material(0xe53b36),
 green:material(0x168b43),milk:material(0xf5e8ce)
};

function box(parent,x,y,z,w,h,d,mat){
 const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);
 o.position.set(x,y,z);
 o.castShadow=true;o.receiveShadow=true;
 parent.add(o);return o;
}
function sphere(parent,x,y,z,r,mat){
 const o=new THREE.Mesh(new THREE.SphereGeometry(r,16,12),mat);
 o.position.set(x,y,z);o.castShadow=true;
 parent.add(o);return o;
}
function cylinder(parent,x,y,z,r1,r2,h,mat){
 const o=new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,16),mat);
 o.position.set(x,y,z);parent.add(o);return o;
}

// Đường 3 làn
box(scene,0,-.2,-120,10,.4,300,mats.road);
box(scene,-5.6,-.1,-120,1,.2,300,mats.grass);
box(scene,5.6,-.1,-120,1,.2,300,mats.grass);

for(let z=10;z>-280;z-=9){
 for(const x of [-1.5,1.5]) box(scene,x,.015,z,.06,.03,3,mats.white);
}

// Cây hai bên đường
for(let z=0;z>-280;z-=13){
 for(const x of [-7,7]){
  cylinder(scene,x,.8,z,.18,.24,1.6,material(0x80532d));
  sphere(scene,x,1.9,z,.9,material(0x239c4c));
 }
}

// Tạo cậu bé
function createBoy(){
 const g=new THREE.Group();
 box(g,0,1.05,0,.65,.8,.4,mats.shirt);
 sphere(g,0,1.67,0,.29,mats.skin);
 sphere(g,0,1.84,-.015,.3,mats.hair);
 box(g,0,1.95,0,.55,.12,.42,mats.hair);
 box(g,-.39,1.05,0,.17,.65,.18,mats.skin);
 box(g,.39,1.05,0,.17,.65,.18,mats.skin);
 const legs=[];
 for(const x of [-.18,.18]){
  legs.push(box(g,x,.43,0,.2,.65,.22,mats.pants));
  box(g,x,.12,-.07,.25,.16,.35,mats.shoe);
 }
 scene.add(g);
 return {group:g,legs};
}
const player=createBoy();
const boy=player.group;

// Tạo chú chó
function createDog(){
 const g=new THREE.Group();
 box(g,0,.57,0,.75,.6,1.05,mats.dog);
 sphere(g,0,.83,-.57,.38,mats.dog);
 sphere(g,-.25,1.12,-.72,.17,mats.dog);
 sphere(g,.25,1.12,-.72,.17,mats.dog);
 sphere(g,-.13,.89,-.9,.07,mats.white);
 sphere(g,.13,.89,-.9,.07,mats.white);
 sphere(g,0,.73,-.95,.08,mats.dark);
 for(const x of [-.24,.24])
  for(const z of [-.34,.34])
   box(g,x,.2,z,.16,.4,.16,mats.dog);
 scene.add(g);
 return g;
}
const dog=createDog();

// Hộp Milo kiểu vật phẩm đồ uống
const drink=new THREE.Group();
box(drink,0,.52,0,.62,1,.48,mats.green);
box(drink,0,.55,.25,.42,.34,.025,mats.milk);
box(drink,0,.65,.275,.25,.1,.03,mats.red);
box(drink,0,1.06,0,.32,.1,.32,mats.milk);
drink.position.set(0,0,-100);
scene.add(drink);

// Xe máy 3D đơn giản
const bike=new THREE.Group();
for(const z of [-.65,.65]){
 const wheel=new THREE.Mesh(
  new THREE.TorusGeometry(.29,.09,12,24),mats.dark);
 wheel.position.set(0,.31,z);
 bike.add(wheel);
 cylinder(bike,0,.31,z,.06,.06,.15,mats.white);
}
box(bike,0,.72,0,.38,.3,1,mats.red);
box(bike,0,.91,-.12,.38,.12,.4,mats.dark);
box(bike,0,1.08,-.6,.65,.07,.08,mats.dark);
bike.position.set(0,0,-200);
scene.add(bike);

// Tạo xu và chướng ngại
const collectibles=[];
const obstacles=[];
function makeCoin(z,lane){
 const g=new THREE.Group();
 const ring=new THREE.Mesh(
  new THREE.TorusGeometry(.25,.08,10,20),mats.gold);
 g.add(ring);
 g.position.set([-3,0,3][lane],1.15,z);
 scene.add(g);
 collectibles.push({g,z,lane,got:false});
}
function makeObstacle(z,lane,type){
 const g=new THREE.Group();
 if(type==="barrier"){
  box(g,0,.5,0,1,.9,.5,mats.red);
  box(g,0,.55,.27,1,.14,.04,mats.white);
 }else{
  box(g,0,.4,0,.9,.8,.8,material(0x9b653c));
 }
 g.position.set([-3,0,3][lane],0,z);
 scene.add(g);
 obstacles.push({g,z,lane,type,hit:false});
}

for(let z=-15;z>-300;z-=10){
 makeCoin(z,Math.floor(Math.random()*3));
}
for(let z=-25;z>-300;z-=18){
 makeObstacle(z,Math.floor(Math.random()*3),
 Math.random()<.5?"barrier":"crate");
}

let distance=0,coinCount=0,lane=1;
let jumpY=0,jumpV=0,slideTime=0;
let boostDistance=0,onBike=false,gameOver=false;
let dogGap=4,lastTime=performance.now();

function message(t){
 const el=document.getElementById("message");
 el.textContent=t;
}
function changeLane(d){
 if(!gameOver)lane=Math.max(0,Math.min(2,lane+d));
}
function doJump(){
 if(!gameOver&&!onBike&&jumpY===0)jumpV=.22;
}
function slide(){
 if(!gameOver&&!onBike)slideTime=.65;
}
function rideBike(){
 if(!gameOver&&distance>=195&&!onBike&&distance<=230){
  onBike=true;bike.visible=false;
  message("LÊN XE THÀNH CÔNG! 🛵");
 }
}
function restart(){
 distance=0;coinCount=0;lane=1;
 jumpY=0;jumpV=0;slideTime=0;
 boostDistance=0;onBike=false;gameOver=false;dogGap=4;
 boy.position.set(0,0,0);
 dog.position.set(0,0,4);
 drink.visible=true;bike.visible=true;
 collectibles.forEach(o=>{o.got=false;o.g.visible=true});
 obstacles.forEach(o=>{o.hit=false});
 message("CHẠY THÔI! CHÓ ĐANG ĐUỔI! 🐕");
 lastTime=performance.now();
}
function finish(){
 gameOver=true;
 message("🐕 CHÓ BẮT KỊP RỒI! Điểm: "+Math.floor(distance));
}

function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min((now-lastTime)/16.67,2);
 lastTime=now;

 if(!gameOver){
  let speed=onBike?.34:(boostDistance>0?.22:.13);
  distance+=speed*dt;
  if(boostDistance>0)boostDistance=Math.max(0,boostDistance-speed*dt);

  boy.position.x += ([-3,0,3][lane]-boy.position.x)*.18*dt;
  boy.position.z=-distance;

  if(jumpV!==0||jumpY>0){
   jumpY+=jumpV*dt;
   jumpV-=.014*dt;
   if(jumpY<=0){jumpY=0;jumpV=0;}
  }
  if(slideTime>0)slideTime-=dt/60;
  boy.position.y=jumpY;
  boy.scale.y=slideTime>0?.6:1;

  // Chó bám đuổi theo
  dogGap-=.0018*dt;
  if(boostDistance>0)dogGap=Math.min(4,dogGap+.018*dt);
  if(onBike)dogGap=Math.min(7,dogGap+.035*dt);
  dog.position.set(boy.position.x,0,boy.position.z+dogGap);

  // Milo xuất hiện từ mốc 100m
  drink.visible=distance<100;
  drink.position.z=-100;
  if(distance>=98&&distance<=102&&
    Math.abs(boy.position.x-drink.position.x)<1.25){
   boostDistance=200;
   drink.visible=false;
   message("🥤 NHẶT HỘP ĐỒ UỐNG! TĂNG TỐC!");
  }

  // Xe máy ở mốc 200m
  bike.visible=!onBike&&distance<200;
  bike.position.z=-200;
  if(distance>=198&&distance<=202&&
    Math.abs(boy.position.x-bike.position.x)<1.4){
   onBike=true;bike.visible=false;
   message("🛵 ĐÃ LÊN XE MÁY!");
  }

  // Thu thập xu
  collectibles.forEach(o=>{
   if(o.got)return;
   if(Math.abs(distance+o.z)<1.1&&
      Math.abs(boy.position.x-o.g.position.x)<1.2){
    o.got=true;o.g.visible=false;coinCount++;
   }
  });

  // Va chạm chướng ngại
  obstacles.forEach(o=>{
   if(o.hit)return;
   if(Math.abs(distance+o.z)<.8&&
      Math.abs(boy.position.x-o.g.position.x)<.85&&
      jumpY<.8&&slideTime<=0&&!onBike){
    o.hit=true;
    dogGap-=.8;
    message("⚠️ CẨN THẬN CHƯỚNG NGẠI!");
  }
  });

  if(dogGap<.8)finish();

  document.getElementById("distance").textContent=Math.floor(distance);
  document.getElementById("coins").textContent=coinCount;
  document.getElementById("boost").textContent=
   boostDistance>0?"Đang tăng tốc":"Chưa có";
  document.getElementById("bikeStatus").textContent=
   onBike?"Đang lái xe":distance>=200?"Đã xuất hiện":"Chưa xuất hiện";

  player.legs[0].rotation.x=Math.sin(now*.015)*.5;
  player.legs[1].rotation.x=-player.legs[0].rotation.x;
 }

 camera.position.lerp(
  new THREE.Vector3(boy.position.x,5,boy.position.z+9),.08);
 camera.lookAt(boy.position.x,1,boy.position.z-5);
 renderer.render(scene,camera);
}

document.addEventListener("keydown",e=>{
 if(e.repeat)return;
 if(e.key==="ArrowLeft")changeLane(-1);
 if(e.key==="ArrowRight")changeLane(1);
 if(e.key==="ArrowUp"||e.key===" ")doJump();
 if(e.key==="ArrowDown")slide();
 if(e.key.toLowerCase()==="e")rideBike();
 if(gameOver&&e.key.toLowerCase()==="r")restart();
});
addEventListener("resize",()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
requestAnimationFrame(animate);
</script>
</body>
</html>
