from abc import ABC, abstractmethod

import numpy as np

class BinaryData(ABC):
    @abstractmethod
    def decode(self, data: bytes) -> None:
        pass

    @abstractmethod
    def encode(self) -> bytes:
        pass

    @abstractmethod
    def length(self) -> np.uint16:
        pass