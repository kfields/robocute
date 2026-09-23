from .image import Image
from robocute.builder import Dna

class ItemImage(Image):
    def __init__(self, dna: Dna, useFn = None, style=None, crop=None):
        super().__init__(dna.img_src, useFn, style=style, crop=crop)
        self.dna = dna
