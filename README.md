# BuildPilot

**Never lose track of what your AI is building.**

BuildPilot is a project tracking and progress recovery plugin for Hermes Agent. It helps AI agents organize projects, track tasks, save checkpoints, and recover project context across sessions.

## Features

- Create and manage multiple projects.
- Track tasks within individual projects.
- Update task statuses.
- Save progress checkpoints.
- Retrieve project details, tasks, and the latest checkpoint together.
- Store project data locally using SQLite.

## Available Tools

| Tool | Description |
|---|---|
| `buildpilot_add_project` | Create a new project |
| `buildpilot_list_projects` | List saved projects |
| `buildpilot_add_task` | Add a task to a project |
| `buildpilot_update_task` | Update a task's status |
| `buildpilot_checkpoint` | Save a project progress checkpoint |
| `buildpilot_get_project_context` | Retrieve project details, tasks, and the latest checkpoint |

## Task statuses

- `pending`
- `in_progress`
- `completed`

## Example workflow

1. Create a project.
2. Add tasks to the project.
3. Update task statuses as work progresses.
4. Save checkpoints to preserve important progress.
5. Retrieve the complete project context when resuming work.

## Technology

- Python
- SQLite
- Hermes Agent Plugin API

## Testing

The project includes automated storage tests covering project creation, task management, checkpoint creation, and project-context retrieval.

**Current test status: 8 tests passing.**

## Data storage

BuildPilot stores project information in a local SQLite database.

## License

MIT
