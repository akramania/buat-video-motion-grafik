#!/usr/bin/env python3
"""Narrate the approved eight-door film with Malaysian Malay male neural TTS."""
import argparse
import asyncio
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import wave

import numpy as np

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
WORK=OUT/'voiceover_work'
WORK.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'tts_deps'))
VOICE='ms-MY-OsmanNeural'
RATE='-5%'
SR=44100
SECTIONS=[
 ('Pembukaan',0,12,
  'Petang itu, aku memandang baki dalam telefon. Semakin kecil angkanya, semakin sempit rasanya hidup. Tapi burung di atas wayar itu, tenang sahaja.'),
 ('Dijamin Allah',12,16,
  'Pintu pertama, rezeki yang dijamin Allah. Setiap makhluk dalam pemeliharaan-Nya. Burung keluar mencari makan. Kita pun belajar percaya, sambil terus berikhtiar.'),
 ('Berusaha',28,16,
  'Pintu kedua, usaha. Kalau burung pun terbang mencari makan, kita juga perlu bergerak. Langkah kecil hari ini tetap sebuah usaha. Tawakal dan ikhtiar berjalan bersama.'),
 ('Bersyukur',44,16,
  'Pintu ketiga, syukur. Ada roti yang sederhana, tetapi ada hati yang bersyukur. Hargailah yang kita miliki. Allah menjanjikan tambahan nikmat kepada hamba-Nya yang bersyukur.'),
 ('Takwa dan tawakal',60,16,
  'Pintu keempat, takwa dan tawakal. Kadang-kadang, jalan di hadapan nampak buntu. Jaga langkah dan pilihan kita. Serahkan hasil kepada Allah. Jalan keluar boleh datang dari arah yang tidak disangka.'),
 ('Istighfar',76,16,
  'Pintu kelima, istighfar. Astaghfirullah. Kita mohon ampun, lalu perbaiki diri. Dalam Surah Nuh, istighfar dikaitkan dengan hujan dan kurniaan Allah. Sentiasalah kembali kepada-Nya dengan penuh harapan.'),
 ('Menikah',92,16,
  'Pintu keenam, menikah. Dua insan membina hidup bersama. Ada tanggungjawab, ada saling menguatkan. Teruskan merancang dan berusaha. Kurnia Allah itu luas, menurut hikmah-Nya.'),
 ('Anak',108,16,
  'Pintu ketujuh, anak. Mereka ialah amanah yang perlu dijaga. Kita berusaha, merancang dan membesarkan mereka sebaiknya. Allah mengingatkan bahawa Dialah yang memberi rezeki kepada mereka dan kepada kita.'),
 ('Sedekah',124,16,
  'Pintu kelapan, sedekah. Hulurkan yang mampu dengan hati yang ikhlas. Kebaikan kecil boleh bergerak dari tangan ke tangan. Apa yang diberi, Allah menggantikannya, menurut kehendak dan hikmah-Nya.'),
 ('Penutup dan doa',140,20,
  'Rezeki lebih luas daripada wang. Ketenangan, kasih sayang dan peluang berbuat baik juga kurniaan-Nya. Ya Allah, berkatilah rezeki yang Engkau beri. Cukupkan kami dengan yang halal. Amin.'),
]


def run(cmd):
    subprocess.run(cmd,check=True)


def duration(path):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'format=duration','-of','default=nw=1:nk=1',str(path)]))


