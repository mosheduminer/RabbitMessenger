from inspect import getfullargspec

from websockets import WebSocketServerProtocol


class Depends:
    __slots__ = ("dependency",)

    def __init__(self, dependency):
        self.dependency = dependency

    def __call__(self):
        return self.dependency


async def resolve_deps(func, param_data: dict, ws: WebSocketServerProtocol):
    spec = getfullargspec(func)
    deps = {}
    cleanup = []
    args = spec.args or []
    defaults = spec.defaults or []
    for reverse_index, default in enumerate(reversed(defaults), 1):
        if isinstance(default, Depends):
            dep_resolved, dep_params, dep_deps, dep_cleanup = await resolve_dep(
                default,
                param_data,
                ws,
            )
            async_iterator = dep_resolved(*dep_params, **dep_deps).__aiter__()
            resolved = await async_iterator.__anext__()
            cleanup.extend([async_iterator, *dep_cleanup])
            deps[args[len(args) - reverse_index]] = resolved
    params = []
    for param_name in args[0 : len(args) - len(defaults)]:
        annotation = spec.annotations.get(param_name)
        if annotation == WebSocketServerProtocol:
            params.append(ws)
            continue
        param = param_data.get(param_name)
        if param is None:
            raise MissingInput(f"missing {param_name}")
        # type conversion
        if annotation is None:
            params.append(param)
        else:
            try:
                # attempt type conversion
                param_type = type(param)
                if param_type == list or param_type == dict:
                    params.append(annotation(**param))
                elif annotation == str and param_type == bytes:
                    params.append(param.decode("utf-8"))
                elif annotation == bytes and param_type == str:
                    params.append(param.encode("utf-8"))
                else:
                    params.append(param)
            except Exception:
                raise BadInput(f"{param} cannot be cast to type {annotation}")
    return params, deps, cleanup


async def resolve_dep(
    dependency: Depends, param_data: dict, ws: WebSocketServerProtocol
):
    resolved = dependency()
    spec = getfullargspec(resolved)
    deps = {}
    cleanup = []
    args = spec.args or []
    defaults = spec.defaults or []
    for reverse_index, default in enumerate(reversed(defaults), 1):
        if isinstance(default, Depends):
            dep_resolved, dep_params, dep_deps, dep_cleanup = await resolve_dep(
                default,
                param_data,
                ws,
            )
            async_iterator = dep_resolved(*dep_params, **dep_deps).__aiter__()
            resolved_dep = await async_iterator.__anext__()
            cleanup.extend([async_iterator, *dep_cleanup])
            deps[args[len(args) - reverse_index]] = resolved_dep
    params = []
    for param_name in args[0 : len(args) - len(defaults)]:
        annotation = spec.annotations.get(param_name)
        if annotation == WebSocketServerProtocol:
            params.append(ws)
            continue
        param = param_data.get(param_name)
        if param is None:
            raise MissingInput(f"missing {param_name}")
        # type conversion
        if annotation is None:
            params.append(param)
        else:
            try:
                # attempt type conversion
                params.append(annotation(**param))
            except Exception:
                raise BadInput(f"{param} cannot be cast to type {annotation}")
    return resolved, params, deps, cleanup


async def cleanup_deps(cleanup: list):
    for dep in cleanup:
        async for _ in dep:
            pass


class MissingInput(Exception):
    pass


class BadInput(Exception):
    pass


class ServerError(Exception):
    def __init__(self, route: str = None, *args):
        self.route = route
        super().__init__(*args)


class StatusError(ServerError):
    def __init__(self, code: int, route: str, message: str):
        self.code = code
        super().__init__(route, message)


class AuthenticationError(Exception):
    pass
