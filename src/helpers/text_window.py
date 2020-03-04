from typing import Optional

OUT_OF_RANGE_CHARACTER = None

class TextWindow:
    def __init__(self, text: str):
        self.text = text
        self.offset = 0
        self.length = len(text)

    def peek_char(self, nums: int = 0) -> Optional[str]:
        if self.offset + nums < self.length:
            return self.text[self.offset + nums]
        return OUT_OF_RANGE_CHARACTER

    def advance_char(self, nums: int = 1):
        self.offset += nums

    def may_continue(self) -> bool:
        return self.offset < self.length
