from .Strategy import Strategy

class Context():
    """
    The Context defines the interface to run cases
    """

    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy
        self._strategy.set_up_chemical()

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy
        self._strategy.set_up_chemical()

    def run(self, data, index) -> None:
        self._strategy.run(data, index)