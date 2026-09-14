
import robocute.bot
    
class RoboVu(robocute.bot.BotVu):
    def __init__(self, imgSrc):
        super().__init__(imgSrc)
        
class Robo(robocute.bot.Bot):
    def __init__(self, dna):
        super().__init__(dna)
