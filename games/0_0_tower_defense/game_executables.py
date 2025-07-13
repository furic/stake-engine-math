"""

"""

from game_calculations import GameCalculations
from src.calculations.cluster import Cluster
from game_events import reveal_event
from src.events.events import (
    freespin_trigger_event,
    win_event,
    update_global_mult_event,
    update_freespin_event,
    upgrade_event,
    prize_payout_event,
)


class GameExecutables(GameCalculations):
    """Game specific executable functions. Used for grouping commonly used/repeated applications."""

    def update_freespin_amount(self, scatter_key: str = "scatter"):
        """Update current and total freespin number and emit event."""
        self.tot_fs = self.count_special_symbols(scatter_key) * 2
        if self.gametype == self.config.basegame_type:
            basegame_trigger, freegame_trigger = True, False
        else:
            basegame_trigger, freegame_trigger = False, True
        freespin_trigger_event(self, basegame_trigger=basegame_trigger, freegame_trigger=freegame_trigger)

    def update_freespin(self) -> None:
        """Called before a new reveal during freegame."""
        self.fs += 1
        
        # Initialize sticky symbols tracking only on the very first free spin
        if self.fs == 1 and not hasattr(self, 'sticky_symbols'):
            self.initialize_sticky_symbols()
        
        update_freespin_event(self)
        # This game does not reset the global multiplier on each spin
        self.global_multiplier = 1
        # Skip updateGlobalMult for tower defense game (will be added back in "super" mode later)
        # update_global_mult_event(self)
        self.win_manager.reset_spin_win()
        self.tumblewin_mult = 0
        self.win_data = {}

    def get_clusters_update_wins(self):
        """Find clusters on board and update win manager - simplified without tumbling."""
        clusters = Cluster.get_clusters(self.board, "wild")
        return_data = {
            "totalWin": 0,
            "wins": [],
        }

        # Custom cluster evaluation without exploding symbols (no tumbling)
        total_win = 0
        for sym in clusters:
            for cluster in clusters[sym]:
                syms_in_cluster = len(cluster)
                if (syms_in_cluster, sym) in self.config.paytable:
                    sym_win = self.config.paytable[(syms_in_cluster, sym)]
                    symwin_mult = sym_win * self.global_multiplier
                    total_win += symwin_mult
                    json_positions = [{"reel": p[0], "row": p[1]} for p in cluster]

                    return_data["wins"] += [
                        {
                            "symbol": sym,
                            "clusterSize": syms_in_cluster,
                            "win": symwin_mult,
                            "positions": json_positions,
                            "meta": {
                                "globalMult": self.global_multiplier,
                                "winWithoutMult": sym_win,
                            },
                        }
                    ]
                    # No exploding symbols - clusters stay on board

        return_data["totalWin"] = total_win
        self.win_data = return_data
        
        # Record wins for statistics
        for win in self.win_data["wins"]:
            self.record({
                "kind": win["clusterSize"],
                "symbol": win["symbol"],
                "mult": int(win["meta"]["globalMult"]),
                "gametype": self.gametype,
            })
        
        self.win_manager.update_spinwin(self.win_data["totalWin"])
        
        # Emit win events if there are any wins
        if self.win_data["totalWin"] > 0:
            win_event(self, include_padding_index=False)
            # Generate upgrade events after win events
            self.generate_upgrade_events()
            
            # Note: Prize payout is now handled at the end of each spin, not here

    def generate_upgrade_events(self):
        """Generate upgrade events for each winning symbol."""
        import random
        
        for win in self.win_data["wins"]:
            symbol = win["symbol"]
            positions = win["positions"]
            cluster_count = len(positions)
            
            # Only upgrade L symbols with clusters of 5 or more
            if symbol.startswith("L") and cluster_count >= 5:
                # Pick a random position from the winning cluster
                random_position = random.choice(positions)
                
                # Determine what symbol it was upgraded to
                if hasattr(self.config, 'upgrade_config'):
                    upgrade_config = self.config.upgrade_config
                    symbol_map = upgrade_config["symbol_map"]
                    thresholds = upgrade_config["thresholds"]
                    
                    if symbol in symbol_map:
                        if cluster_count >= thresholds["high"]:
                            upgraded_symbol = symbol_map[symbol]["H"]
                        elif cluster_count >= thresholds["medium"]:
                            upgraded_symbol = symbol_map[symbol]["M"]
                        else:
                            continue
                        
                        # Generate upgrade event
                        upgrade_event(self, symbol, random_position, positions)
                        
                        # Place the upgraded symbol on the board immediately
                        self.board[random_position["reel"]][random_position["row"]] = self.create_symbol(upgraded_symbol)
                        
                        # Add to sticky symbols during free spins - THIS IS CRITICAL!
                        if self.gametype == self.config.freegame_type:
                            if not hasattr(self, 'sticky_symbols'):
                                self.initialize_sticky_symbols()
                            self.add_sticky_symbol(upgraded_symbol, random_position)

    def generate_prize_payout_events(self):
        """Generate prize payout events for M and H symbols currently on the board."""
        # Check if game has prize configuration
        if not hasattr(self.config, 'prize_config'):
            return
            
        prize_config = self.config.prize_config
        prize_symbols = prize_config["symbols"]
        prize_paytable = prize_config["paytable"]
        
        # Scan the board for M and H symbols
        board_symbols = {}
        for reel in range(len(self.board)):
            for row in range(len(self.board[reel])):
                symbol_name = self.board[reel][row].name
                if symbol_name in prize_symbols:
                    if symbol_name not in board_symbols:
                        board_symbols[symbol_name] = []
                    board_symbols[symbol_name].append({"reel": reel, "row": row})
        
        # Generate prize payout if we have M or H symbols
        if board_symbols:
            total_prize_amount = 0
            details = []
            
            for symbol_name, positions in board_symbols.items():
                if symbol_name in prize_paytable:
                    count = len(positions)
                    symbol_payout = prize_paytable.get(symbol_name, 0)
                    amount = int(round(symbol_payout * count * 100, 0))
                    total_prize_amount += amount
                    
                    details.append({
                        "symbol": symbol_name,
                        "positions": positions,
                        "amount": amount,
                        "count": count,
                        "baseAmount": amount,
                        "multiplier": 1
                    })
            
            # Create the prize payout event if there are any prizes
            if total_prize_amount > 0:
                event = {
                    "index": len(self.book.events),
                    "type": "win",
                    "reason": "prize",
                    "total": total_prize_amount,
                    "details": details,
                }
                self.book.add_event(event)
                
                # Update win manager with the prize amount
                prize_win_amount = total_prize_amount / 100.0  # Convert back to float
                self.win_manager.update_spinwin(prize_win_amount)

    def draw_board(self, emit_event: bool = True, trigger_symbol: str = "scatter") -> None:
        """Override to handle sticky symbols and use custom reveal_event."""
        # Call parent draw_board but without emitting the event
        super().draw_board(emit_event=False, trigger_symbol=trigger_symbol)
        
        # Replace board with sticky symbols if we're in free spins
        if self.gametype == self.config.freegame_type:
            self.replace_board_with_stickys()
        
        # Emit our custom reveal_event if needed
        if emit_event:
            reveal_event(self)

    def initialize_sticky_symbols(self):
        """Initialize sticky symbols tracking for free spins."""
        self.sticky_symbols = []  # List of sticky symbol details
        self.existing_sticky_positions = []  # Track positions that have sticky symbols

    def add_sticky_symbol(self, symbol_name: str, position: dict):
        """Add a new sticky symbol to track during free spins."""
        if not hasattr(self, 'sticky_symbols'):
            self.initialize_sticky_symbols()
        
        reel, row = position["reel"], position["row"]
        pos_tuple = (reel, row)
        
        # Check if position already has a sticky symbol
        if pos_tuple not in self.existing_sticky_positions:
            sticky_details = {
                "reel": reel,
                "row": row,
                "symbol": symbol_name,
            }
            self.sticky_symbols.append(sticky_details)
            self.existing_sticky_positions.append(pos_tuple)

    def replace_board_with_stickys(self):
        """Replace board positions with sticky symbols before each free spin reveal."""
        # Ensure sticky symbols are initialized
        if not hasattr(self, 'sticky_symbols'):
            self.initialize_sticky_symbols()
            
        if not self.sticky_symbols:
            return
        
        for sticky in self.sticky_symbols:
            # Create the sticky symbol on the board
            self.board[sticky["reel"]][sticky["row"]] = self.create_symbol(sticky["symbol"])

    def check_for_new_sticky_symbols(self):
        """Check the board for new M and H symbols that should become sticky."""
        if not hasattr(self, 'sticky_symbols'):
            self.initialize_sticky_symbols()
        
        new_sticky_symbols = []
        
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                symbol_name = self.board[reel][row].symbol
                pos_tuple = (reel, row)
                
                # Check if this is an M or H symbol that isn't already sticky
                if (symbol_name.startswith("M") or symbol_name.startswith("H")) and pos_tuple not in self.existing_sticky_positions:
                    sticky_details = {
                        "reel": reel,
                        "row": row,
                        "symbol": symbol_name,
                    }
                    new_sticky_symbols.append(sticky_details)
                    self.sticky_symbols.append(sticky_details)
                    self.existing_sticky_positions.append(pos_tuple)
        
        return new_sticky_symbols
