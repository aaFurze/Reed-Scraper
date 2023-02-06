from typing_extensions import Protocol


class UrlConstructor(Protocol):
    @classmethod
    def get_url(cls, *args, **kwargs) -> str:
        ...