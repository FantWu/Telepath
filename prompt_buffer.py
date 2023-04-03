class prompt_buffer:
    def __init__(self):
        self.buffer = ""

    def get_buffer(self):
        return self.buffer

    def set_buffer(self, prompt: str):
        self.buffer = prompt
        return self.buffer

    def clear_buffer(self):
        self.buffer = ""
        return ""


buffer = prompt_buffer()
