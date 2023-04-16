

from typing import Union, TypeVar, Optional


class ParseTypes:
    callback_data = TypeVar("callback_data", bound=str)

    symbols = (":", ".", "?")


def callback_data(prefix: str, parameter: str = "",
                  value: Union[str, int] = "", additional: Union[str, int] = "") -> ParseTypes.callback_data:

    return f"{prefix}/{parameter}/{value}/{additional}"


class Parser:
    def __init__(self, data: ParseTypes.callback_data):
        self.data = data

        self.prefix: Optional[str] = None
        self.parameter: Optional[str] = None
        self.value: Optional[str] = None
        self.additional: Optional[str] = None

    def parse(self):
        data = self.string_parse(self.data)

        self.prefix = data["prefix"]
        self.parameter = data["parameter"]
        self.value = data["value"]
        self.additional = data["additional"]

    @staticmethod
    def string_parse(callback_data_string: str) -> dict[str, str, str, str]:
        sptlit_data = callback_data_string.split("/")

        prefix, parameter, value, additional = sptlit_data

        return {"prefix": prefix, "parameter": parameter, "value": value, "additional": additional}

