# Student Task MCP Server

## Beskrivning

Detta projekt implementerar en MCP-server (Model Context Protocol) för att hantera uppgifter lokalt.

Servern exponerar flera verktyg (tools) som kan användas av en agent för att:

* skapa uppgifter
* lista uppgifter
* markera uppgifter som klara
* söka efter uppgifter
* ta bort uppgifter

All data lagras lokalt i en JSON-fil (`tasks.json`).

---

## Funktionalitet

### Tillgängliga verktyg

* **add_task**
  Lägger till en ny uppgift.

* **list_tasks**
  Listar uppgifter baserat på status (`all`, `open`, `done`).

* **complete_task**
  Markerar en uppgift som klar.

* **search_tasks**
  Söker efter uppgifter baserat på nyckelord.

* **delete_task**
  Tar bort en uppgift.

---

## Tekniska krav (uppfylls)

* Minst 5 tools implementerade
* Alla parametrar använder `Annotated` och `Field`
* MCP-server byggd med `FastMCP`
* Middleware används för loggning

---

## Projektstruktur

```
task_mcp/
├─ task_server.py
├─ tasks.json
```

---

## Installation

Installera dependencies:

```bash
pip install -r requirements.txt
```

---

## Starta servern

```bash
python -m task_mcp.task_server
```

Servern startar på:

```
http://localhost:8003/mcp
```

---

## Exempel på användning

När servern körs kan en agent anropa verktygen, t.ex.:

* skapa uppgift
* lista uppgifter
* uppdatera status

---

## Datamodell

Uppgifter lagras i `tasks.json` med följande struktur:

```json
{
  "id": 1,
  "title": "Skriva rapport",
  "description": "MLOps uppgift",
  "priority": "high",
  "status": "open"
}
```

---

## Syfte

Syftet med projektet är att demonstrera hur en MCP-server kan användas för att exponera funktionalitet till en AI-agent, samt hur lokal datalagring kan kombineras med verktygsbaserad interaktion.

# student_task_mcp_server
