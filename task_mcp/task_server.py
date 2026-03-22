from fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
from pathlib import Path
import json

from config.custom_logging_config import RequestLoggingMiddleware
from config.logging_config import configure_logging

configure_logging()

mcp = FastMCP("Task Server")
mcp.add_middleware(RequestLoggingMiddleware())

TASKS_FILE = Path(__file__).parent / "tasks.json"


def load_tasks() -> list[dict]:
    if not TASKS_FILE.exists():
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_tasks(tasks: list[dict]) -> None:
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


def get_next_id(tasks: list[dict]) -> int:
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


@mcp.tool()
def add_task(
    title: Annotated[str, Field(description="Kort titel på uppgiften")],
    description: Annotated[str, Field(description="Beskrivning av uppgiften")],
    priority: Annotated[str, Field(description="Prioritet: low, medium eller high")],
) -> dict:
    """Lägger till en ny uppgift i den lokala uppgiftslistan."""
    tasks = load_tasks()

    normalized_priority = priority.strip().lower()
    if normalized_priority not in {"low", "medium", "high"}:
        return {
            "success": False,
            "message": "Ogiltig prioritet. Använd: low, medium eller high."
        }

    new_task = {
        "id": get_next_id(tasks),
        "title": title.strip(),
        "description": description.strip(),
        "priority": normalized_priority,
        "status": "open"
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return {
        "success": True,
        "message": "Uppgift skapad.",
        "task": new_task
    }


@mcp.tool()
def list_tasks(
    status: Annotated[str, Field(description="Filter för status: all, open eller done")],
) -> dict:
    """Listar uppgifter baserat på status."""
    tasks = load_tasks()

    normalized_status = status.strip().lower()
    if normalized_status not in {"all", "open", "done"}:
        return {
            "success": False,
            "message": "Ogiltig status. Använd: all, open eller done."
        }

    if normalized_status == "all":
        filtered_tasks = tasks
    else:
        filtered_tasks = [task for task in tasks if task["status"] == normalized_status]

    return {
        "success": True,
        "count": len(filtered_tasks),
        "tasks": filtered_tasks
    }


@mcp.tool()
def complete_task(
    task_id: Annotated[int, Field(description="ID för uppgiften som ska markeras som klar")],
) -> dict:
    """Markerar en uppgift som klar."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            save_tasks(tasks)
            return {
                "success": True,
                "message": f"Uppgift {task_id} markerades som klar.",
                "task": task
            }

    return {
        "success": False,
        "message": f"Hittade ingen uppgift med id {task_id}."
    }


@mcp.tool()
def search_tasks(
    keyword: Annotated[str, Field(description="Sökord som matchas mot titel och beskrivning")],
) -> dict:
    """Söker efter uppgifter baserat på nyckelord."""
    tasks = load_tasks()
    query = keyword.strip().lower()

    matches = [
        task for task in tasks
        if query in task["title"].lower() or query in task["description"].lower()
    ]

    return {
        "success": True,
        "count": len(matches),
        "tasks": matches
    }


@mcp.tool()
def delete_task(
    task_id: Annotated[int, Field(description="ID för uppgiften som ska tas bort")],
) -> dict:
    """Tar bort en uppgift från listan."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            updated_tasks = [t for t in tasks if t["id"] != task_id]
            save_tasks(updated_tasks)
            return {
                "success": True,
                "message": f"Uppgift {task_id} togs bort.",
                "deleted_task": task
            }

    return {
        "success": False,
        "message": f"Hittade ingen uppgift med id {task_id}."
    }


if __name__ == "__main__":
    import asyncio

    asyncio.run(
        mcp.run_http_async(
            host="0.0.0.0",
            port=8003,
            log_level="warning",
        )
    )