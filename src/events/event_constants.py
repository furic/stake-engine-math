"""Single class containing all reuseable event `type` constants."""

from enum import Enum


class EventConstants(Enum):
    "Define all standard event 'type' keys."

    # Reveal events
    REVEAL = "reveal"

    # Win events
    WIN = "win"
    SET_FINAL_WIN = "setFinalWin"
    SET_WIN = "setWin"
    SET_TOTAL_WIN = "setTotalWin"
    WIN_CAP = "winCap"

    # Freespins events
    UPDATE_FREE_SPINS = "updateFreeSpins"
    TRIGGER_FREE_SPINS = "triggerFreeSpins"
    RETRIGGER_FREE_SPINS = "retriggerFreeSpins"
    END_FREE_SPINS = "endFreeSpins"

    # Tumble events
    TUMBLE_BOARD = "tumbleBoard"
    SET_TUMBLE_WIN = "setTumbleWin"
    UPDATE_TUMBLE_WIN = "updateTumbleWin"

    # Special symbol events
    UPDATE_GLOBAL_MULT = "updateGlobalMult"
    UPGRADE = "upgrade"
