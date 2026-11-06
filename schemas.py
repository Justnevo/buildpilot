def make_schema(name, description, properties, required=None):
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required or [],
        },
    }


ADD_PROJECT = make_schema(
    "buildpilot_add_project",
    "Create a new project in BuildPilot.",
    {
        "name": {"type": "string", "description": "Project name"},
        "description": {"type": "string", "description": "Project description"},
    },
    ["name"],
)

LIST_PROJECTS = make_schema(
    "buildpilot_list_projects",
    "List all saved BuildPilot projects.",
    {},
)

ADD_TASK = make_schema(
    "buildpilot_add_task",
    "Add a task to an existing project.",
    {
        "project_id": {"type": "integer", "description": "Project ID"},
        "title": {"type": "string", "description": "Task title"},
    },
    ["project_id", "title"],
)

UPDATE_TASK = make_schema(
    "buildpilot_update_task",
    "Update a task's status.",
    {
        "task_id": {"type": "integer", "description": "Task ID"},
        "status": {
            "type": "string",
            "enum": ["pending", "in_progress", "completed"],
            "description": "New task status",
        },
    },
    ["task_id", "status"],
)

ADD_CHECKPOINT = make_schema(
    "buildpilot_checkpoint",
    "Save a progress checkpoint for a project.",
    {
        "project_id": {"type": "integer", "description": "Project ID"},
        "summary": {"type": "string", "description": "Current project progress"},
    },
    ["project_id", "summary"],
)
GET_PROJECT_CONTEXT = make_schema(
    "buildpilot_get_project_context",
    "Retrieve a project's details, tasks, and latest progress checkpoint.",
    {
        "project_id": {
            "type": "integer",
            "description": "ID of the project to retrieve"
        },
    },
    ["project_id"],
)
