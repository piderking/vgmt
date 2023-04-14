from .config import ConfigClass
import os

# Development
config = ConfigClass(os.path.join(os.path.abspath("."), "app/util","dev.json"))