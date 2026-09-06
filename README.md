# Demo de AWS App Runner — Curso de AWS para principiantes

Aplicacion minima en Flask para la demostracion en clase de **AWS App Runner**.

Muestra en pantalla un contador de visitas, la hora del servidor y el nombre de la
maquina que atendio la peticion: son datos que **calcula el programa en AWS**, no el
navegador. Es el contraste con la demo anterior (S3 + CloudFront), donde no se
ejecutaba nada del lado del servidor.

## Como se despliega

1. Consola de AWS -> **App Runner** -> **Create service**
2. Source: **Source code repository** -> **Add new** -> *Install & Authorize AWS Connector for GitHub*
3. Repositorio: este. Branch: `main`. Deployment trigger: **Automatic**
4. Configure build: **Use a configuration file** (lee `apprunner.yaml`)
5. Nombre del servicio, 1 vCPU / 2 GB -> **Create & deploy**

A los ~5 minutos entrega una URL `https://xxxx.awsapprunner.com` con certificado incluido.

`apprunner.yaml` ya trae el runtime, el comando de arranque y el puerto 8080.

## Al terminar la clase

App Runner cobra por tener la aplicacion encendida aunque nadie entre.
Consola -> App Runner -> el servicio -> **Actions** -> **Delete**.

---
Curso de Amazon Web Services para principiantes — por **Joel Francia**
CortexGovernor Academy
