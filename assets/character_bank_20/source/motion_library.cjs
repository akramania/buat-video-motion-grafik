/** Original deterministic pose/action library for Bank Watak 20.
 * No render clock, randomness, network dependency or paid API.
 * Angles in degrees; limbs use x=sin(angle), y=cos(angle), with 0 down.
 * Angles are GLOBAL in the character frame, not relative to the parent limb.
 */
'use strict';
const PI=Math.PI, rad=PI/180, deg=180/PI;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const smooth=x=>{x=clamp(x);return x*x*x*(x*(x*6-15)+10)};
const mix=(a,b,t)=>a+(b-a)*t;
const copy=x=>JSON.parse(JSON.stringify(x));
const BASE_STATE=Object.freeze({rootX:0,rootY:0,bodyLean:0,headTilt:0,leftUpperArm:-10,leftForearm:0,rightUpperArm:10,rightForearm:0,leftThigh:0,rightThigh:0,leftShin:0,rightShin:0,footLeft:0,footRight:0,leftUpperArmScale:1,rightUpperArmScale:1,handLeft:'relaxed',handRight:'relaxed',expression:'neutral',blink:0,mouthOpen:0,prop:null,propAttachment:null,view:'front',contacts:{left:true,right:true,ground_mode:'fixed',left_kind:'foot',right_kind:'foot'}});
const NUMBERS=['rootX','rootY','bodyLean','headTilt','leftUpperArm','leftForearm','rightUpperArm','rightForearm','leftThigh','rightThigh','leftShin','rightShin','footLeft','footRight','blink','mouthOpen','leftUpperArmScale','rightUpperArmScale'];
const P=(id,label,view,tags,state)=>({id,label,view,tags,state});
const seated={rootY:184,leftThigh:90,rightThigh:90,leftShin:0,rightShin:0,prop:'chair',propAttachment:'scene',view:'side',contacts:{left:true,right:true,ground_mode:'fixed',left_kind:'foot',right_kind:'foot',seat:true}};
const kneel={rootX:100-Math.sqrt(184*184-25*25),rootY:159,leftThigh:0,leftShin:-90,rightThigh:Math.acos(25/184)*deg,rightShin:0,footLeft:-90,prop:null,view:'three_quarter',contacts:{left:true,right:true,ground_mode:'fixed',left_kind:'knee',right_kind:'foot'}};
const poseRecords=[
P('stand_relaxed','Berdiri santai','front',['asas','berdiri'],{}),
P('stand_welcome','Menyambut dengan tapak tangan terbuka','front',['salam','berdiri'],{leftUpperArm:-30,leftForearm:-65,rightUpperArm:30,rightForearm:65,handLeft:'open',handRight:'open',expression:'happy'}),
P('stand_confident','Berdiri yakin, satu tangan di pinggang','three_quarter',['yakin','berdiri'],{bodyLean:-2,headTilt:3,leftUpperArm:-25,leftForearm:70,rightUpperArm:12,rightForearm:0,handLeft:'relaxed',expression:'happy'}),
P('wave_hello','Melambai salam','front',['salam','tangan'],{rightUpperArm:52,rightForearm:165,handRight:'open',headTilt:-4,expression:'happy'}),
P('explain_one_hand','Menerang dengan sebelah tangan','three_quarter',['penerangan','tangan'],{rightUpperArm:32,rightForearm:84,handRight:'open',headTilt:-2}),
P('explain_two_hands','Menerang dengan kedua-dua tangan','front',['penerangan','tangan'],{leftUpperArm:-36,leftForearm:-86,rightUpperArm:36,rightForearm:86,handLeft:'open',handRight:'open'}),
P('point_left','Menunjuk ke kiri skrin','front',['tunjuk','tangan'],{leftUpperArm:-65,leftForearm:-92,handLeft:'point',headTilt:5}),
P('point_right','Menunjuk ke kanan skrin','front',['tunjuk','tangan'],{rightUpperArm:65,rightForearm:92,handRight:'point',headTilt:-5}),
P('point_up','Menunjuk ke atas','front',['tunjuk','tangan'],{rightUpperArm:50,rightForearm:166,handRight:'point',headTilt:-5}),
P('think','Berfikir sambil menyentuh dagu','three_quarter',['emosi','tangan'],{rightUpperArm:-19,rightForearm:177,leftUpperArm:-10,leftForearm:5,handRight:'relaxed',headTilt:6,expression:'concerned'}),
P('listen','Mendengar dengan perhatian','three_quarter',['emosi','berdiri'],{headTilt:-8,bodyLean:3,rightUpperArm:9,rightForearm:-4,expression:'neutral'}),
P('ask_question','Bertanya dengan satu tapak terbuka','front',['emosi','penerangan'],{leftUpperArm:-36,leftForearm:-106,handLeft:'open',headTilt:8,expression:'surprised'}),
P('read_book','Membaca buku terbuka','three_quarter',['prop','buku'],{leftUpperArm:13,leftForearm:71,rightUpperArm:-13,rightForearm:-71,headTilt:6,handLeft:'grip',handRight:'grip',prop:'book',propAttachment:'both_hands'}),
P('use_phone','Melihat telefon di tangan','three_quarter',['prop','telefon'],{rightUpperArm:8,rightForearm:-137,leftUpperArm:-8,leftForearm:5,headTilt:8,handRight:'grip',prop:'phone',propAttachment:'right_hand'}),
P('call_phone','Menelefon dengan sopan','three_quarter',['prop','telefon'],{rightUpperArm:40,rightForearm:-163,handRight:'grip',headTilt:5,prop:'phone',propAttachment:'right_hand'}),
P('type_laptop','Menaip pada komputer riba','side',['prop','komputer'],{...seated,leftUpperArm:32,leftForearm:83,rightUpperArm:27,rightForearm:88,handLeft:'open',handRight:'open',headTilt:4,prop:'laptop',propAttachment:'desk',secondaryProp:'chair'}),
P('carry_box','Memegang kotak dengan dua tangan','front',['prop','kotak'],{leftUpperArm:12,leftForearm:82,rightUpperArm:-12,rightForearm:-82,handLeft:'grip',handRight:'grip',prop:'box',propAttachment:'both_hands'}),
P('reach_forward','Menghulur tangan ke hadapan','side',['capaian','tangan'],{bodyLean:8,rightUpperArm:58,rightForearm:86,handRight:'open',headTilt:-3}),
P('pick_low','Mencapai objek rendah dengan lutut lembut','three_quarter',['capaian','rendah'],{rootX:-(184*Math.sin(16*rad)+159*Math.sin(-14*rad)),rootY:343-184*Math.cos(16*rad)-159*Math.cos(-14*rad),leftThigh:16,rightThigh:16,leftShin:-14,rightShin:-14,bodyLean:14,rightUpperArm:7,rightForearm:28,leftUpperArm:-17,leftForearm:-22,handRight:'grip',headTilt:5}),
P('sit_upright','Duduk tegak di kerusi','side',['duduk','kerusi'],{...seated,leftUpperArm:7,leftForearm:62,rightUpperArm:8,rightForearm:66}),
P('sit_relaxed','Duduk santai dengan tangan di paha','side',['duduk','kerusi'],{...seated,bodyLean:-5,headTilt:4,leftUpperArm:16,leftForearm:78,rightUpperArm:18,rightForearm:81}),
P('sit_read','Duduk sambil membaca','side',['duduk','buku'],{...seated,leftUpperArm:22,leftForearm:92,rightUpperArm:17,rightForearm:97,handLeft:'grip',handRight:'grip',headTilt:7,prop:'book',propAttachment:'both_hands',secondaryProp:'chair'}),
P('kneel','Melutut sebelah lutut','three_quarter',['melutut','rendah'],{...kneel,leftUpperArm:-4,leftForearm:10,rightUpperArm:18,rightForearm:73}),
P('kneel_reach','Melutut sambil menghulur tangan','three_quarter',['melutut','capaian'],{...kneel,bodyLean:10,rightUpperArm:58,rightForearm:86,leftUpperArm:-12,leftForearm:4,handRight:'open'}),
P('walk_contact_left','Langkah berjalan: kaki kiri menyentuh','three_quarter',['kunci_berjalan','langkah'],{...walkState(0,false)}),
P('walk_contact_right','Langkah berjalan: kaki kanan menyentuh','three_quarter',['kunci_berjalan','langkah'],{...walkState(.5,false)}),
P('walk_pass_left','Langkah berjalan: kaki kiri melintas','three_quarter',['kunci_berjalan','langkah'],{...walkState(.75,false)}),
P('walk_pass_right','Langkah berjalan: kaki kanan melintas','three_quarter',['kunci_berjalan','langkah'],{...walkState(.25,false)}),
P('run_contact_left','Kunci joging perlahan: kiri','three_quarter',['kunci_joging','langkah'],{...walkState(0,false),leftUpperArm:-25,leftForearm:65,rightUpperArm:25,rightForearm:120,bodyLean:7}),
P('run_contact_right','Kunci joging perlahan: kanan','three_quarter',['kunci_joging','langkah'],{...walkState(.5,false),leftUpperArm:25,leftForearm:110,rightUpperArm:-25,rightForearm:55,bodyLean:7}),
P('arms_folded','Tangan bersilang longgar','front',['berdiri','tangan'],{leftUpperArm:5,leftForearm:103,rightUpperArm:-5,rightForearm:-103,handLeft:'relaxed',handRight:'relaxed',headTilt:-3}),
P('celebrate','Gembira dengan dua tangan diangkat','front',['emosi','tangan'],{leftUpperArm:-52,leftForearm:-156,rightUpperArm:52,rightForearm:156,handLeft:'open',handRight:'open',expression:'happy',headTilt:-4}),
P('stand_back','Berdiri menghadap belakang (pandangan belakang penuh)','back',['asas','berdiri','belakang'],{view:'back'}),
P('look_sky_back','Memandang langit/ufuk dari belakang','back',['emosi','belakang','reflektif'],{view:'back',headTilt:-6}),
P('walk_side_right','Melangkah profil sisi menghadap kanan','side_right',['kunci_berjalan','sisi_kanan'],{...walkState(0,false),view:'side_right'}),
P('walk_side_left','Melangkah profil sisi menghadap kiri','side_left',['kunci_berjalan','sisi_kiri'],{...walkState(0,false),view:'side_left'}),
P('sit_side_eat','Duduk di meja makan & minum (profil sisi kanan)','side_right',['duduk','makan','sisi_kanan'],{...seated,view:'side_right',rightUpperArm:45,rightForearm:105,handRight:'grip',prop:'meal',secondaryProp:'chair',mealLift:0,mealUtensil:'spoon'}),
P('call_phone_left','Menelefon menghadap suku kiri (telefon di telinga)','three_quarter_left',['prop','telefon','suku_kiri'],{view:'three_quarter_left',rightUpperArm:40,rightForearm:-163,handRight:'grip',headTilt:4,prop:'phone',propAttachment:'right_hand'}),
P('dua_stand','Berdiri menadah kedua-dua tapak tangan berdoa','three_quarter_right',['ibadah','doa','tangan'],{view:'three_quarter_right',leftUpperArm:22,leftForearm:108,rightUpperArm:28,rightForearm:112,handLeft:'open',handRight:'open',headTilt:5}),
P('dua_sit','Melutut rendah sambil menadah tangan berdoa','three_quarter_right',['ibadah','doa','duduk'],{...kneel,view:'three_quarter_right',leftUpperArm:22,leftForearm:108,rightUpperArm:28,rightForearm:112,handLeft:'open',handRight:'open',headTilt:5}),
P('touch_lanyard','Memegang tali lanyard / kad kerja di dada','front',['emosi','pekerja','tangan'],{view:'front',rightUpperArm:-28,rightForearm:-115,handRight:'open',headTilt:6,expression:'concerned'}),
P('wipe_tear','Mengelap air mata dengan hujung lengan baju','front',['emosi','sebak','tangan'],{view:'front',rightUpperArm:35,rightForearm:155,handRight:'open',headTilt:6,expression:'concerned'})
];
const POSES=Object.freeze(poseRecords.map(({state,...m})=>Object.freeze({...m,prop:state.prop||null})));
const poseMap=new Map(poseRecords.map(x=>[x.id,x]));
const M=(id,label,duration,loop,view,tags,prop=null)=>({id,label,duration,loop,view,tags,prop});
const MOTIONS=Object.freeze([
M('idle_breathe','Diam hidup: pernafasan dan kelipan',4,true,'front',['asas','gelung']),
M('wave_hello','Angkat tangan, melambai dan kembali',4,false,'front',['salam','tangan']),
M('nod_yes','Mengangguk setuju',2.8,false,'three_quarter',['kepala','emosi']),
M('shake_no','Menggeleng perlahan',3,false,'front',['kepala','emosi']),
M('explain_one_hand','Penerangan dengan satu tangan',4.8,false,'three_quarter',['penerangan','tangan']),
M('explain_two_hands','Penerangan dengan dua tangan berurutan',5,false,'front',['penerangan','tangan']),
M('point_left','Menunjuk ke kiri dan kembali',3.8,false,'front',['tunjuk','tangan']),
M('point_right','Menunjuk ke kanan dan kembali',3.8,false,'front',['tunjuk','tangan']),
M('point_up','Menunjuk ke atas dan kembali',3.8,false,'front',['tunjuk','tangan']),
M('shrug','Mengangkat bahu dan tapak tangan',3.6,false,'front',['emosi','tangan']),
M('celebrate_gentle','Meraikan dengan gerakan terkawal',4,false,'front',['emosi','tangan']),
M('think','Berhenti, berfikir dan kembali',4.5,false,'three_quarter',['emosi','tangan']),
M('reach_forward','Bersedia, menghulur dan menarik tangan',4,false,'side',['capaian','tangan']),
M('pick_up_phone','Mencapai, menggenggam dan melihat telefon',5,false,'three_quarter',['prop','telefon'],'phone'),
M('read_book','Membaca buku dengan alihan perhatian',6,true,'three_quarter',['prop','buku','gelung'],'book'),
M('type_laptop','Menaip dengan gerakan jari dan kepala',5,true,'side',['prop','komputer','gelung'],'laptop'),
M('carry_box','Mengangkat dan menahan kotak',5,false,'front',['prop','kotak'],'box'),
M('walk_in_place','Berjalan setempat pada permukaan bergerak',2.4,true,'three_quarter',['berjalan','gelung']),
M('walk_across','Berjalan dua kitaran merentas skrin',6.4,false,'three_quarter',['berjalan','alih_posisi']),
M('step_side','Melangkah ke sisi dan kembali',4,false,'front',['langkah','alih_posisi']),
M('sit_down','Membengkokkan lutut lalu duduk',4.5,false,'side',['duduk','kerusi'],'chair'),
M('stand_up','Bangun dari kerusi dan seimbang',4.5,false,'side',['duduk','kerusi'],'chair'),
M('kneel_down','Turun melutut dengan sebelah lutut',5,false,'three_quarter',['melutut','rendah']),
M('look_around','Memerhati kiri, kanan lalu kembali',4.8,false,'front',['kepala','perhatian']),
M('turn_back_to_front','Berpusing badan dan kepala dari belakang ke hadapan',3.6,false,'back',['pusing_badan','alih_sudut']),
M('turn_left_to_right','Berpusing badan dan kepala dari suku kiri ke suku kanan',3.2,false,'three_quarter_left',['pusing_badan','alih_sudut']),
M('walk_side_right','Berjalan profil sisi menghadap kanan sepenuhnya',2.4,true,'side_right',['berjalan','sisi_kanan','gelung']),
M('walk_side_left','Berjalan profil sisi menghadap kiri sepenuhnya',2.4,true,'side_left',['berjalan','sisi_kiri','gelung']),
M('sigh_tired','Mengeluh penat dengan bahu jatuh dan helaan nafas',4.0,false,'front',['emosi','penat','nafas']),
M('wipe_tears_sleeve','Mengangkat lengan baju mengelap air mata yang bergenang',3.8,false,'front',['emosi','sebak','tangan']),
M('sit_eat_drink','Duduk di meja menyuap makanan dan menghirup minuman',4.5,true,'side_right',['duduk','makan','gelung'],'meal'),
M('dua_khusyuk','Menadah kedua-dua tapak tangan berdoa dengan khusyuk',5.0,true,'three_quarter_right',['ibadah','doa','gelung']),
M('call_phone_converse','Berbual di telefon dengan anggukan kepala dan gerakan mulut',4.5,true,'three_quarter_left',['prop','telefon','dialog-contoh','gelung'],'phone'),
M('ride_motorcycle','Menunggang motosikal kapcai memegang handlebar',3.0,true,'side_right',['kenderaan','motor','gelung'],'motorcycle')
].map(Object.freeze));
const motionMap=new Map(MOTIONS.map(x=>[x.id,x]));
function getPose(id){const p=POSES.find(p=>p.id===id);if(!p)throw new RangeError(`Pose tidak dikenali: ${id}`);return p}
function getMotion(id){const m=motionMap.get(id);if(!m)throw new RangeError(`Gerakan tidak dikenali: ${id}`);return m}
function state(overrides={}){return {...copy(BASE_STATE),...copy(overrides)}}
function mergeState(a,b){return {...a,...copy(b),contacts:b.contacts?copy(b.contacts):copy(a.contacts)}}
function blendStates(a,b,t){const s=t<=0?copy(a):t>=1?copy(b):copy(t<.5?a:b);for(const k of NUMBERS)s[k]=mix(Number(a[k])||0,Number(b[k])||0,t);return s}
function transitionState(from,to,tSeconds,duration=.6){if(!Number.isFinite(tSeconds)||!Number.isFinite(duration)||duration<=0)throw new TypeError('Masa dan tempoh mesti nombor terhingga; tempoh > 0.');return blendStates(from,to,smooth(tSeconds/duration))}
function adapted(s,c={}){s=copy(s);const age=Number(c.age)||30,f=age>=65?.87:age<13?.96:1;for(const k of ['leftUpperArm','leftForearm','rightUpperArm','rightForearm'])s[k]=mix(BASE_STATE[k],s[k],f);s.bodyLean*=f;s.headTilt*=f;return s}
function poseState(id,c={}){getPose(id);const p=poseMap.get(id);return constrainArms(adapted(state({...p.state,view:p.view,pose:id}),c),c,id,null)}
function ageTempo(c={}){const age=Number(c.age)||30;return age>=65?1.2:age<13?1.04:age<20?.96:1}
function durationForCharacter(id,c={}){return getMotion(id).duration*ageTempo(c)}
function pulse(u,start,end){if(u<=start||u>=end)return 0;return Math.sin(PI*(u-start)/(end-start))**2}
function env(u,a=.15,b=.78){if(u<a)return smooth(u/a);if(u>b)return 1-smooth((u-b)/(1-b));return 1}
function sequence(u,keys){if(u<=keys[0][0])return state(keys[0][1]);for(let i=1;i<keys.length;i++)if(u<=keys[i][0])return blendStates(state(keys[i-1][1]),state(keys[i][1]),smooth((u-keys[i-1][0])/(keys[i][0]-keys[i-1][0])));return state(keys[keys.length-1][1])}
function gesture(u,poseId,{anticipation={},end={},hold=.7}={}){return sequence(u,[[0,{}],[.11,anticipation],[.34,poseMap.get(poseId).state],[hold,poseMap.get(poseId).state],[1,end]])}
function inverseLeg(x,y){const a=184,b=159,d=clamp(Math.hypot(x,y),Math.abs(a-b)+1e-6,a+b-1e-6),theta=Math.atan2(x,y),alpha=Math.acos(clamp((a*a+d*d-b*b)/(2*a*d),-1,1)),beta=Math.acos(clamp((b*b+d*d-a*a)/(2*b*d),-1,1));return {thigh:(theta+alpha)*deg,shin:(theta-beta)*deg}}
function gaitFoot(q){q=((q%1)+1)%1;if(q<.5)return{x:24-96*q,y:0,stance:true};const u=(q-.5)*2;return{x:-24-48*u+288*u*u-192*u*u*u,y:-22*Math.sin(PI*u)**2,stance:false}}
function walkState(phase,across){const l=gaitFoot(phase),r=gaitFoot(phase+.5),li=inverseLeg(l.x,339+l.y),ri=inverseLeg(r.x,339+r.y),swing=Math.sin(2*PI*phase);return {rootX:across?phase*96:0,rootY:4,leftThigh:li.thigh,leftShin:li.shin,rightThigh:ri.thigh,rightShin:ri.shin,footLeft:0,footRight:0,leftUpperArm:-10+12*swing,leftForearm:5+7*swing,rightUpperArm:10-12*swing,rightForearm:5-7*swing,bodyLean:2,headTilt:-1,contacts:{left:l.stance,right:r.stance,ground_mode:across?'fixed':'treadmill',left_kind:'foot',right_kind:'foot',ground_velocity:across?0:-40},view:'three_quarter'}}
function plantBoth(s){const yL=184*Math.cos(s.leftThigh*rad)+159*Math.cos(s.leftShin*rad),yR=184*Math.cos(s.rightThigh*rad)+159*Math.cos(s.rightShin*rad);s.rootY=343-Math.max(yL,yR);if(Math.abs(s.leftThigh-s.rightThigh)<1e-7&&Math.abs(s.leftShin-s.rightShin)<1e-7)s.rootX=-(184*Math.sin(s.leftThigh*rad)+159*Math.sin(s.leftShin*rad));return s}
function blinkAt(u){return pulse(u,.18,.22)+pulse(u,.69,.73)}
function sampleMotion(id,tSeconds,c={},options={}){
  const m=getMotion(id);if(!Number.isFinite(tSeconds))throw new TypeError('tSeconds mesti nombor terhingga.');
  const duration=durationForCharacter(id,c),loop=options.loop===undefined?m.loop:Boolean(options.loop);
  const phase=loop&&!m.loop?((tSeconds/duration)%2+2)%2:((tSeconds/duration)%1+1)%1;
  let u=loop?(m.loop?phase:phase<=1?phase:2-phase):clamp(tSeconds/duration),s=state({view:m.view}),w=env(u),v=2*PI*u;
  switch(id){
    case 'idle_breathe': s.bodyLean=.55*Math.sin(v);s.headTilt=.7*Math.sin(v+.35);s.leftUpperArm=-10+.65*Math.sin(v);s.rightUpperArm=10-.65*Math.sin(v);s.breath=.5-.5*Math.cos(v);break;
    case 'wave_hello':s=gesture(u,'wave_hello',{anticipation:{rightUpperArm:4,rightForearm:-8,headTilt:2},hold:.76});s.rightForearm+=12*Math.sin(8*PI*u)*env(u,.34,.72);break;
    case 'nod_yes':s.headTilt=8*Math.sin(4*PI*u)*Math.sin(PI*u)**2;s.expression=u>.18&&u<.82?'happy':'neutral';break;
    case 'shake_no':s.headTilt=7*Math.sin(6*PI*u)*Math.sin(PI*u)**2;s.headYaw=14*Math.sin(4*PI*u)*Math.sin(PI*u)**2;break;
    case 'explain_one_hand':s=gesture(u,'explain_one_hand',{anticipation:{rightUpperArm:4,rightForearm:-6},hold:.76});s.rightForearm+=8*Math.sin(4*PI*u)*env(u,.34,.74);s.headTilt+=2*Math.sin(2*PI*u)*w;break;
    case 'explain_two_hands':s=sequence(u,[[0,{}],[.12,{leftUpperArm:-4,rightUpperArm:4}],[.32,{leftUpperArm:-34,leftForearm:-82,handLeft:'open',rightUpperArm:22,rightForearm:55,handRight:'open'}],[.53,poseMap.get('explain_two_hands').state],[.76,{leftUpperArm:-29,leftForearm:-73,rightUpperArm:39,rightForearm:95,handLeft:'open',handRight:'open'}],[1,{}]]);break;
    case 'point_left':case 'point_right':case 'point_up':s=gesture(u,id,{anticipation:{bodyLean:id==='point_left'?2:-2,headTilt:2},hold:.75});break;
    case 'shrug':s=gesture(u,'ask_question',{anticipation:{headTilt:-2},hold:.7});s=mergeState(s,{rightUpperArm:mix(10,36,w),rightForearm:mix(0,106,w),handRight:w>.4?'open':'relaxed',bodyLean:0});s.shoulderLift=6*w;break;
    case 'celebrate_gentle':s=gesture(u,'celebrate',{anticipation:{leftUpperArm:-3,rightUpperArm:3,headTilt:3},hold:.7});s.headTilt+=2*Math.sin(4*PI*u)*w;break;
    case 'think':s=gesture(u,'think',{anticipation:{headTilt:3},hold:.8});s.headTilt+=1.5*Math.sin(4*PI*u)*w;break;
    case 'reach_forward':s=gesture(u,'reach_forward',{anticipation:{bodyLean:-3,rightUpperArm:2,rightForearm:-5},hold:.66});break;
    case 'pick_up_phone':s=sequence(u,[[0,{}],[.12,{bodyLean:-2}],[.38,{...poseMap.get('pick_low').state,handRight:'open'}],[.48,{...poseMap.get('pick_low').state,handRight:'grip',prop:'phone',propAttachment:'right_hand'}],[.76,poseMap.get('use_phone').state],[1,poseMap.get('use_phone').state]]);s=plantBoth(s);s.prop=u<.45?'phone':'phone';s.propAttachment=u<.48?'scene_low':'right_hand';s.contacts={left:true,right:true,ground_mode:'fixed',left_kind:'foot',right_kind:'foot'};break;
    case 'read_book':s=state(poseMap.get('read_book').state);s.headTilt+=1.3*Math.sin(v);s.leftForearm+=1.4*Math.sin(v);s.rightForearm-=1.4*Math.sin(v);s.gazeX=3*Math.sin(v);break;
    case 'type_laptop':s=state(poseMap.get('type_laptop').state);s.leftForearm+=1.5*Math.sin(16*PI*u);s.rightForearm+=1.5*Math.sin(16*PI*u+PI);s.headTilt+=1.8*(1-Math.cos(2*PI*u));s.fingerTapLeft=.5-.5*Math.cos(16*PI*u);s.fingerTapRight=.5+.5*Math.cos(16*PI*u);break;
    case 'carry_box':s=sequence(u,[[0,{...poseMap.get('pick_low').state,prop:'box',propAttachment:'scene_low',handLeft:'open',handRight:'open'}],[.18,{...poseMap.get('pick_low').state,leftForearm:53,rightForearm:-53,handLeft:'grip',handRight:'grip',prop:'box',propAttachment:'both_hands'}],[.62,poseMap.get('carry_box').state],[1,poseMap.get('carry_box').state]]);s=plantBoth(s);break;
    case 'walk_in_place':s=state(walkState(u,false));s.contacts.ground_velocity=-96/duration;break;
    case 'walk_across':{const phase=2*smooth(u);s=state(walkState(phase,true));s.contacts.ground_velocity=0;break}
    case 'step_side':{const p=u<.5?smooth(u*2):1-smooth((u-.5)*2),lift=u<.5?pulse(u,0,.5):pulse(u,.5,1),root=40*p;const footL=0,footR=80*p;const li=inverseLeg(footL-root,339),ri=inverseLeg(footR-root,339-16*lift);s=state({rootX:root,rootY:4,leftThigh:li.thigh,leftShin:li.shin,rightThigh:ri.thigh,rightShin:ri.shin,leftUpperArm:-10-5*lift,rightUpperArm:10+5*lift,contacts:{left:true,right:lift<1e-8,ground_mode:'fixed',left_kind:'foot',right_kind:'foot'}});break}
    case 'sit_down':case 'stand_up':{const p=id==='sit_down'?smooth(u):1-smooth(u),angle=90*p;s=state({...seated,leftThigh:angle,rightThigh:angle,leftShin:0,rightShin:0,bodyLean:12*Math.sin(PI*p),leftUpperArm:mix(-10,7,p),leftForearm:62*p,rightUpperArm:mix(10,8,p),rightForearm:66*p});s=plantBoth(s);s.rootX=-184*Math.sin(angle*rad);s.contacts={left:true,right:true,ground_mode:'fixed',left_kind:'foot',right_kind:'foot',seat:p>.98};s.prop='chair';s.propAttachment='scene';break}
    case 'kneel_down':{if(u<.24){const p=smooth(u/.24),root=50*p,lift=14*Math.sin(PI*p)**2,li=inverseLeg(-root,339),ri=inverseLeg(100*p-root,339-lift);s=state({rootX:root,rootY:4,leftThigh:li.thigh,leftShin:li.shin,rightThigh:ri.thigh,rightShin:ri.shin,bodyLean:3*Math.sin(PI*p),contacts:{left:true,right:p<1e-8||p>1-1e-8,ground_mode:'fixed',left_kind:'foot',right_kind:'foot'}})}else{const p=smooth((u-.24)/.76),li0=inverseLeg(-50,339),ri0=inverseLeg(50,339),leftThigh=mix(li0.thigh,0,p),leftShin=mix(li0.shin,-90,p),rightShin=mix(ri0.shin,0,p),leftY=184*Math.cos(leftThigh*rad)+159*Math.cos(leftShin*rad),lift=12*Math.sin(PI*p)**2,rootY=343-leftY-lift,rightThigh=Math.acos(clamp((343-rootY-159*Math.cos(rightShin*rad))/184,-1,1))*deg,rootX=100-184*Math.sin(rightThigh*rad)-159*Math.sin(rightShin*rad);s=state({...kneel,rootX,rootY,leftThigh,leftShin,rightThigh,rightShin,footLeft:-90*p,bodyLean:8*Math.sin(PI*p),leftUpperArm:mix(-10,-4,p),leftForearm:10*p,rightUpperArm:mix(10,18,p),rightForearm:73*p,contacts:{left:p>1-1e-8,right:true,ground_mode:'fixed',left_kind:p>1-1e-8?'knee':'swing',right_kind:'foot'}})}break}
    case 'look_around':s=sequence(u,[[0,{}],[.24,{headTilt:5}],[.58,{headTilt:-6}],[.8,{headTilt:2}],[1,{}]]);s.headYaw=12*Math.sin(2*PI*u)*Math.sin(PI*u)**2;s.gazeX=8*Math.sin(2*PI*u)*Math.sin(PI*u)**2;break;
    case 'turn_back_to_front':s=state({view:u<.42?'back':(u<.72?'side_right':'front'),turnScaleX:1-.88*Math.exp(-(((u-.42)/.065)**2))-.88*Math.exp(-(((u-.72)/.065)**2)),bodyLean:3*Math.sin(PI*u),headTilt:4*Math.sin(PI*u)});break;
    case 'turn_left_to_right':s=state({view:u<.5?'three_quarter_left':'three_quarter_right',turnScaleX:1-.88*Math.exp(-(((u-.5)/.065)**2)),bodyLean:4*Math.sin(PI*u),headYaw:10*Math.cos(PI*u)});break;
    case 'walk_side_right':s=state({...walkState(u,false),view:'side_right'});s.contacts.ground_velocity=-96/duration;break;
    case 'walk_side_left':s=state({...walkState(u,false),view:'side_left'});s.contacts.ground_velocity=96/duration;break;
    case 'sigh_tired':{const sigh=Math.sin(PI*u);s=state({view:'front',expression:'concerned',bodyLean:-4.5*sigh,headTilt:10*sigh,shoulderLift:-6*sigh,breath:1.4*sigh});break}
    case 'wipe_tears_sleeve':s=gesture(u,'wipe_tear',{anticipation:{headTilt:4},hold:.75});s.expression='concerned';s.tear=env(u,.25,.82);break;
    case 'sit_eat_drink':{const lift=.5-.5*Math.cos(4*PI*u);s=state({...seated,view:'side_right',expression:'happy',headTilt:4-6*lift,rightUpperArm:35+25*lift,rightForearm:75+45*lift,handRight:'grip',mouthOpen:lift>.7?.45:.1,prop:'meal',secondaryProp:'chair',mealLift:lift,mealUtensil:u<.5?'spoon':'cup'});break}
    case 'dua_khusyuk':{const br=Math.sin(2*PI*u);s=state({view:'three_quarter_right',headTilt:5+1.5*br,leftUpperArm:22,leftForearm:108+3*br,rightUpperArm:28,rightForearm:112+3*br,handLeft:'open',handRight:'open',breath:.8*br});break}
    case 'call_phone_converse':{const nod=Math.sin(4*PI*u)*3.5;s=state({...poseMap.get('call_phone_left').state,view:'three_quarter_left',expression:'happy',headTilt:nod,mouthOpen:.3+.35*Math.abs(Math.sin(6*PI*u))});break}
    case 'ride_motorcycle':{const vib=Math.sin(12*PI*u)*1.2;s=state({...seated,view:'side_right',bodyLean:6,headTilt:2,leftShin:20,rightShin:20,handLeft:'grip',handRight:'grip',rootY:110+vib,prop:'motorcycle',secondaryProp:null,wheelPhase:2*PI*u,contacts:{left:true,right:true,ground_mode:'vehicle',left_kind:'peg',right_kind:'peg'}});break}
  }
  s=adapted(s,c);if(!id.startsWith('turn_'))s.view=m.view;s=constrainArms(s,c,id,u);s.motion=id;s.time=tSeconds;s.duration=duration;s.progress=u;s.loopMode=loop?(m.loop?'repeat':'ping_pong'):'once';
  // Expressions use authored emotion only; no fabricated speech or narration.
  s.blink=blinkAt(u);s.mouthOpen=Number(s.mouthOpen)||0;
  s.contacts=s.contacts||copy(BASE_STATE.contacts);
  return s;
}
// Solve contacts using each character's authored arm lengths; children keep shorter reaches.
function armBasis(c,s){
  const canonical=s.view.startsWith('side_')?'side':s.view.startsWith('three_quarter_')?'three_quarter':s.view;
  const g=require('./character_renderer.cjs').geometry(c,{view:canonical});
  const rot=P=>{const x=P[0]-300,y=P[1]-568,co=Math.cos(s.bodyLean*rad),si=Math.sin(s.bodyLean*rad);return [300+co*x-si*y+s.rootX,568+si*x+co*y+s.rootY]};
  return {g,shoulder:{left:rot(g.landmarks.shoulder_left),right:rot(g.landmarks.shoulder_right)}};
}
function solveArm(origin,target,a,b,side,view){const dx=target[0]-origin[0],dy=target[1]-origin[1],d=clamp(Math.hypot(dx,dy),Math.abs(a-b)+.001,a+b-.001),bearing=Math.atan2(dy,dx),off=Math.acos(clamp((a*a+d*d-b*b)/(2*a*d),-1,1)),ang=bearing+(side==='left'||view.startsWith('side')?off:-off),E=[origin[0]+a*Math.cos(ang),origin[1]+a*Math.sin(ang)];return {upper:Math.atan2(E[0]-origin[0],E[1]-origin[1])*deg,lower:Math.atan2(target[0]-E[0],target[1]-E[1])*deg}}
function constrainArms(s,c,id,u){
  const relevant=['read_book','use_phone','call_phone','type_laptop','carry_box','sit_read','think','arms_folded','pick_low','pick_up_phone','call_phone_left','call_phone_converse','dua_stand','dua_sit','dua_khusyuk','sit_side_eat','sit_eat_drink','ride_motorcycle','touch_lanyard','wipe_tear','wipe_tears_sleeve'];if(!relevant.includes(id))return s;
  const {g,shoulder}=armBasis(c,s),targets={};
  function goal(side,P,w=1){targets[side]={P,w}}
  if(id==='read_book'){goal('left',[250,480]);goal('right',[350,480])}
  if(id==='sit_read'){goal('left',[420,720]);goal('right',[500,720])}
  if(id==='type_laptop'){const tap=u===null?0:1.6*Math.sin(16*PI*u);goal('left',[440,650+tap]);goal('right',[480,650-tap])}
  if(id==='use_phone')goal('right',[365,465]);
  if(['call_phone','call_phone_left','call_phone_converse'].includes(id)){s.propAngle=180;s.rightUpperArmScale=.55;const head=g.landmarks.head;goal('right',[365,head[1]+55])}
  if(id==='think'){const weight=u===null?1:env(u,.34,.8),head=g.landmarks.head;s.rightUpperArmScale=mix(1,(Number(c.age)||30)<13?.86:.65,weight);goal('right',[320,head[1]+g.segments.head_height*.43+38],weight)}
  if(id==='arms_folded'){goal('left',[350,425]);goal('right',[250,445])}
  if(id==='pick_low')goal('right',[460,620]);
  if(id==='pick_up_phone'){
    const P=u<.48?[460,620]:[mix(460,365,smooth((u-.48)/.28)),mix(620,465,smooth((u-.48)/.28))];goal('right',P,u<.38?smooth((u-.12)/.26):1);s.propX=460;s.propY=620;
  }
  if(id==='carry_box'){
    if(u===null){goal('left',[225,560]);goal('right',[375,560])}
    else{const lift=smooth((u-.18)/.44),y=mix(610,560,lift),weight=smooth(u/.18);goal('left',[225,y],weight);goal('right',[375,y],weight);s.propX=300;s.propY=610;s.propAttachment=u<.18?'scene_low':'both_hands';s.handLeft=u<.18?'open':'grip';s.handRight=u<.18?'open':'grip';}
  }
  if(['dua_stand','dua_sit','dua_khusyuk'].includes(id)){s.handAngleLeft=165;s.handAngleRight=-165;goal('left',[245,320+s.rootY]);goal('right',[355,320+s.rootY])}
  if(['sit_side_eat','sit_eat_drink'].includes(id)){const head=g.landmarks.head;const lift=s.mealLift||0;s.rightUpperArmScale=mix(1,.7,lift);goal('left',[435,650]);goal('right',[mix(500,390,lift),mix(630,head[1]+s.rootY+90,lift)])}
  if(id==='ride_motorcycle'){goal('left',[490,570]);goal('right',[520,570])}
  if(id==='touch_lanyard'){s.lanyard=true;goal('right',[315,430])}
  if(['wipe_tear','wipe_tears_sleeve'].includes(id)){const w=u===null?1:env(u,.3,.78);s.rightUpperArmScale=mix(1,.62,w);goal('right',[360,g.landmarks.head[1]+80],w);s.tear=w}
  for(const [side,{P,w}]of Object.entries(targets)){const sol=solveArm(shoulder[side],P,g.segments['upper_arm_'+side]*(s[side+'UpperArmScale']||1),g.segments['forearm_'+side],['call_phone','call_phone_left','call_phone_converse'].includes(id)?'left':side,s.view);s[side+'UpperArm']=mix(s[side+'UpperArm'],sol.upper,w);const lower=id==='think'&&sol.lower<0?sol.lower+360:sol.lower;s[side+'Forearm']=mix(s[side+'Forearm'],lower,w)}
  if(id==='pick_up_phone')s.propAngle=smooth((u-.48)/.28)*s.rightForearm;
  return s;
}
function anklePositions(s){const angle=k=>(Number(s[k])||0)*rad;return {left:{x:(Number(s.rootX)||0)-31+184*Math.sin(angle('leftThigh'))+159*Math.sin(angle('leftShin')),y:568+(Number(s.rootY)||0)+184*Math.cos(angle('leftThigh'))+159*Math.cos(angle('leftShin'))},right:{x:(Number(s.rootX)||0)+33+184*Math.sin(angle('rightThigh'))+159*Math.sin(angle('rightShin')),y:568+(Number(s.rootY)||0)+184*Math.cos(angle('rightThigh'))+159*Math.cos(angle('rightShin'))}}}
const CONTROL_SCHEMA={units:'SVG user units; angle degrees',frame:{viewBox:[0,0,600,1000],pelvis:[300,568],ground_ankle_y:911,thigh_length:184,shin_length:159},angle_convention:'0 = down; +90 = screen-right; -90 = screen-left. Limb angles global; headTilt relative torso. bodyLean positive moves shoulders screen-right.',numeric:NUMBERS,projection_scales:'leftUpperArmScale/rightUpperArmScale are unitless foreshortening; default1. Phone and chin poses project an upper arm in depth to keep elbows below the face.',optional_numeric:['breath','headYaw','gazeX','shoulderLift','fingerTapLeft','fingerTapRight','propX','propY','propAngle'],hands:['relaxed','open','point','grip'],expressions:['neutral','happy','concerned','surprised'],props:['phone','book','box','laptop','chair','meal','motorcycle'],contacts:'left/right booleans; ground_mode fixed or treadmill; left_kind/right_kind foot/knee/swing; seat optional. treadmill velocity SVG units/second.'};
module.exports={POSES,MOTIONS,BASE_STATE,CONTROL_SCHEMA,poseState,sampleMotion,durationForCharacter,getPose,getMotion,transitionState,blendStates,anklePositions,smooth,inverseLeg,gaitFoot};
if(require.main===module){const fs=require('fs'),path=require('path');const out=path.join(__dirname,'motion_catalog.json');fs.writeFileSync(out,JSON.stringify({schema_version:1,language:'ms-MY',title:'Bank 42 Pose dan 34 Gerakan untuk 20 Watak',poses:POSES,motions:MOTIONS,controls:CONTROL_SCHEMA,usage:{pose:'poseState(poseId, character)',motion:'sampleMotion(motionId, seconds, character, {loop:false})',duration:'durationForCharacter(motionId, character)',transition:'transitionState(previousState, nextState, seconds, duration): use for compatible standing gestures. For posture changes use dedicated sit_down/stand_up/kneel_down clips to preserve foot contacts.',looping:'Native loop actions repeat with matching seams. Explicit loop:true on finite actions uses a continuous ping-pong over 2 x duration to avoid pose jumps.',clock:'Sample from frameIndex / fps. No wall-clock animation or unseeded randomness.',age:'Elders: duration x1.20, arm/head/body amplitude x0.87. Children: duration x1.04, amplitude x0.96. Teens: duration x0.96. Legs retain IK contact geometry.',walk_in_place:'Uses a moving-ground treadmill convention. For fixed-world foot contacts use walk_across.',scope:'34 authored action recipes, 42 authored key poses. New V3 actions have no bundled pre-rendered clip bank; export on demand. Optional secondary controls are enhancement hooks; renderer may ignore these without losing primary action. No speech/lip-sync is synthesized.'}},null,2)+'\n');process.stdout.write(out+'\n')}