async def synthesize():
    import edge_tts
    from edge_tts import communicate
    # Trust the runtime's installed root CA while retaining TLS verification.
    ca=os.environ.get('SSL_CERT_FILE')
    if ca:communicate._SSL_CTX.load_verify_locations(cafile=ca)
    sem=asyncio.Semaphore(3)
    async def one(i,section):
        path=WORK/f'voice_{i:02}.mp3'
        if path.exists() and path.stat().st_size>1000:
            print('Reusing',i,section[0],flush=True);return
        async with sem:
            events=[]
            c=edge_tts.Communicate(section[3],voice=VOICE,rate=RATE,boundary='WordBoundary')
            with path.open('wb') as stream:
                async for event in c.stream():
                    if event['type']=='audio':stream.write(event['data'])
                    else:events.append(event)
            (WORK/f'voice_{i:02}_boundaries.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
            print('Generated',i,section[0],round(duration(path),2),'s',flush=True)
    await asyncio.gather(*(one(i,s) for i,s in enumerate(SECTIONS)))


def compose():
    durations=[duration(WORK/f'voice_{i:02}.mp3') for i in range(len(SECTIONS))]
    # Keep the voice at its natural rate; stretch all visuals by one factor so
    # the music tempo and the animation tempo remain internally consistent.
    required=max((v+1.8)/s[2] for v,s in zip(durations,SECTIONS))
    scale=max(1.25,math.ceil(required*20)/20)
    length=160*scale
    voice=np.zeros(round(length*SR),np.float32)
    manifest=[]
    for i,(section,secs) in enumerate(zip(SECTIONS,durations)):
        name,original_start,original_len,words=section
        raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(WORK/f'voice_{i:02}.mp3'),
            '-af','highpass=f=75','-ac','1','-ar',str(SR),'-f','f32le','pipe:1'])
        samples=np.frombuffer(raw,dtype='<f4').copy()
        active=samples[np.abs(samples)>.015]
        rms=float(np.sqrt(np.mean(active**2))) if len(active) else .1
        gain=min(.14/max(rms,.001),.85/max(float(np.max(np.abs(samples))),.001))
        samples*=gain
        at=original_start*scale+.85
        first=round(at*SR)
        assert first+len(samples)<=round((original_start+original_len)*scale*SR),name
        voice[first:first+len(samples)]+=samples
        manifest.append({'section':name,'start':round(original_start*scale,3),
            'end':round((original_start+original_len)*scale,3),'voice_start':round(at,3),
            'voice_duration':secs,'text':words})
    stem=WORK/'narration.wav'
    pcm=np.clip(voice*32767,-32768,32767).astype('<i2')
    with wave.open(str(stem),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
    manifest_path=WORK/'voiceover_manifest.json'
    manifest_path.write_text(json.dumps({'voice':VOICE,'rate':RATE,'scale':scale,'duration':length,'scenes':manifest},ensure_ascii=False,indent=2))
    script=OUT/'8_Pintu_Rezeki_Skrip_Voiceover_BM.txt'
    def tc(v):
        return f'{int(v)//60:02}:{int(v)%60:02}'
    lines=['8 PINTU REZEKI | NARASI LELAKI BAHASA MELAYU',
           f'Suara: Microsoft Osman Neural (ms-MY). Kadar: {RATE}.',
           f'Tempoh video: {tc(length)}. Terjemahan Al-Quran kekal pada skrin.',
           'Narasi ini ialah penerangan cerita, bukan bacaan teks terjemahan penuh.','']
    for s in manifest:lines.extend([f'{tc(s["start"])}–{tc(s["end"])} | {s["section"]}',s['text'],''])
    script.write_text('\n'.join(lines),encoding='utf-8')
    print('TIMING',json.dumps({'scale':scale,'length':length,'durations':durations}),flush=True)
    base=WORK/'approved_base_160s.mp4'
    target=OUT/'8_Pintu_Rezeki_Voiceover_Lelaki_BM.mp4'
    if not base.exists():shutil.copy2(OUT/'8_Pintu_Rezeki_Animasi_Cerita_160s_9x16.mp4',base)
    temp=WORK/'narrated_final.mp4'
    graph=(f'[0:v]setpts={scale}*(PTS-STARTPTS),fps=24[v];'
           f'[1:a]atempo={1/scale},volume=0.6[bed];'
           '[2:a]asplit=2[narration][trigger];'
           '[bed][trigger]sidechaincompress=threshold=0.020:ratio=8:attack=40:release=550[ducked];'
           '[ducked][narration]amix=inputs=2:normalize=0:duration=longest,'
           'loudnorm=I=-16:TP=-1.5:LRA=9[a]')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(base),
         '-i',str(OUT/'8_Pintu_Rezeki_music_sfx_160s.wav'),'-i',str(stem),
         '-filter_complex',graph,'-map','[v]','-map','[a]',
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','192k','-ar',str(SR),'-ac','2','-t',str(length),
         '-movflags','+faststart',str(temp)])
    shutil.copyfile(temp,target)
    run(['ffmpeg','-v','error','-y','-i',str(stem),'-af','loudnorm=I=-16:TP=-1.5:LRA=9',
         '-ar',str(SR),'-c:a','libmp3lame','-b:a','192k',str(OUT/'8_Pintu_Rezeki_Voiceover_Lelaki_BM.mp3')])
    print('FINAL',target,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--synthesize',action='store_true');p.add_argument('--compose',action='store_true')
    args=p.parse_args()
    if args.synthesize:asyncio.run(synthesize())
    if args.compose:compose()
