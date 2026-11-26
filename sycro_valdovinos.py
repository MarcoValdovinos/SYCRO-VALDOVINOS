import argparse, hashlib, json, math, os, struct, sys, wave, datetime

def sha3(b): return hashlib.sha3_512(b).hexdigest()

def derive_freqs(h):
    b = bytes.fromhex(h)
    return [110 + (b[i] % 700) for i in range(7)]

def gen_mandala(freqs, out):
    try:
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        theta = np.linspace(0, 2*np.pi, 3000)
        r = np.ones_like(theta)
        for i, f in enumerate(freqs):
            r += 0.22*np.sin((f/60)*theta + i*1.3)
            r += 0.12*np.cos((f/90)*theta - i*0.7)
        r = abs(r)
        fig = plt.figure(figsize=(8,8), dpi=150)
        fig.patch.set_facecolor('black')
        ax = fig.add_subplot(111, projection='polar')
        ax.set_facecolor('black')
        ax.plot(theta, r, color='#00F0FF', linewidth=1.1, alpha=0.95)
        ax.plot(theta+0.15, r*0.92, color='#FF00E5', linewidth=0.9, alpha=0.7)
        ax.plot(theta-0.12, r*1.05, color='#FFD700', linewidth=0.7, alpha=0.6)
        ax.set_yticklabels([]); ax.set_xticklabels([]); ax.grid(False)
        ax.set_ylim(0, r.max()*1.15)
        plt.tight_layout()
        plt.savefig(out, facecolor='black', bbox_inches='tight')
        plt.close()
        return out
    except Exception as e:
        print(f"[SYCRO] Mandala PNG omitido, el HTML sigue vivo: {e}")
        return None

def gen_wav(freqs, out):
    sr = 44100; dur = 3; n = sr*dur; data = []
    for i in range(n):
        t = i/sr
        v = sum(math.sin(2*math.pi*f*t + j) for j, f in enumerate(freqs)) / len(freqs)
        v *= 0.6 * math.sin(math.pi*t/dur)
        data.append(int(v*32767))
    with wave.open(out, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b''.join(struct.pack('<h', x) for x in data))
    return out

def gen_html(freqs, titulo, h, sello, humano, out):
    tpl = """<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>__TITULO__</title><style>body{margin:0;background:#000;color:#fff;font-family:monospace;overflow:hidden}canvas{position:fixed;inset:0}.panel{position:fixed;left:12px;bottom:12px;background:rgba(0,0,0,.72);padding:12px;border:1px solid #00F0FF;border-radius:12px;max-width:92vw;font-size:12px;line-height:1.5}.bar{display:flex;height:14px;border:1px solid #fff;margin:8px 0}.h51{width:51%;background:#00F0FF}.a49{width:49%;background:#FF00E5}b{color:#00F0FF}</style></head><body><canvas id='c'></canvas><div class='panel'><b>__TITULO__</b><br>SYCRO VALDOVINOS - CO-CREATIVIDAD SIMBIOTICA CYMATIC CUANTICA<br><div class='bar'><div class='h51'></div><div class='a49'></div></div>51 por ciento HUMANO __HUMANO__ / 49 por ciento IA SYCRO<br>HASH: __HASH__<br>SELLO: __SELLO__<br>Toca para pantalla completa, el mandala reacciona en vivo.</div><script>const FREQS=__FREQS__; const cv=document.getElementById('c'); const ctx=cv.getContext('2d'); let W,H,t=0; function rs(){W=cv.width=innerWidth;H=cv.height=innerHeight} rs(); addEventListener('resize',rs); document.body.onclick=()=>{if(document.documentElement.requestFullscreen) document.documentElement.requestFullscreen()}; function fr(){t+=0.012; ctx.fillStyle='rgba(0,0,0,0.15)'; ctx.fillRect(0,0,W,H); ctx.save(); ctx.translate(W/2,H/2-40); for(let k=0;k<3;k++){ctx.beginPath(); for(let i=0;i<=700;i++){let th=i/700*Math.PI*2; let r=90; for(let f of FREQS){r+=16*Math.sin(f/60*th+t+k)} let x=Math.cos(th)*r*1.3; let y=Math.sin(th)*r*1.3; if(i==0)ctx.moveTo(x,y); else ctx.lineTo(x,y)} ctx.strokeStyle=k==0?'#00F0FF':k==1?'#FF00E5':'#FFD700'; ctx.lineWidth=1.2; ctx.stroke()} ctx.restore(); requestAnimationFrame(fr)} fr();</script></body></html>"""
    html = tpl.replace("__TITULO__", titulo).replace("__HUMANO__", humano).replace("__HASH__", h[:32]+"...").replace("__SELLO__", sello[:32]+"...").replace("__FREQS__", json.dumps(freqs))
    open(out, 'w', encoding='utf-8').write(html)
    return out

