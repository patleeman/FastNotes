import unittest
import unittest.mock
import InitialSetup

class TestInitialSetup(unittest.TestCase):
    class mock_path():
        @staticmethod
        def join(self, a):
            return '/'
        @staticmethod
        def dirname(self):
            pass
        @staticmethod
        def abspath(self):
            pass
        def expanduser(self):
            pass

    class mock_open():
        def __init__(self, a, b):
            pass
        def __enter__(self):
            return self
        def write(self, a):
            pass
        def __exit__(self, a, b, c):
            pass


    @unittest.mock.patch('builtins.open', new=mock_open)
    @unittest.mock.patch('os.path', new=mock_path)
    @unittest.mock.patch('InitialSetup.find_home_directory')
    @unittest.mock.patch('sys.stdout.write')
    def test_run(self, mock_print, home):
        InitialSetup.run()
        self.assertTrue(mock_print.called)
        self.assertTrue(home.called)



    def test_find_home_directory(self):
        pass



if __name__ == '__main__':
    unittest.main()