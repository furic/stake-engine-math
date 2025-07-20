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
        self.game_name = "Tower Treasures"
        self.output_regular_json = True
        self.provider_number = 0
        self.working_name = "Tower Treasures"
        self.wincap = 5000.0
        self.win_type = "cluster"
        self.rtp = 0.9700
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [5] * self.num_reels  # Optionally include variable number of rows per reel
        # Board and Symbol Properties - Cluster Pay (Low symbols only)
        # Format: ((min_cluster, max_cluster), "symbol"): payout_multiplier
        # Extended cluster sizes for more diverse gameplay
        c5, c6, c8, c9, c10, c11, c12, c13, c14, c15 = (5, 5), (6, 6), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 25)
        pay_group = {
            # L1 - HIGHEST PAYING (Premium Symbol)
            (c5, "L1"): 1.0,   # 5 cluster
            (c6, "L1"): 2.0,   # 6 cluster
            (c8, "L1"): 4.0,   # 8 cluster
            (c9, "L1"): 6.0,   # 9 cluster
            (c10, "L1"): 9.0,   # 10 cluster
            (c11, "L1"): 12.5,  # 11 cluster
            (c12, "L1"): 17.5,  # 12 cluster
            (c13, "L1"): 25.0,  # 13 cluster
            (c14, "L1"): 37.5,  # 14 cluster
            (c15, "L1"): 60.0, # 15+ cluster
            
            # L2 - HIGH PAYING
            (c5, "L2"): 0.5,   # 5 cluster
            (c6, "L2"): 1.0,   # 6 cluster
            (c8, "L2"): 2.0,   # 8 cluster
            (c9, "L2"): 3.0,   # 9 cluster
            (c10, "L2"): 4.5,   # 10 cluster
            (c11, "L2"): 6.3,   # 11 cluster
            (c12, "L2"): 8.8,   # 12 cluster
            (c13, "L2"): 12.5,  # 13 cluster
            (c14, "L2"): 18.8,  # 14 cluster
            (c15, "L2"): 30.0, # 15+ cluster
            
            # L3 - MEDIUM PAYING
            (c5, "L3"): 0.2,   # 5 cluster
            (c6, "L3"): 0.4,   # 6 cluster
            (c8, "L3"): 0.8,   # 8 cluster
            (c9, "L3"): 1.2,   # 9 cluster
            (c10, "L3"): 1.8,   # 10 cluster
            (c11, "L3"): 2.5,   # 11 cluster
            (c12, "L3"): 3.5,   # 12 cluster
            (c13, "L3"): 5.0,   # 13 cluster
            (c14, "L3"): 7.5,   # 14 cluster
            (c15, "L3"): 12.0, # 15+ cluster
            
            # L4 - LOW PAYING
            (c5, "L4"): 0.1,   # 5 cluster
            (c6, "L4"): 0.2,   # 6 cluster
            (c8, "L4"): 0.4,   # 8 cluster
            (c9, "L4"): 0.6,   # 9 cluster
            (c10, "L4"): 0.9,   # 10 cluster
            (c11, "L4"): 1.3,   # 11 cluster
            (c12, "L4"): 1.8,   # 12 cluster
            (c13, "L4"): 2.5,   # 13 cluster
            (c14, "L4"): 3.8,   # 14 cluster
            (c15, "L4"): 6.0,  # 15+ cluster
            
            # L5 - LOWEST PAYING
            (c5, "L5"): 0.05,  # 5 cluster
            (c6, "L5"): 0.1,   # 6 cluster
            (c8, "L5"): 0.2,   # 8 cluster
            (c9, "L5"): 0.3,   # 9 cluster
            (c10, "L5"): 0.5,   # 10 cluster
            (c11, "L5"): 0.7,   # 11 cluster
            (c12, "L5"): 1.0,   # 12 cluster
            (c13, "L5"): 1.5,   # 13 cluster
            (c14, "L5"): 2.2,   # 14 cluster
            (c15, "L5"): 3.5,  # 15+ cluster
        }
        self.paytable = self.convert_range_table(pay_group)
        
        # Add M and H symbols to paytable so they can be registered
        # These symbols pay fixed amounts based on the prize_config
        m_h_symbols = {
            # M symbols (Medium tier)
            ((1, 1), "M1"): 2.0,
            ((1, 1), "M2"): 1.0,
            ((1, 1), "M3"): 0.4,
            ((1, 1), "M4"): 0.2,
            ((1, 1), "M5"): 0.1,
            
            # H symbols (High tier)
            ((1, 1), "H1"): 5.0,
            ((1, 1), "H2"): 2.5,
            ((1, 1), "H3"): 1.0,
            ((1, 1), "H4"): 0.5,
            ((1, 1), "H5"): 0.25,
        }
        # Add the M and H symbols to the main paytable
        self.paytable.update(m_h_symbols)

        # Upgrade System Configuration
        self.upgrade_config = {
            "symbol_map": {
                "L1": {"M": "M1", "H": "H1"},
                "L2": {"M": "M2", "H": "H2"},
                "L3": {"M": "M3", "H": "H3"},
                "L4": {"M": "M4", "H": "H4"},
                "L5": {"M": "M5", "H": "H5"},
            },
            "thresholds": {
                "medium": 5,  # 5-9 clusters upgrade to M symbols
                "high": 10,   # 10+ clusters upgrade to H symbols
            }
        }

        # Prize Symbol Payout Configuration
        # M and H symbols pay fixed amounts based on count on board
        self.prize_config = {
            "symbols": ["M1", "M2", "M3", "M4", "M5", "H1", "H2", "H3", "H4", "H5"],
            "paytable": {
                # M symbols (Medium tier) - 2x base value of corresponding L symbol
                "M1": 2.0,   # 2x multiplier
                "M2": 1.0,   # 2x multiplier  
                "M3": 0.4,   # 2x multiplier
                "M4": 0.2,   # 2x multiplier
                "M5": 0.1,   # 2x multiplier
                
                # H symbols (High tier) - 5x base value of corresponding L symbol
                "H1": 5.0,   # 5x multiplier
                "H2": 2.5,   # 5x multiplier
                "H3": 1.0,   # 5x multiplier
                "H4": 0.5,   # 5x multiplier
                "H5": 0.25,  # 5x multiplier
            }
        }

        self.include_padding = False
        self.special_symbols = {"wild": ["W"], "scatter": ["S"]}

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

        # Padding reels removed - include_padding = False, so they're not used
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
