class Player:
    def __init__(self, player_id, hp, num_bullets, num_bombs, hp_shield, num_deaths, num_shield):
        self.player_id = player_id
        self.hp = hp
        self.num_bullets = num_bullets
        self.num_bombs = num_bombs
        self.hp_shield = hp_shield
        self.num_deaths = num_deaths
        self.num_shield = num_shield

    def get_dict(self):
        data = {
            "hp": self.hp,
            "bullets": self.num_bullets,
            "bombs": self.num_bombs,
            "shield_hp": self.hp_shield,
            "deaths": self.num_deaths,
            "shields": self.num_shield
        }

        return data
    
    