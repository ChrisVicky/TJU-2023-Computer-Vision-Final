from dataclasses import dataclass

api_base_url = 'https://abc235.site/api/proxy_pool/'


@dataclass
class Proxy:
    proxy: str
    support_https: bool

    def __hash__(self):
        return self.proxy.__hash__()

    def __eq__(self, other):
        return self.proxy == other.proxy


