-- ============================================================
-- Estrategia Innova · persistencia del Gantt en Supabase
-- Proyecto: siwiluoxrjnqjnrufbjl
-- Ejecutar en: Supabase Dashboard → SQL Editor → New query → Run
-- ============================================================

-- 1) Tabla: un solo registro guarda TODO el estado (tareas + config) en JSONB.
create table if not exists public.gantt_state (
  id          text primary key,
  data        jsonb not null default '{}'::jsonb,
  updated_at  timestamptz not null default now()
);

-- 2) Row Level Security activado.
alter table public.gantt_state enable row level security;

-- 3) Permisos de tabla para el rol anónimo (la publishable key usa el rol "anon").
grant select, insert, update on public.gantt_state to anon;

-- 4) Políticas de ACCESO ABIERTO (sin login).
--    Cualquiera con la publishable key puede leer y editar este tablero.
--    Si más adelante quieres cerrarlo, se reemplazan estas políticas por
--    unas basadas en auth (Supabase Auth).
drop policy if exists "gantt_state anon read"   on public.gantt_state;
drop policy if exists "gantt_state anon insert" on public.gantt_state;
drop policy if exists "gantt_state anon update" on public.gantt_state;

create policy "gantt_state anon read"   on public.gantt_state for select to anon using (true);
create policy "gantt_state anon insert" on public.gantt_state for insert to anon with check (true);
create policy "gantt_state anon update" on public.gantt_state for update to anon using (true) with check (true);

-- Listo. Al volver a abrir el Gantt, el indicador debe pasar a "Supabase ✓".
