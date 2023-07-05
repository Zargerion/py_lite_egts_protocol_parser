from config import LogLevel, Settings, from_yaml

import unittest
import os

class TestConfigLoad(unittest.TestCase):
    def test_config_load(self):
        # os helps to take abs path to conf.yaml using ralative of this file.
        conf = from_yaml(os.path.join(os.path.dirname(os.path.abspath(__file__)), "conf.yaml"))
        expected_conf = Settings(
            host="127.0.0.1",
            port="6000",
            conn_ttl=10,
            log_level=LogLevel.DEBUG,
        )

        self.assertEqual(conf, expected_conf)


if __name__ == "__main__":
    unittest.main()