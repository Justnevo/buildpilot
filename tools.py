import json
try:
    from . import storage
except ImportError:
    import storage


def _response(data):
    return json.dumps(data, ensure_ascii=False)


def _error(error):
    return _response({
        "success": False,
        "error": str(error)
    })


def add_project(params, **kwargs):
    try:
        project_id = storage.add_project(
            params["name"],
            params.get("description", "")
        )
        return _response({
            "success": True,
            "project_id": project_id,
            "message": "Project created successfully"
        })
    except (ValueError, KeyError) as exc:
        return _error(exc)


def list_projects(params, **kwargs):
    try:
        return _response({
            "success": True,
            "projects": storage.list_projects()
        })
    except Exception as exc:
        return _error(exc)


def add_task(params, **kwargs):
    try:
        task_id = storage.add_task(
            params["project_id"],
            params["title"]
        )
        return _response({
            "success": True,
            "task_id": task_id,
            "message": "Task created successfully"
        })
    except (ValueError, KeyError) as exc:
        return _error(exc)


def update_task(params, **kwargs):
    try:
        storage.update_task(
            params["task_id"],
            params["status"]
        )
        return _response({
            "success": True,
            "message": "Task status updated successfully"
        })
    except (ValueError, KeyError) as exc:
        return _error(exc)


def add_checkpoint(params, **kwargs):
    try:
        checkpoint_id = storage.add_checkpoint(
            params["project_id"],
            params["summary"]
        )
        return _response({
            "success": True,
            "checkpoint_id": checkpoint_id,
            "message": "Checkpoint saved successfully"
        })
    except (ValueError, KeyError) as exc:
        return _error(exc)
def get_project_context(params, **kwargs):
    try:
        context = storage.get_project_context(
            params["project_id"]
        )
        return _response({
            "success": True,
            "context": context
        })
    except (ValueError, KeyError) as exc:
        return _error(exc)
    except Exception as exc:
        return _error(exc)
