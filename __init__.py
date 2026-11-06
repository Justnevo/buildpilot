from . import schemas, tools


def register(ctx):
    registrations = [
        (schemas.ADD_PROJECT, tools.add_project),
        (schemas.LIST_PROJECTS, tools.list_projects),
        (schemas.ADD_TASK, tools.add_task),
        (schemas.UPDATE_TASK, tools.update_task),
        (schemas.ADD_CHECKPOINT, tools.add_checkpoint),
        (schemas.GET_PROJECT_CONTEXT, tools.get_project_context),
    ]

    for schema, handler in registrations:
        ctx.register_tool(
            name=schema["name"],
            toolset="buildpilot",
            schema=schema,
            handler=handler,
        )
