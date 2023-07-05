import os
import yaml
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class Settings:
    def __init__(self, host: str, port: str, conn_ttl: int, log_level: LogLevel):
        self.host = host
        self.port = port
        self.conn_ttl = conn_ttl
        self.log_level = log_level

    def __eq__(self, other):
        """Helps to compare this objects"""
        if isinstance(other, Settings):
            return (
                self.host == other.host
                and self.port == other.port
                and self.conn_ttl == other.conn_ttl
                and self.log_level == other.log_level
            )
        return False

    def __repr__(self):
        """String represintation of object"""
        return f"Settings(host={self.host}, port={self.port}, conn_ttl={self.conn_ttl}, log_level={self.log_level})"
    
    def get_empty_conn_ttl(self) -> int:
        """Return time of TTL connection"""
        return self.conn_ttl

    def get_listen_address(self) -> str:
        """Return host and port as f'{self.host}:{self.port}'"""
        return f"{self.host}:{self.port}"

    def get_log_level(self) -> LogLevel:
        """Return level of logging"""
        return self.log_level


def from_yaml(conf_path: str) -> Settings:
    """
    Return Settings object from YAML file

    host = data["host"]
    port = data["port"]
    conn_ttl = data["conn_ttl"]
    log_level = LogLevel(data["log_level"])
    
    """
    with open(conf_path, "r") as file:
        data = yaml.safe_load(file)

    host = data["host"]
    port = data["port"]
    conn_ttl = data["con_live_sec"]
    log_level = LogLevel(data["log_level"])

    return Settings(host, port, conn_ttl, log_level)

