class DetailedHTTPException(Exception):
    DETAIL: str = 'Error'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.DETAIL, *args, **kwargs)
