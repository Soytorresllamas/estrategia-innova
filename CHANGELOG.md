# Registro de cambios — Gantt Estrategia Innova

Historial de cambios del artefacto, como respaldo y referencia. Cada bloque
corresponde a un commit en GitHub (`Soytorresllamas/estrategia-innova`).
Formato inspirado en [Keep a Changelog](https://keepachangelog.com/es/).

> **Recuperación rápida:** todo el código está versionado en git/GitHub. Los
> **datos en vivo** (tareas que editan los usuarios) viven en Supabase, no en
> git — por eso se guardan *snapshots* en [`backups/`](backups/). Ver
> «Cómo restaurar» al final.

---

## Configuración clave (para no perder el hilo)

- **Repo:** https://github.com/Soytorresllamas/estrategia-innova
- **Sitio en vivo:** https://soytorresllamas.github.io/estrategia-innova/
- **Despliegue:** GitHub Actions → Pages (`.github/workflows/deploy.yml`). Cada
  push a `main` publica en ~1-2 min. (El builder *legacy*/Jekyll se descartó
  porque fallaba con el JSX `{{...}}`; hay `.nojekyll` por si acaso.)
- **Persistencia:** Supabase, proyecto `siwiluoxrjnqjnrufbjl`, tabla
  `gantt_state` (un registro `id='innova-default'` con `data` JSONB =
  `{ tasks, config }`). RLS **abierto** (anónimo lee/escribe). Esquema en
  [`supabase_setup.sql`](supabase_setup.sql).
- **Acceso a la app:** pantalla de login con usuarios **Alejandro** y
  **Ricardo** (contraseña guardada como hash SHA-256 en `index.html`, no en
  texto plano). Es un candado ligero del lado del cliente, no seguridad fuerte.
- **Tablero de pruebas (staging):** abrir la app con **`?board=staging`**
  (ej. `…/estrategia-innova/?board=staging`) usa una fila aislada
  `innova-staging` con su propio caché local y muestra un distintivo amarillo.
  Sirve para probar sin tocar los datos reales (`innova-default`). Para
  re-clonar staging desde prod, copiar el `data` de `innova-default` a
  `innova-staging` con un `UPDATE` (o reusar el script de respaldo).
- **Archivo principal:** `index.html` (autocontenido: React + Babel + supabase-js por CDN).

---

## 2026-06-24

Toda la construcción ocurrió en un día, en estos hitos:

### Despliegue confiable vía GitHub Actions — `8695092`
- **Cambiado:** el despliegue de GitHub Pages pasó del builder *legacy* (Jekyll)
  a un workflow de **GitHub Actions** que publica los archivos estáticos tal cual.
- **Porqué:** el builder legacy fallaba intermitentemente (su parser Liquid se
  atraganta con el JSX `style={{...}}`) y dejaba el sitio congelado en una
  versión vieja; los cambios no llegaban a producción aunque sí al repo.

### Arreglo: logo deformado — `e6a76ab`
- **Corregido:** el logo se estiraba a lo ancho. Se agregó `align-self:flex-start`
  para que el `<img>` respete su proporción dentro del contenedor flex en columna.

### Icono de exportación más claro — `ca911ff`
- **Cambiado:** el botón de exportar usa el icono `file-spreadsheet` de Lucide
  (archivo con celdas), en verde Excel. Reemplaza el cuadro con «X» previo.

### `.nojekyll` — `480366c`
- **Agregado:** archivo `.nojekyll` para que Pages no procese el HTML con Jekyll.

### Exportación: solo Excel/CSV — `4f3c92c`
- **Eliminado:** botón y función de exportar a JSON.
- **Cambiado:** el botón de CSV quedó como icono (export a hoja de cálculo).

### Inicio en julio + acordeón — `f2afccf`
- **Cambiado:** todas las fechas del plan se desplazaron +1 mes; el horizonte
  ahora arranca en **julio 2026** (jul 2026 – mar 2027).
- **Agregado:** control de **acordeón** (esquina del encabezado) que colapsa o
  expande todos los grupos a la vez.

### Logo Hotmarketing — `1904645`
- **Agregado:** logo de Hotmarketing en el header y en la pantalla de login.
  Se recortó el fondo crema del PNG a transparente (`hotmarketing-logo.png`).

### Login, persistencia y edición — `97e193f`
- **Agregado:** pantalla de acceso (usuarios Alejandro/Ricardo, contraseña con
  hash SHA-256).
- **Agregado:** persistencia en **Supabase** (carga al abrir + autoguardado),
  con `localStorage` de respaldo e indicador de sincronización.
- **Agregado:** botón de **papelera** por fila para quitar tareas.
- **Cambiado:** «Restablecer» se movió al pie y exige escribir `RESTABLECER`.
- **Cambiado:** todo el texto de la interfaz creció ×1.25.

### Versión inicial — `693a797`
- **Creado:** Gantt interactivo de la *Estrategia de Marketing Grupo Innova*.
  Roadmap maestro 2026: 5 niveles del Plan de Acción (priorizado por ROI) como
  fases con fechas sugeridas editables + sprint Open House Cluster Borgoña.
- Arrastrar para reprogramar, editar, agrupar por Nivel/Canal, zoom, filtros,
  % de avance, hitos, exportación y autoguardado. Estilo «Marfil editorial»
  (serif Fraunces + acento terracota).

---

## Cómo restaurar

**Restaurar el código:** está todo en git. Para volver a un punto:
`git checkout <hash> -- index.html` (o clonar el repo de nuevo).

**Restaurar los datos (tareas) en Supabase** desde un snapshot de `backups/`:
- `backups/latest.json` = estado más reciente. `backups/gantt-state-AAAA-MM-DD.json`
  = historial por día. **El contenido del archivo es directamente el objeto `data`**
  (`{ config, tasks }`), listo para pegar.
1. Abrir el snapshot que quieras restaurar y copiar todo su contenido.
2. En Supabase → SQL Editor del proyecto `siwiluoxrjnqjnrufbjl`, ejecutar:
   ```sql
   update public.gantt_state
   set data = '<pega-aquí-el-contenido-del-archivo>'::jsonb, updated_at = now()
   where id = 'innova-default';
   ```
   (O usar el botón **Restablecer** de la app para volver al plan original de fábrica.)

**Respaldo automático:** un GitHub Action (`.github/workflows/backup.yml`) corre a
diario (09:00 UTC) y guarda un snapshot nuevo en `backups/` solo si los datos
cambiaron. También se puede correr a mano desde la pestaña **Actions** del repo.

**Generar un nuevo snapshot de respaldo** (cuando quieras):
```bash
curl -s "https://siwiluoxrjnqjnrufbjl.supabase.co/rest/v1/gantt_state?select=*&id=eq.innova-default" \
  -H "apikey: <publishable-key>" -H "Authorization: Bearer <publishable-key>" \
  | python3 -m json.tool > "backups/gantt-state-$(date +%F).json"
```
