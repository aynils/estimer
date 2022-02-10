from dataclasses import dataclass


@dataclass
class IRISData:
    iris_name: str
    chart_b64_svg: str
    price_evolution_text: str
