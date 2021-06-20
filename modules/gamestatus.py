
class GameStatus:

    def __init__(self):
        self.statuslist = [
            'Starting Screen',
            'Game Running!',
            'Game Over!',
            'Game Paused!'
            'Score Board'
        ]

        self.status = 0
    
    def set_status(self, status: int):
        self.status = status if status >= 0 and status < len(self.statuslist) else 0
