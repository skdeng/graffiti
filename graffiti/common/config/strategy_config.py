import importlib.util
import inspect
import ntpath
import os
from typing import Callable, Generic, List, TypeVar

from graffiti.market import Portfolio

ConfigType = TypeVar('ConfigType')


class StrategyConfig(Generic[ConfigType]):
    def __init__(self, config_root, global_config):
        self.global_config = global_config
        self.config_root = config_root
        self._module = None
        self._strategy_class = None

    @property
    def file(self) -> str:
        return self.config_root['file']

    @property
    def name(self) -> str:
        return self.config_root.get('name', os.path.splitext(ntpath.basename(self.file.rstrip('/\\')))[0])

    @property
    def enabled(self) -> str:
        return self.config_root.get('enabled', True)

    @property
    def config(self) -> ConfigType:
        return self.config_root.get('config', {})

    @property
    def flat_fee(self) -> float:
        return self.config_root.get('flat_fee', 0)

    @property
    def ratio_fee(self) -> float:
        return self.config_root.get('ratio_fee', 0)

    @property
    def module(self):
        if not self._module:
            spec = importlib.util.spec_from_file_location(
                'strategy.module', self.file)
            self._module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self._module)
        return self._module

    def get_strategy_instance(self):
        if not self._strategy_class:
            item = inspect.getmembers(self.module, inspect.isclass)
            item = list(
                filter(lambda i: i[0].lower().endswith('strategy'), item))
            if len(item) > 1:
                raise "More than 1 strategy class found in the file"
            if len(item) == 0:
                return None
            _, self._strategy_class = item[0]

        return self._strategy_class(self.config)

    def get_strategy_function(self) -> Callable[[List, ConfigType], List]:
        return self.module.run_strategy

    def get_initial_portfolio(self) -> Portfolio:
        if 'portfolio' in self.config_root:
            return Portfolio.from_config(self.config_root['portfolio'])
        else:
            return self.global_config.get_initial_portfolio()
