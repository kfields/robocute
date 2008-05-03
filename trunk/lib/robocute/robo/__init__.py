
import robocute.bot
    
class RoboVu(robocute.bot.BotVu):
    def __init__(self, node, imgSrc):
        super(RoboVu, self).__init__(node, imgSrc)
        
class Robo(robocute.bot.Bot):
    def __init__(self, dna):
        super(Robo, self).__init__(dna)
