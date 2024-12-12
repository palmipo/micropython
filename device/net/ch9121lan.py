import network

class CH9121Lan(network.AbstractNIC):
    def __init__(self, ch9121):
        pass

    def active(self) -> bool:
        pass

    def active(self, is_active: bool) -> None:
        pass

    def connect(self, key: str | None = None, **kwargs: Any) -> None:
        pass

    def connect(
        self, service_id: Any, key: str | None = None, **kwargs: Any
    ) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def isconnected(self) -> bool:
        pass

    def scan(self, **kwargs: Any) -> list[tuple[str, ...]]:
        pass

    def status(self) -> Any:
        pass

    def status(self, param: str) -> Any:
        pass

    def ifconfig(self) -> tuple[str, str, str, str]:
        pass

    def ifconfig(self, ip_mask_gateway_dns: tuple[str, str, str, str]) -> None:
        pass

    def config(self, param: str) -> Any:
        pass

    def config(self, **kwargs: Any) -> None:
        pass