def crear(args):
    if not args.humano_aprueba:
        print("BLOQUEADO SYCRO: falta firma 51 por ciento humano. La IA 49 por ciento no puede publicar sola.")
        print("Usa --humano-aprueba para firmar tu decision final.")
        sys.exit(1)
    if not os.path.exists(args.archivo):
        print(f"No existe: {args.archivo}"); sys.exit(1)
    data = open(args.archivo, 'rb').read()
    h = sha3(data)
    freqs = derive_freqs(h)
    firma_humano = sha3(data + args.humano.encode())
    firma_ia = sha3(data + b"SYCRO-IA-49-VALDOVINOS")
    sello = sha3((firma_humano + firma_ia).encode())
    os.makedirs("sycro_salida", exist_ok=True)
    cert = {
        "protocolo": "CO-CREATIVIDAD SIMBIOTICA CYMATIC CUANTICA SYCRO VALDOVINOS",
        "titulo": args.titulo, "humano_51": args.humano, "ia_49": "SYCRO",
        "hash_sha3_512": h, "frecuencias_cymatic": freqs,
        "firma_humano_51": firma_humano, "firma_ia_49": firma_ia,
        "sello_cymatic": sello, "fecha": datetime.datetime.now().isoformat(),
        "regla": "Sin firma 51 por ciento humano, el 49 por ciento IA no ejecuta ni publica. Verificable por cualquiera."
    }
    open("sycro_salida/certificado.json", "w").write(json.dumps(cert, indent=2, ensure_ascii=False))
    gen_mandala(freqs, "sycro_salida/sello_cymatic.png")
    gen_wav(freqs, "sycro_salida/huella_cymatic.wav")
    gen_html(freqs, args.titulo, h, sello, args.humano, "sycro_salida/certificado.html")
    print("=== SYCRO VALDOVINOS 51-49 CREADO ===")
    print(f"Titulo: {args.titulo}")
    print(f"Hash: {h[:32]}...")
    print(f"Frecuencias: {freqs}")
    print(f"Sello: {sello[:32]}...")
    print("Archivos en sycro_salida/: certificado.json, sello_cymatic.png, huella_cymatic.wav, certificado.html")

def verificar(args):
    cert = json.load(open(args.verificar))
    data = open(args.original, 'rb').read()
    h = sha3(data)
    ok = (h == cert["hash_sha3_512"])
    print(f"Hash coincide: {ok}")
    print(f"Protocolo: {cert['protocolo']}")
    print(f"51 por ciento Humano: {cert['humano_51']} / 49 por ciento IA: {cert['ia_49']}")
    print(f"Sello: {cert['sello_cymatic'][:32]}...")
    print("VERIFICADO SYCRO 51-49" if ok else "ALTERADO: el mandala y el sonido ya no coinciden")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="SYCRO VALDOVINOS 51-49")
    p.add_argument("--archivo", help="Archivo a certificar")
    p.add_argument("--titulo", default="OBRA SYCRO VALDOVINOS")
    p.add_argument("--humano", default="VALDOVINOS")
    p.add_argument("--humano-aprueba", action="store_true", help="Firma 51 por ciento humano, decision final")
    p.add_argument("--verificar", help="Ruta a certificado.json")
    p.add_argument("--original", help="Archivo original para verificar")
    args = p.parse_args()
    if args.verificar:
        verificar(args)
    else:
        crear(args)
