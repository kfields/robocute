from loguru import logger

import robocute.bot
    
class RoboVu(robocute.bot.BotVu):
    def __init__(self, img_src):
        super().__init__(img_src)
        
class Robo(robocute.bot.Bot):
    def __init__(self, dna):
        super().__init__(dna)
        logger.debug(f"Created Robo: {self.__class__.__name__}  with DNA: {dna}")

    def construct_vu(self):
        if self.dna.img_src:
            self.vu = self.add(RoboVu(self.dna.img_src))
