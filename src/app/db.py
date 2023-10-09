from time import time

import tarantool

RECONNECT_MAX_ATTEMPTS = 5
RECONNECT_DELAY = 1
CONNECTION_TIMEOUT = 2


class Store:
    def __init__(
        self,
        space,
        url="tarantool",
        port=3301,
        max_att=RECONNECT_MAX_ATTEMPTS,
        delay=RECONNECT_DELAY,
        timeout=CONNECTION_TIMEOUT,
    ):
        self.connection = tarantool.Connection(
            url,
            port,
            reconnect_max_attempts=max_att,
            reconnect_delay=delay,
            connection_timeout=timeout,
        )
        self.link_space = self.connection.space(space)

    def cache_set(self, key: str, val: str, lte: float | int):
        """
        It puts value and time to live to the cache
        """
        self._set(str(key), str(val), time() + float(lte))

    def cache_get(self, key: str):
        """
        It returns value if cache has and if time to live not expired
        """
        val = self._get(key)
        try:
            if val is not None:
                return val[1] if val[2] >= time() else 0
        except IndexError:
            pass
        return 0

    def _set(self, key: str, value: str, lte):
        try:
            self.link_space.replace((key, value, lte))
        except tarantool.error.NetworkError:
            pass

    def _get(self, key: str):
        try:
            response = self.link_space.select(key)
            return response.data[0]
        except tarantool.error.NetworkError:
            pass
        except IndexError:
            pass
        return ()
