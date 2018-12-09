import ntpath
import os

class StrategyConfig:
    def __init__(self, config_root):
        self.config_root = config_root
        
    @property
    def file(self):
        return self.config_root['file']

    @property
    def name(self):
        return self.config_root.get('name', os.path.splitext(ntpath.basename(self.file.rstrip('/\\')))[0])

    @property
    def enabled(self):
        return self.config_root.get('enabled', True)

    @property
    def config(self):
        return self.config_root.get('config', {})

    @property
    def flat_fee(self):
        return self.config_root.get('flat_fee', 0)

    @property
    def ratio_fee(self):
        return self.config_root.get('ratio_fee', 0)