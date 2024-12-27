class PirateException(Exception):
    def __init__(self, message: str, line_number: int = None, context: str = None):
        self.message = message
        self.line_number = line_number
        self.context = context
        super().__init__(self.format_error())

    def format_error(self) -> str:
        error_parts = [f"💀 Arr! {self.message}"]
        
        if self.line_number is not None:
            error_parts.append(f"📍 Line {self.line_number}")
        
        if self.context:
            error_parts.append(f"🗺️ Context: {self.context}")
            
        return "\n".join(error_parts)