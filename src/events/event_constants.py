"""Single class containing all reuseable event `type` constants."""

from enum import Enum


class EventConstants(Enum):
    "Define all standard event 'type' keys."

    # Reveal events
    REVEAL = "reveal"

    # Win events
    WIN_DATA = "win"
    SET_FINAL_WIN = "setFinalWin"
    SET_WIN = "setWin"
    SET_TOTAL_WIN = "setTotalWin"
    WIN_CAP = "winCap"

    # Freespin events
    UPDATE_FREE_SPIN = "updateFreeSpin"
    TRIGGER_FREE_SPIN = "triggerFreeSpin"
    RETRIGGER_FREE_SPIN = "retriggerFreeSpin"
    END_FREE_SPIN = "endFreeSpin"
    ENTER_BONUS = "enterBonus"

    # Tumble events
    TUMBLE_BOARD = "tumbleBoard"
    SET_TUMBLE_WIN = "setTumbleWin"
    UPDATE_TUMBLE_WIN = "updateTumbleWin"

    # Special symbol events
    UPDATE_GLOBAL_MULT = "updateGlobalMult"
    UPGRADE = "upgrade"
