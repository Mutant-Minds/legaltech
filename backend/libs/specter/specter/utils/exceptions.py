class TenantNotFoundError(Exception):
    def __init__(self, host: str):
        """

        Args:
            host:
        """
        self.message = f"Tenant not found for host: {host}"
        super().__init__(self.message)
