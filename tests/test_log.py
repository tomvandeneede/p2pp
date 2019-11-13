import unittest2
import p2pp.variables as v
from p2pp.log import LogService

class TestLogServiceMock():
    errors = []
    warnings = []
    info = []

    def log_error(self, message):
        self.errors.append(message)

    def log_warning(self, message):
        self.warnings.append(message)

    def log_info(self, message):
        self.info.append(message)

class TestLogService(unittest2.TestCase):
    def __create_logging_service(self):
        log = LogService()
        log.register_service(TestLogServiceMock())
        return log

    def test_register_service(self):
        log = self.__create_logging_service()
        self.assertTrue(isinstance(log.get_service(), TestLogServiceMock))

    def test_logging_service(self):
        log = self.__create_logging_service()
        impl = log.get_service()

        with self.subTest("Summary is printed"):
            log.summary("Test summary")
            self.assertTrue(len(impl.info))

        with self.subTest("Adds errors to log"):
            error_msg = "Test error log"
            log.error(error_msg)
            self.assertIn(error_msg, impl.errors)

        with self.subTest("Adds warnings to log"):
            warning_msg = "Test warning log"
            log.warning(warning_msg)
            self.assertIn(warning_msg, impl.warnings)
        
        with self.subTest("Adds info to log"):
            info_msg = "Test info log"
            log.info(info_msg)
            self.assertIn(info_msg, impl.info)

if __name__ == '__main__':
    unittest2.main()
