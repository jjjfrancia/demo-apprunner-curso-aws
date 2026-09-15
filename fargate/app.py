# -*- coding: utf-8 -*-
"""
Demostración de AWS Fargate — Curso de AWS para principiantes
CortexGovernor Academy · por Joel Francia

Qué demuestra esta aplicación:

Corre DENTRO DE UN CONTENEDOR. La misma imagen corre igual en tu computadora, en
CloudShell y en Fargate. Cada tarea de Fargate es una copia de este contenedor, con su
propio nombre de máquina: si pones dos tareas detrás de un balanceador y recargas, verás
cambiar la fila «Tarea que te atendió». Y la versión sale de una variable de entorno que
se pone en la definición de tarea, sin tocar el código.
"""
import os
import socket
import time
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

ARRANQUE = time.time()
VISITAS = {"n": 0}

PAGINA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hola desde Fargate — demostración del curso</title>
<style>
:root{--bg:#f4f7fb;--card:#fff;--bd:#b9c9de;--tx:#16202e;--mut:#5b6b80;
      --acc:#14448f;--ok:#0f766e;--warn:#b45309;--aws:#ec7211}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);line-height:1.6;
     font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif}
.wrap{max-width:880px;margin:0 auto;padding:48px 24px 80px}
h1{font-size:40px;margin:0 0 8px;color:#0b1b33}
h1 .hl{color:var(--aws)}
.sub{color:var(--mut);font-size:18px;margin:0 0 8px}
.marca{font-size:14px;color:var(--mut);margin:0 0 32px}
.marca b{color:var(--acc)}
.card{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:24px 26px;margin:20px 0}
.card h2{font-size:18px;margin:0 0 16px;color:var(--acc)}
.fila{display:flex;justify-content:space-between;align-items:center;gap:16px;
      padding:11px 0;border-top:1px solid #e6ecf4;font-size:15px}
.fila:first-of-type{border-top:0}
.fila .k{color:var(--mut)}
.fila .v{font-family:Consolas,Monaco,monospace;font-weight:700;text-align:right;word-break:break-all}
.big{font-size:26px;color:var(--ok)}
.ver{display:inline-block;padding:3px 14px;border-radius:999px;background:#fff7ed;color:var(--aws)}
button{background:var(--acc);color:#fff;border:0;border-radius:10px;padding:13px 26px;
       font-size:15px;font-weight:700;cursor:pointer;font-family:inherit}
.nota{background:#e5eefb;border-left:4px solid var(--acc);border-radius:10px;
      padding:14px 18px;margin:18px 0;font-size:14.5px}
.nota.ok{background:#e7f5f2;border-color:var(--ok)}
.nota.warn{background:#fdf3e3;border-color:var(--warn)}
table{width:100%;border-collapse:collapse;font-size:14.5px;margin-top:8px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid #e6ecf4;vertical-align:top}
th{color:var(--mut);font-weight:700}
code{background:#eef3fa;padding:1px 6px;border-radius:4px;font-size:13.5px}
.pie{margin-top:36px;padding-top:20px;border-top:1px solid var(--bd);
     color:var(--mut);font-size:13px;text-align:center}
</style>
</head>
<body>
<div class="wrap">

  <h1>Hola desde un contenedor en <span class="hl">Fargate</span></h1>
  <p class="sub">Esta página la sirve un contenedor. No hay ninguna máquina que sea tuya.</p>
  <p class="marca">Demostración del curso de AWS · <b>CortexGovernor™ Academy</b></p>

  <div class="card">
    <h2>Lo que este contenedor sabe de sí mismo</h2>
    <div class="fila"><span class="k">Versión de la imagen</span>
      <span class="v"><span class="ver">{{ version }}</span></span></div>
    <div class="fila"><span class="k">Tarea que te atendió</span><span class="v">{{ tarea }}</span></div>
    <div class="fila"><span class="k">Visitas atendidas por ESTA tarea</span>
      <span class="v big">{{ visitas }}</span></div>
    <div class="fila"><span class="k">Lleva encendida</span><span class="v">{{ encendida }}</span></div>
    <div class="fila"><span class="k">Hora del contenedor (UTC)</span><span class="v">{{ hora }}</span></div>
    <div style="margin-top:18px"><button onclick="location.reload()">Recargar</button></div>
  </div>

  <div class="nota ok">
    <b>La versión no está escrita en el código.</b> Sale de la variable de entorno
    <code>VERSION</code> que pusiste en la definición de tarea. Cambias la variable, creas una
    revisión nueva y actualizas el servicio: la imagen es la misma.
  </div>

  <div class="card">
    <h2>La misma aplicación, en dos sitios</h2>
    <table>
      <tr><th style="width:34%"></th><th style="width:33%">App Runner</th><th style="width:33%">Fargate</th></tr>
      <tr><td><b>Qué le entregas</b></td><td>El repositorio</td><td>Una imagen de contenedor</td></tr>
      <tr><td><b>Quién construye</b></td><td>App Runner, solo</td><td>Tú, con <code>docker build</code></td></tr>
      <tr><td><b>Dirección https</b></td><td>Incluida</td><td>La pones tú, con un balanceador</td></tr>
      <tr><td><b>Varias piezas distintas</b></td><td>Un servicio por app</td><td>Web, trabajador y tareas programadas en el mismo clúster</td></tr>
      <tr><td><b>Control de red</b></td><td>Poco</td><td>Subredes, grupos de seguridad, IP pública o privada</td></tr>
    </table>
  </div>

  <div class="nota warn">
    <b>Al terminar la clase:</b> pon el servicio en 0 tareas y bórralo, borra el clúster y el
    repositorio de ECR. Una tarea encendida factura por segundo aunque nadie entre.
  </div>

  <p class="pie">
    Curso de Amazon Web Services para principiantes — por <b>Joel Francia</b><br>
    CortexGovernor™ Academy · powered by DiscoveryFast
  </p>
</div>
</body>
</html>
"""


def _encendida():
    s = int(time.time() - ARRANQUE)
    if s < 60:
        return "%d segundos" % s
    if s < 3600:
        return "%d min %d s" % (s // 60, s % 60)
    return "%d h %d min" % (s // 3600, (s % 3600) // 60)


@app.route("/")
def inicio():
    VISITAS["n"] += 1
    return render_template_string(
        PAGINA,
        version=os.getenv("VERSION", "v1"),
        tarea=socket.gethostname(),
        visitas=VISITAS["n"],
        encendida=_encendida(),
        hora=datetime.now(timezone.utc).strftime("%H:%M:%S"),
    )


@app.route("/salud")
def salud():
    """El balanceador llama aquí para saber si la tarea está sana."""
    return jsonify(estado="ok", version=os.getenv("VERSION", "v1"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
