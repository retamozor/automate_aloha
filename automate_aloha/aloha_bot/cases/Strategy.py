from abc import ABC, abstractmethod
from pywinauto.application import WindowSpecification


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of cases.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def __init__(self, dlg: WindowSpecification, lat_deg, lat_min, long_deg, long_min) -> None:
      pass

    
    @abstractmethod
    def set_up_chemical(self) -> None:
      pass
    
    @abstractmethod
    def run(self, data, index) -> None:
      pass