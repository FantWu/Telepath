from configparser import ConfigParser


class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")
        self.openai_api_key = self.config.get("keys", "openai_api_key")
        self.wolfram_alpha_api_key = self.config.get("keys", "wolfram_alpha_api_key")
        self.language_mode = self.config.get("settings", "language_mode")
        self.your_name = self.config.get("settings", "your_name")
        self.bing_cookie = self.config.get("settings", "bing_cookie")
        self.show_balance = self.config.get("settings", "show_balance")


config_instance = Config()