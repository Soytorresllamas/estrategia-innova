"""Descarga el estado del Gantt desde Supabase y guarda un respaldo en backups/.
Solo escribe un snapshot nuevo cuando los datos cambiaron respecto al último.
Lo usa el workflow .github/workflows/backup.yml (también ejecutable a mano)."""
import json
import os
import datetime
import urllib.request

SB_URL = os.environ["SB_URL"].rstrip("/")
SB_KEY = os.environ["SB_KEY"]

req = urllib.request.Request(
    f"{SB_URL}/rest/v1/gantt_state?select=data&id=eq.innova-default",
    headers={"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}"},
)
raw = json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))
data = raw[0]["data"] if raw else {}

os.makedirs("backups", exist_ok=True)
out = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True)

latest = "backups/latest.json"
old = open(latest, encoding="utf-8").read() if os.path.exists(latest) else None

if out != old:
    with open(latest, "w", encoding="utf-8") as f:
        f.write(out + "\n")
    stamp = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    with open(f"backups/gantt-state-{stamp}.json", "w", encoding="utf-8") as f:
        f.write(out + "\n")
    tasks = data.get("tasks", []) if isinstance(data, dict) else []
    print(f"changed: {len(tasks)} tareas guardadas en backups/")
else:
    print("unchanged: sin cambios en los datos, no se crea respaldo")
