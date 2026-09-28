source_id: FASTAPI_BACKGROUND
title: FastAPI Background Tasks
url: https://fastapi.tiangolo.com/tutorial/background-tasks/

FastAPI BackgroundTasks lets a path operation schedule work that runs after returning the response. This is useful for small follow-up work such as writing a log or sending a notification when the client does not need to wait for completion. Heavy distributed jobs typically need a separate task system.
