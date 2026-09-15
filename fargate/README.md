# Demo de AWS Fargate con contenedores — Curso de AWS para principiantes

Tres ejemplos para empezar, de menos a más. Todo en la región **us-east-1**.

| Ejemplo | Qué se hace | Qué hace falta |
|---|---|---|
| 1 · Un contenedor que ya existe | Correr la imagen pública de nginx en Fargate | Solo la consola |
| 2 · Tu propio contenedor | Construir esta app, subirla a ECR y correrla | CloudShell (trae Docker) |
| 3 · Que no se caiga | Un servicio de ECS que mantiene 2 tareas y reemplaza la que muere | Lo del ejemplo 2 |

## Archivos

- `app.py` — la aplicación (Flask). Muestra la versión, la tarea que atendió y un contador por tarea.
- `requirements.txt` — las librerías.
- `Dockerfile` — la receta del contenedor, comentada línea por línea.
- `subir_imagen.sh` — crea el repositorio de ECR, construye la imagen y la sube.

## Ejemplo 2, en CloudShell

```bash
git clone https://github.com/jjjfrancia/demo-apprunner-curso-aws.git
cd demo-apprunner-curso-aws/fargate
bash subir_imagen.sh v1
```

Al final imprime la URI de la imagen para pegarla en la definición de tarea
(puerto del contenedor **8080**, variable de entorno `VERSION=v1`).

## En AWS Academy

Donde la consola pide **rol de ejecución de tareas**, elige `LabRole`: la cuenta no deja crear roles.

## Al terminar

1. Servicio → Actualizar → tareas deseadas **0** → luego Eliminar servicio.
2. Detener las tareas sueltas del ejemplo 1.
3. Eliminar el clúster.
4. ECR → repositorio `demo-fargate` → Eliminar (las imágenes guardadas también cobran).

---
Curso de Amazon Web Services para principiantes — por **Joel Francia** · CortexGovernor Academy
