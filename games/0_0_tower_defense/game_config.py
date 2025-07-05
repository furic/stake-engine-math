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
        # Board and Symbol Properties - Cluster Pay (3 to 14, then 15+)
        # Format: ((min_cluster, max_cluster), "symbol"): payout_multiplier
        pay_group = {
            # H1 - Premium symbol
            ((3, 3), "H1"): 1.0,
            ((4, 4), "H1"): 2.0,
            ((5, 5), "H1"): 4.0,
            ((6, 6), "H1"): 8.0,
            ((7, 7), "H1"): 15.0,
            ((8, 8), "H1"): 25.0,
            ((9, 9), "H1"): 40.0,
            ((10, 10), "H1"): 60.0,
            ((11, 11), "H1"): 80.0,
            ((12, 12), "H1"): 120.0,
            ((13, 13), "H1"): 180.0,
            ((14, 14), "H1"): 250.0,
            ((15, 25), "H1"): 500.0,  # 15+ clusters
            
            # H2 - High symbol
            ((3, 3), "H2"): 0.8,
            ((4, 4), "H2"): 1.5,
            ((5, 5), "H2"): 3.0,
            ((6, 6), "H2"): 6.0,
            ((7, 7), "H2"): 12.0,
            ((8, 8), "H2"): 20.0,
            ((9, 9), "H2"): 32.0,
            ((10, 10), "H2"): 48.0,
            ((11, 11), "H2"): 65.0,
            ((12, 12), "H2"): 90.0,
            ((13, 13), "H2"): 140.0,
            ((14, 14), "H2"): 200.0,
            ((15, 25), "H2"): 400.0,  # 15+ clusters
            
            # H3 - Medium symbol
            ((3, 3), "H3"): 0.6,
            ((4, 4), "H3"): 1.2,
            ((5, 5), "H3"): 2.4,
            ((6, 6), "H3"): 4.8,
            ((7, 7), "H3"): 9.0,
            ((8, 8), "H3"): 15.0,
            ((9, 9), "H3"): 24.0,
            ((10, 10), "H3"): 36.0,
            ((11, 11), "H3"): 50.0,
            ((12, 12), "H3"): 70.0,
            ((13, 13), "H3"): 100.0,
            ((14, 14), "H3"): 150.0,
            ((15, 25), "H3"): 300.0,  # 15+ clusters
            
            # L1 - Low symbol
            ((3, 3), "L1"): 0.4,
            ((4, 4), "L1"): 0.8,
            ((5, 5), "L1"): 1.6,
            ((6, 6), "L1"): 3.2,
            ((7, 7), "L1"): 6.0,
            ((8, 8), "L1"): 10.0,
            ((9, 9), "L1"): 16.0,
            ((10, 10), "L1"): 24.0,
            ((11, 11), "L1"): 35.0,
            ((12, 12), "L1"): 50.0,
            ((13, 13), "L1"): 75.0,
            ((14, 14), "L1"): 110.0,
            ((15, 25), "L1"): 200.0,  # 15+ clusters
            
            # L2 - Lower symbol
            ((3, 3), "L2"): 0.3,
            ((4, 4), "L2"): 0.6,
            ((5, 5), "L2"): 1.2,
            ((6, 6), "L2"): 2.4,
            ((7, 7), "L2"): 4.5,
            ((8, 8), "L2"): 7.5,
            ((9, 9), "L2"): 12.0,
            ((10, 10), "L2"): 18.0,
            ((11, 11), "L2"): 26.0,
            ((12, 12), "L2"): 38.0,
            ((13, 13), "L2"): 55.0,
            ((14, 14), "L2"): 80.0,
            ((15, 25), "L2"): 150.0,  # 15+ clusters
            
            # L3 - Lowest symbol
            ((3, 3), "L3"): 0.2,
            ((4, 4), "L3"): 0.4,
            ((5, 5), "L3"): 0.8,
            ((6, 6), "L3"): 1.6,
            ((7, 7), "L3"): 3.0,
            ((8, 8), "L3"): 5.0,
            ((9, 9), "L3"): 8.0,
            ((10, 10), "L3"): 12.0,
            ((11, 11), "L3"): 18.0,
            ((12, 12), "L3"): 26.0,
            ((13, 13), "L3"): 38.0,
            ((14, 14), "L3"): 55.0,
            ((15, 25), "L3"): 100.0,  # 15+ clusters
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
