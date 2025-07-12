"""

"""

from game_calculations import GameCalculations
from src.calculations.cluster import Cluster
from game_events import reveal_event
from src.events.events import (
    fs_trigger_event,
    win_info_event,
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
        fs_trigger_event(self, basegame_trigger=basegame_trigger, freegame_trigger=freegame_trigger)

    def update_freespin(self) -> None:
        """Called before a new reveal during freegame."""
        self.fs += 1
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
            win_info_event(self, include_padding_index=False)
            # Generate upgrade events after win events
            self.generate_upgrade_events()
            # Generate prize payout events after all upgrades
            self.generate_prize_payout_events()

    def generate_upgrade_events(self):
        """Generate upgrade events for each winning symbol."""
        import random
        
        self.upgrade_positions = {}  # Track upgraded positions for prize payout
        
        for win in self.win_data["wins"]:
            symbol = win["symbol"]
            positions = win["positions"]
            cluster_count = len(positions)
            
            # Only upgrade L symbols with clusters of 5 or more
            if symbol.startswith("L") and cluster_count >= 5:
                # Pick a random position from the winning cluster
                random_position = random.choice(positions)
                
                # Generate upgrade event
                upgrade_event(self, symbol, random_position, positions)
                
                # Track the upgraded symbol for prize payout
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
                        
                        if upgraded_symbol not in self.upgrade_positions:
                            self.upgrade_positions[upgraded_symbol] = []
                        self.upgrade_positions[upgraded_symbol].append(random_position)

    def generate_prize_payout_events(self):
        """Generate prize payout events for M and H symbols from upgrade events."""
        # Check if we have any upgraded positions to pay out
        if not hasattr(self, 'upgrade_positions') or not self.upgrade_positions:
            return
        
        # Check if game has prize configuration
        if not hasattr(self.config, 'prize_config'):
            return
            
        prize_config = self.config.prize_config
        prize_paytable = prize_config["paytable"]
        
        total_prize_amount = 0
        details = []
        
        for symbol_name, positions in self.upgrade_positions.items():
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

    def draw_board(self, emit_event: bool = True, trigger_symbol: str = "scatter") -> None:
        """Override to use custom reveal_event without paddingPositions and anticipation."""
        # Call parent draw_board but without emitting the event
        super().draw_board(emit_event=False, trigger_symbol=trigger_symbol)
        
        # Emit our custom reveal_event if needed
        if emit_event:
            reveal_event(self)
