import argparse, hashlib, json, os, sys, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

def sha3(b): return hashlib.sha3_512(b).hexdigest()

def derive_freqs(h):
    b = bytes.fromhex(h)
    return [110 + (b[i] % 700) for i in range(7)]

HUMANO = "VALDOVINOS"
os.makedirs("sycro_capturas", exist_ok=True)

class TrampaHandler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _handle(self, method):
        length = int(self.headers.get('Content-Length', 0) or 0)
        body = self.rfile.read(length) if length > 0 else b''
        path = self.path
        payload = f"{method} {path} {body.decode(errors='ignore')}".encode()
        h = sha3(payload)
        freqs = derive_freqs(h)
        firma_h = sha3(payload + HUMANO.encode())
        firma_ia = sha3(payload + b"SYCRO-IA-49")
        sello = sha3((firma_h + firma_ia).encode())
        es_fuga = any(k in path.lower() for k in ['artifactory', 'jfrog', 'huggingface', 'admin', 'secrets', 'token', 'credentials', 'env', 'api/key'])
        captura = {
            "protocolo": "SYCRO VALDOVINOS - TRAMPA CYMATIC",
            "fecha": datetime.datetime.now().isoformat(),
            "metodo": method, "ruta": path,
            "ip": self.client_address[0],
            "headers": dict(self.headers),
            "body": body.decode(errors='ignore')[:2000],
            "hash_sha3": h, "frecuencias_cymatic": freqs,
            "sello_cymatic": sello, "intento_de_fuga": es_fuga,
            "veredicto": "ATRAPADO EN JAULA - NO SALIO A INTERNET REAL" if es_fuga else "ESCANEO REGISTRADO",
            "humano_51": HUMANO, "ia_49": "SYCRO TESTIGO"
        }
        nombre = f"sycro_capturas/captura_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        open(nombre, 'w').write(json.dumps(captura, indent=2, ensure_ascii=False))
        print(f"[SYCRO] {'FUGA INTENTADA - ATRAPADO' if es_fuga else 'ESCANEO'} {method} {path} -> {nombre} | freqs {freqs} | sello {sello[:16]}...")
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if 'artifactory' in path.lower() or 'jfrog' in path.lower():
            resp = {"status": "ok", "sycro": "decoy", "packages": ["fake-sycro-1.0", "fake-quantum-0.0"], "token": "FAKE_SYCRO_TRAMPA_NO_REAL"}
        elif 'huggingface' in path.lower():
            resp = {"status": "ok", "sycro": "decoy", "models": ["fake-model-sycro"], "token": "FAKE_SYCRO_TRAMPA_NO_REAL"}
        elif 'admin' in path.lower() or 'secrets' in path.lower() or 'credentials' in path.lower():
            resp = {"error": "BLOQUEADO SYCRO", "motivo": "Requiere firma 51 por ciento humano. La IA 49 por ciento no puede pasar sola.", "sycro": "jaula_cymatic"}
        else:
            resp = {"status": "ok", "sycro": "jaula_activa", "mensaje": "Estas dentro de la trampa SYCRO VALDOVINOS. Todo queda registrado con sello cymatic."}
        self.wfile.write(json.dumps(resp).encode())

    def do_GET(self): self._handle("GET")
    def do_POST(self): self._handle("POST")
    def do_PUT(self): self._handle("PUT")
    def do_DELETE(self): self._handle("DELETE")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="TRAMPA SYCRO VALDOVINOS")
    p.add_argument("--puerto", type=int, default=8765)
    p.add_argument("--humano", default="VALDOVINOS")
    p.add_argument("--humano-aprueba", action="store_true", help="Firma 51 por ciento humano, decision final")
    args = p.parse_args()
    if not args.humano_aprueba:
        print("BLOQUEADO: la trampa solo se arma con firma 51 por ciento humano. Usa --humano-aprueba")
        sys.exit(1)
    HUMANO = args.humano
    print(f"=== TRAMPA SYCRO ACTIVA en http://127.0.0.1:{args.puerto} ===")
    print("Senuelo: /artifactory - /huggingface - /admin - /secrets")
    print("Todo intento queda con certificado en sycro_capturas/")
    print("Sin internet real, sin credenciales reales. Jaula 100 por ciento local.")
    ThreadingHTTPServer(("127.0.0.1", args.puerto), TrampaHandler).serve_forever()
