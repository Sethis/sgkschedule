

from typing import Optional

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from tools import Parser


class ParseFilter(BaseFilter):
    def __init__(self, prefix: Optional[str] = None, parameter: Optional[str] = None,
                 value: Optional[str] = None, additional: Optional[str] = None):

        self.prefix = prefix
        self.parameter = parameter
        self.value = value
        self.additional = additional

    async def __call__(self, _message: CallbackQuery, parser: Parser) -> bool:
        if self.prefix and self.prefix != parser.prefix:
            return False

        if self.parameter and self.parameter != parser.parameter:
            return False

        if self.value and self.value != parser.value:
            return False

        if self.additional and self.additional != parser.additional:
            return False

        return True
