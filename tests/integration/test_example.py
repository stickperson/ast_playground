from run_tests import Application

class TestClass:
    code = '''\
class Workflow:
    pass

class X(Workflow):
    pass
    '''

    test = '''\
from sub.joe import X
'''
    def test_app(self, tmp_path, capsys):
        with tmp_path:
            d = tmp_path / 'sub'
            d.mkdir()
            f = d / 'joe.py'
            t = d / 'integration_joe.py'
            f.write_text(self.code)
            t.write_text(self.test)
            app = Application([f], start_directory=d)
            app.run()
            assert len(app._inspectors) == 1
            targets = app._inspectors[0].report()
            assert len(targets) == 1
            assert targets == {'X'}
