"""Genera reporte-qa.html consolidando tests, cobertura y revision de seguridad."""
import subprocess, re, datetime, pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[3]

def correr(cmd):
    r = subprocess.run(cmd, shell=True, cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.stdout or "") + (r.stderr or "")

salida_tests = correr("python -m pytest -q")
m = re.search(r"(\d+) passed", salida_tests)
pasaron = int(m.group(1)) if m else 0
m = re.search(r"(\d+) failed", salida_tests)
fallaron = int(m.group(1)) if m else 0

salida_cov = correr("python -m pytest --cov=src --cov-report=term-missing -q")
m = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", salida_cov)
cobertura = int(m.group(1)) if m else 0

hallazgos = []
patron_secreto = re.compile(r"(?i)(api[_-]?key|password|passwd|secret|token)\s*=\s*[\"'][^\"']{6,}[\"']")
patron_except = re.compile(r"except\s*:")
for py in (RAIZ / "src").rglob("*.py"):
    texto = py.read_text(encoding="utf-8", errors="replace")
    for n, linea in enumerate(texto.splitlines(), 1):
        if patron_secreto.search(linea):
            hallazgos.append(("Secreto expuesto", py.name + ":" + str(n), "Mover el valor a una variable de entorno"))
        if patron_except.search(linea):
            hallazgos.append(("Manejo de excepciones", py.name + ":" + str(n), "Capturar una excepcion especifica"))

ok = fallaron == 0 and cobertura >= 80 and not hallazgos
veredicto = "APROBADO" if ok else "REQUIERE CORRECCION"
color = "#1a7f37" if ok else "#b42318"
fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

filas = "".join("<tr><td>{}</td><td><code>{}</code></td><td>{}</td></tr>".format(c, d, s) for c, d, s in hallazgos)
if not filas:
    filas = '<tr><td colspan="3">Sin hallazgos</td></tr>'

css = """
body{font-family:Segoe UI,sans-serif;max-width:820px;margin:40px auto;padding:0 20px;color:#1f2328}
h1{margin-bottom:4px} .fecha{color:#656d76;font-size:14px}
.veredicto{color:#fff;padding:14px 20px;border-radius:8px;font-size:20px;font-weight:600;margin:24px 0}
table{border-collapse:collapse;width:100%;margin:12px 0 28px}
th,td{border:1px solid #d0d7de;padding:8px 12px;text-align:left;font-size:14px}
th{background:#f6f8fa} code{background:#f6f8fa;padding:1px 5px;border-radius:4px}
.m{display:inline-block;background:#f6f8fa;border:1px solid #d0d7de;border-radius:8px;padding:12px 18px;margin-right:12px}
.m b{display:block;font-size:26px}
"""

html = """<!doctype html><html lang="es"><meta charset="utf-8">
<title>Reporte de calidad</title>
<style>{css}</style>
<h1>Reporte de calidad</h1>
<div class="fecha">Generado el {fecha}</div>
<div class="veredicto" style="background:{color}">{veredicto}</div>
<div class="m"><b>{pasaron}</b>tests pasados</div>
<div class="m"><b>{fallaron}</b>tests fallidos</div>
<div class="m"><b>{cobertura}%</b>cobertura</div>
<h2>Revision de seguridad</h2>
<table><tr><th>Caso</th><th>Donde</th><th>Correccion sugerida</th></tr>{filas}</table>
<h2>Criterio del veredicto</h2>
<p>Se aprueba si no hay tests fallidos, la cobertura es 80% o mas, y no hay hallazgos de seguridad.</p>
</html>""".format(css=css, fecha=fecha, color=color, veredicto=veredicto, pasaron=pasaron, fallaron=fallaron, cobertura=cobertura, filas=filas)

(RAIZ / "reporte-qa.html").write_text(html, encoding="utf-8")
print("Veredicto: {} | {} pasados, {} fallidos, {}% cobertura, {} hallazgos".format(veredicto, pasaron, fallaron, cobertura, len(hallazgos)))