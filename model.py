import sys
from cv2 import Mat
import yaml
from importlib.machinery import SourceFileLoader

class ModelHandler:
    def __init__(self, conf_route: str):
        with open(conf_route, 'r') as f:
            self.data = yaml.safe_load(f)
        # Clear
        try:
            assert 'Models' in self.data, 'Field "Models" not found'
            assert isinstance(self.data['Models'], list), 'No model list found'
            assert len(self.data['Models']) > 0, 'Models list is empty'
        except AssertionError as err:
            self.valid = False
            print("Error:", err, file=sys.stderr)
        else:
            self.valid = True
        # Sel model
        self.n = 0
        if self.valid:
            self.change_model(self.n)
            self.source = SourceFileLoader('Modelo', self.current_model['alg_path'])
            self.module = self.source.load_module()
        else:
            self.current_model = {'name' : 'Error with Model Handler'}

    def __bool__(self):
        return self.valid

    def change_model(self, n):
        assert n < len(self.data['Models'])
        self.current_model = self.data['Models'][n]

    def next_model(self):
        self.n = self.n + 1
        self.n = 0 if self.n == len(self.data['Models']) else self.n 
        self.change_model(self.n)

    def get_model(self):
        return self.current_model.copy()

    def compute(self, img: Mat) -> int:
        if self.source.path != self.current_model['alg_path']:
            self.source = SourceFileLoader('Modelo', self.current_model['alg_path'])
            self.module = self.source.load_module()
        return self.module.count(img)

    def __getitem__(self, key):
        return self.current_model[key]

    def lock_model(self):
        pass

    def train_model(self):
        pass

