from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Bouquet:
    """
    表示一种花束类型：配方 + 制作时间 + 售价。
    不包含库存、现金等副作用。
    """
    code: str          # "fern_tastic" / "be_leaf" / "you_rose"
    greenery: int
    roses: int
    daisies: int
    minutes: int
    price: float

    @property
    def ingredients(self) -> Dict[str, int]:
        """返回制作一束花需要的原料数量。"""
        return {
            "greenery": self.greenery,
            "roses": self.roses,
            "daisies": self.daisies,
        }
