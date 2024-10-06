from game_engine.game_state import GameState

class GameEngine:
    def __init__(self, num_players):
        self.game_state = GameState()
        self.num_players = num_players
    
    def perform_action(self, action, player_id, is_visible):
        self.game_state.perform_action(action, player_id, is_visible)