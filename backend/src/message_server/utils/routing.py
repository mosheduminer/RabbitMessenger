import json
import logging
from typing import Awaitable, Callable, Iterable, Optional

from websockets.server import WebSocketServerProtocol

from .depends import (
    AuthenticationError,
    BadInput,
    Depends,
    MissingInput,
    ServerError, StatusError,
    cleanup_deps,
    resolve_dep,
    resolve_deps,
)

import websockets


logger = logging.getLogger("router")

log_message = "{} - {} {} {}"  # origin, route, status code, message


class Router:
    def __init__(self, deps: Optional[Iterable[Depends]] = None):
        self.routes: dict[str, tuple[Awaitable, Optional[Iterable[Depends]]]] = {}
        self.connect_deps = deps
        self.replacement_deps = {}

    def replace_dep(self, dep: Callable, replacement: Callable):
        """
        This function exists for testing purposes, it allows mocking a dependency with a stub
        """
        self.replacement_deps[dep] = replacement

    def route(self, route, deps: Optional[Iterable[Depends]] = None):
        def register(func):
            self.routes[route] = (func, deps)

        return register

    async def call(self, input_data: str, ws: websockets.WebSocketServerProtocol):
        data: list = json.loads(input_data)
        route, param_data = data
        route_data = self.routes.get(route)
        if route_data is None:
            message = f"no route found matching {route}"
            logger.error(log_message.format(ws.origin, route, 404))
            return {"code": 404, "message": message}
        func, deps = route_data
        try:
            await self._run_deps(deps, param_data, ws)
        except MissingInput as e:
            logger.error(log_message.format(ws.origin, route, 400, str(e)))
            return {"code": 400, "message": str(e)}
        except BadInput as e:
            logger.error(log_message.format(ws.origin, route, 422, str(e)))
            return {"code": 422, "message": str(e)}
        except AuthenticationError as e:
            logger.error(log_message.format(ws.origin, route, 401, str(e)))
            return {"code": 401, "message": str(e)}
        try:
            params, deps, cleanup = await resolve_deps(func, param_data, ws)
        except MissingInput as e:
            logger.error(log_message.format(ws.origin, route, 400, str(e)))
            return {"code": 400, "message": str(e)}
        except BadInput as e:
            logger.error(log_message.format(ws.origin, route, 422, str(e)))
            return {"code": 422, "message": str(e)}
        except AuthenticationError as e:
            logger.error(log_message.format(ws.origin, route, 401, str(e)))
            return {"code": 401, "message": str(e)}
        try:
            ret = await func(*params, **deps)
            logger.info(log_message.format(ws.origin, route, 200, ""))
            return (ret and {"code": 200, "message": ret}) or ret
        finally:
            await cleanup_deps(cleanup)

    @staticmethod
    async def _run_deps(
        deps: Optional[Iterable],
        param_data: dict,
        ws: WebSocketServerProtocol,
    ):
        cleanup_list = []
        if deps is not None:
            try:
                for dep in deps:
                    (
                        dep_resolved,
                        dep_params,
                        dep_deps,
                        dep_cleanup,
                    ) = await resolve_dep(dep, param_data, ws)
                    async_iterator = dep_resolved(*dep_params, **dep_deps).__aiter__()
                    dep_resolved = await async_iterator.__anext__()
                    cleanup_list.extend([async_iterator, *dep_cleanup])
                    # dep_resolved and await dep_resolved(*dep_params, **dep_deps)
            finally:
                await cleanup_deps(cleanup_list)

    async def handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        await self._run_deps(self.connect_deps, {}, websocket)

        async for message in websocket:
            try:
                ret = await self.call(message, websocket)
                if ret is not None:
                    await websocket.send(json.dumps(ret))
            except StatusError as e:
                logger.error(
                    log_message.format(websocket.origin, e.route, e.code, ""),
                )
                await websocket.send(json.dumps({"code": e.code, "message": str(e)}))
            except ServerError as e:
                logger.error(
                    log_message.format(websocket.origin, e.route, 500, ""),
                    exc_info=True,
                )
                await websocket.send(json.dumps({"code": 500, "message": str(e)}))
            except Exception as e:
                logger.error(
                    log_message.format(websocket.origin, "unknkown", 500, ""),
                    exc_info=True,
                )
                await websocket.send(
                    json.dumps({"code": 500, "message": "internal server error"})
                )

    async def __call__(self, websocket: websockets.WebSocketServerProtocol, path: str):
        logger.info(f"{websocket.origin} connecting")
        try:
            await self.handler(websocket, path)
        except AuthenticationError as e:
            logger.error(log_message.format(websocket.origin, "----", 401, str(e)))
        except Exception:
            logger.error(
                log_message.format(
                    websocket.origin,
                    "----",
                    500,
                    "unexpected error, connection terminated",
                ),
                exc_info=True,
            )
