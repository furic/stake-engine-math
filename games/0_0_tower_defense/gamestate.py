from game_override import GameStateOverride
from src.calculations.cluster import Cluster


class GameState(GameStateOverride):
    """Gamestate for a single spin - simplified cluster game without tumbling"""

    def run_spin(self, sim: int):
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.draw_board()

            self.get_clusters_update_wins()
            # No tumbling - symbols stay on board after winning

            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_fs_condition() and self.check_freespin_entry():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self):
        self.reset_fs_spin()
        while self.fs < self.tot_fs:
            self.update_freespin()
            self.draw_board()

            self.get_clusters_update_wins()
            # No tumbling in free spins either - just cluster detection

            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

        self.end_freespin()
