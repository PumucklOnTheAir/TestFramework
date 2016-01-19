from router.ip_address import IPAddress


class IPv6(IPAddress):
    def __init__(self, ip: str, mask: int):
        super().__init__(ip)
