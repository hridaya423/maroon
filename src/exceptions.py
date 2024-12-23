"""Custom exceptions for the Maroon interpreter."""

class PirateException(Exception):
    def __init__(self, message: str, line_number: int = None, context: str = None):
        self.message = message
        self.line_number = line_number
        self.context = context
        super().__init__(self.format_error())

    def format_error(self) -> str:
        base_error = f"🏴‍☠️ Pirate Error: {self.message}"
        if self.line_number is not None:
            base_error += f" (Line {self.line_number})"
        if self.context:
            base_error += f"\n🗺️ Context: {self.context}"
        return base_error