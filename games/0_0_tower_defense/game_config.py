import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode
from src.config.paths import PROJECT_PATH


class GameConfig(Config):
    """Load all game specific parameters and elements"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        os.chdir(PROJECT_PATH)
        super().__init__()
        self.game_id = "0_0_tower_defense"
        self.game_name = "Tower Defense"
        self.output_regular_json = True
        self.provider_number = 0
        self.working_name = "Sample scatter pay (pay anywhere)"
        self.wincap = 5000.0
        self.win_type = "scatter"
        self.rtp = 0.9700
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [5] * self.num_reels  # Optionally include variable number of rows per reel
        # Board and Symbol Properties - Cluster Pay (optimized for performance)
        # Format: ((min_cluster, max_cluster), "symbol"): payout_multiplier
        # Reduced to 3-7 cluster sizes for better performance
        t1, t2, t3 = (3, 4), (5, 6), (7, 8)
        pay_group = {
            (t1, "H1"): 1.0,
            (t2, "H1"): 3.0,
            (t3, "H1"): 7.5,
            (t1, "H2"): 0.8,
            (t2, "H2"): 2.0,
            (t3, "H2"): 5.0,
            (t1, "H3"): 0.6,
            (t2, "H3"): 1.3,
            (t3, "H3"): 3.2,
            (t1, "L1"): 0.4,
            (t2, "L1"): 0.6,
            (t3, "L1"): 1.5,
            (t1, "L2"): 0.3,
            (t2, "L2"): 0.4,
            (t3, "L2"): 1.2,
            (t1, "L3"): 0.2,
            (t2, "L3"): 0.2,
            (t3, "L3"): 0.8,
        }
        self.paytable = self.convert_range_table(pay_group)

        self.include_padding = False
        self.special_symbols = {"wild": ["W"], "scatter": ["S"], "multiplier": ["M"]}

        self.freespin_triggers = {
            self.basegame_type: {
                3: 8,
                4: 12,
                5: 15,
                6: 17,
                7: 19,
                8: 21,
                9: 23,
                10: 24,
            },
            self.freegame_type: {
                2: 3,
                3: 5,
                4: 8,
                5: 12,
                6: 14,
                7: 16,
                8: 18,
                9: 10,
                10: 12,
            },
        }
        self.anticipation_triggers = {
            self.basegame_type: min(self.freespin_triggers[self.basegame_type].keys()) - 1,
            self.freegame_type: min(self.freespin_triggers[self.freegame_type].keys()) - 1,
        }
        # Reels
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]
        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        # win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "mult_values": {
                                self.basegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
                                self.freegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
                            },
                            "scatter_triggers": {4: 1, 5: 2},
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.1,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {4: 5, 5: 1},
                            "mult_values": {
                                self.basegame_type: {2: 100, 3: 80, 4: 50, 5: 20, 10: 10},
                                self.freegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.4,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "mult_values": {
                                self.basegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
                                self.freegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
                            },
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.5,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "mult_values": {self.basegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
            BetMode(
                name="bonus",
                cost=200,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        # win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "mult_values": {
                                self.basegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
                                self.freegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
                            },
                            "scatter_triggers": {4: 10, 5: 5},
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.1,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {4: 10, 5: 5},
                            "mult_values": {
                                self.basegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
                                self.freegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                ],
            ),
        ]
