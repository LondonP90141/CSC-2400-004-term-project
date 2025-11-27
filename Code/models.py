# This file defines the basic data structure we use in the project.

from dataclasses import dataclass

@dataclass
class Product:
    #Represents a single item from the CSV.
    id: int
    category: str
    price: float     # in dollars
    utility: int     # how “valuable” the item is in our knapsack