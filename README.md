# Estrategia de Marketing — Grupo Innova · Gantt interactivo

Herramienta de planeación visual (Gantt) para la **Estrategia de Marketing de Grupo Innova**, desarrollo residencial de lujo en León, Guanajuato (perfil UHNW). Un solo archivo HTML autocontenido, sin build ni dependencias instalables.

## ▶️ Demo en vivo

**https://soytorresllamas.github.io/estrategia-innova/**

> La primera carga requiere conexión a internet (React y Babel se cargan desde CDN). Después puedes abrir `index.html` con doble clic.

## Qué incluye

- **Roadmap maestro 2026**: las 5 niveles del Plan de Acción (priorizado por ROI) como fases, más el **sprint Open House Cluster Borgoña** (4 semanas con fechas reales) embebido.
- **43 acciones** con su canal, responsable, estatus, % de avance y racional.
- Las **7 ideas nuevas** de mayor potencial marcadas, y las acciones de **bajo ROI** señaladas para revisar/eliminar.

## Cómo se usa

| Acción | Cómo |
|---|---|
| Reprogramar | Arrastra el centro de una barra |
| Cambiar duración | Arrastra los bordes de la barra |
| Editar | Clic en la acción → editor lateral (nombre, descripción, nivel, canal, fechas, responsable, estatus, avance) |
| Quitar | Ícono de papelera al pasar el cursor sobre una fila, o **Eliminar** en el editor |
| Crear | Botón **+ Acción** |
| Agrupar | Por **Nivel de ROI** o por **Canal** |
| Zoom | Trimestre · Mes · Semana |
| Filtrar | Búsqueda, por estatus, o **solo ideas nuevas** |
| Exportar | **CSV** o **JSON** |
| Restablecer | Botón al final de la página; pide escribir `RESTABLECER` para confirmar |

## Acceso y persistencia

- **Pantalla de acceso** con usuario y contraseña (gate ligero del lado del cliente). Las contraseñas se guardan como *hash* SHA-256, no en texto plano. ⚠️ No es seguridad fuerte: al ser un sitio público, un usuario técnico podría saltarlo. Para control de acceso real se migraría a Supabase Auth.
- **Persistencia en Supabase**: el estado (tareas + configuración) vive en la tabla `gantt_state` del proyecto `siwiluoxrjnqjnrufbjl`; se carga al abrir y se guarda en cada cambio. `localStorage` queda como respaldo offline. El esquema está en [`supabase_setup.sql`](supabase_setup.sql).
- Acceso a datos **abierto** (políticas RLS anónimas): cualquiera con la *publishable key* puede leer/editar el tablero.

## Nota sobre las fechas

El documento original solo traía fechas duras en el sprint de 4 semanas. Las fechas de los **Niveles 1–5 son sugerencias** derivadas de su prioridad de ROI (N1 inmediato → N3 Q4'26–Q1'27) y son **100% editables** dentro de la herramienta.

## Tecnología

React 18 + Babel standalone + supabase-js (vía CDN), un único `index.html`. Sin servidor ni paso de compilación. Se publica con GitHub Actions (`.github/workflows/deploy.yml`).

## Respaldo e historial

- **Historial de cambios:** [`CHANGELOG.md`](CHANGELOG.md) — qué cambió y por qué, con instrucciones de recuperación.
- **Respaldos de datos:** carpeta [`backups/`](backups/) — *snapshots* JSON del estado en Supabase (las tareas en vivo), por si la base se pierde o se sobrescribe.
