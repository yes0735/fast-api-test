# -*- coding: utf-8 -*-
import os

from fastapi import FastAPI


def get_application() -> FastAPI:
    """get_application"""
    application = FastAPI(title=f"leekh Test API")
    # Routing
    set_routes(application, load_controllers())
    # print(load_controllers())

    return application


def set_routes(application, controllers):
    """set_routes"""

    tags_metadata = []
    for route in controllers:
        route = route.replace(".py", "").replace("./", "").replace("/", ".")
        # print(route)
        router = __import__(route, fromlist=[route])
        application.include_router(router.router)
        # Configurations
        configurations = getattr(router, "configurations", {})
        swagger = configurations.get("swagger", {})
        tags = swagger.get("tags")
        meta = swagger.get("tags_metadata")
        if meta is not None:
            tags_metadata.append(meta)

        application.include_router(router.router, tags=tags)
    # Swagger Ordering
    application.openapi_tags = sorted(tags_metadata, key=lambda k: k["name"])


def load_controllers():
    """load_controllers"""

    route_path = "./app/controllers/"
    controllers = []
    for path, dirs, files in os.walk(route_path):
        if files:
            for filename in files:
                if filename.startswith("__") is False and filename.endswith(".py"):
                    controllers.append(os.path.join(path, filename))
    return controllers


app = get_application()
