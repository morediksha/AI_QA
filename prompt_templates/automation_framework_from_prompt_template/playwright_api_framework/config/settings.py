import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Global settings and configuration"""
    
    # Environment
    TEST_ENV = os.getenv("TEST_ENV", "dev").lower()
    CONFIG_PATH = Path(__file__).parent / "environments.yaml"
    
    # Load environment-specific config
    with open(CONFIG_PATH, 'r') as f:
        ENV_CONFIG = yaml.safe_load(f)
    
    @property
    def base_url(self) -> str:
        return self.ENV_CONFIG[self.TEST_ENV]["base_url"]
    
    @property
    def timeout(self) -> int:
        return self.ENV_CONFIG[self.TEST_ENV].get("timeout", 10000)
    
    @property
    def max_retries(self) -> int:
        return self.ENV_CONFIG[self.TEST_ENV].get("retries", 3)
    
    # Reporting
    REPORTS_DIR = Path(__file__).parent.parent / "reports"
    LOGS_DIR = Path(__file__).parent.parent / "logs"
    REPORT_TYPE = os.getenv("REPORT_TYPE", "html")  # html, json, allure
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Retry
    RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "1"))
    RETRY_BACKOFF = float(os.getenv("RETRY_BACKOFF", "2"))
    
    # Parallel execution
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    
    def __init__(self):
        """Ensure directories exist"""
        self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
