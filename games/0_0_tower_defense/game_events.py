from copy import deepcopy
from src.events.event_constants import EventConstants


def json_ready_sym(symbol: object, special_attributes: list = None):
    """Converts a symbol to dictionary/JSON format."""
    assert special_attributes is not None
    print_sym = {"name": symbol.name}
    attrs = vars(symbol)
    for key, val in attrs.items():
        if key in special_attributes and symbol.get_attribute(key) != False:
            print_sym[key] = val
    return print_sym


def reveal_event(gamestate):
    """Display the initial board drawn from reelstrips - Tower Defense custom version without paddingPositions and anticipation."""
    board_client = []
    special_attributes = list(gamestate.config.special_symbols.keys())
    for reel, _ in enumerate(gamestate.board):
        board_client.append([])
        for row in range(len(gamestate.board[reel])):
            board_client[reel].append(json_ready_sym(gamestate.board[reel][row], special_attributes))

    if gamestate.config.include_padding:
        for reel, _ in enumerate(board_client):
            board_client[reel] = [json_ready_sym(gamestate.top_symbols[reel], special_attributes)] + board_client[
                reel
            ]
            board_client[reel].append(json_ready_sym(gamestate.bottom_symbols[reel], special_attributes))

    event = {
        "index": len(gamestate.book.events),
        "type": EventConstants.REVEAL.value,
        "board": board_client,
        "gameType": gamestate.gametype,
    }
    gamestate.book.add_event(event)


BOARD_MULT_INFO = "boardMultiplierInfo"


def send_mult_info_event(gamestate, board_mult: int, mult_info: dict, base_win: float, updatedWin: float):
    multiplier_info, winInfo = {}, {}
    multiplier_info["positions"] = []
    if gamestate.config.include_padding:
        for m in range(len(mult_info)):
            multiplier_info["positions"].append(
                {"reel": mult_info[m]["reel"], "row": mult_info[m]["row"] + 1, "multiplier": mult_info[m]["value"]}
            )
    else:
        for m in range(len(mult_info)):
            multiplier_info["positions"].append(
                {"reel": mult_info[m]["reel"], "row": mult_info[m]["row"], "multiplier": mult_info[m]["value"]}
            )

    winInfo["tumbleWin"] = int(round(min(base_win, gamestate.config.wincap) * 100))
    winInfo["boardMult"] = board_mult
    winInfo["totalWin"] = int(round(min(updatedWin, gamestate.config.wincap) * 100))

    assert round(updatedWin, 1) == round(base_win * board_mult, 1)
    event = {
        "index": len(gamestate.book.events),
        "type": BOARD_MULT_INFO,
        "multInfo": multiplier_info,
        "winInfo": winInfo,
    }
    gamestate.book.add_event(event)
