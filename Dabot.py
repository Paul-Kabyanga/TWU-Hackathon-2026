# bot_template.py
# Template for participants to create their own chess bot

import chess
from chess_player import ChessPlayer
import random


class Dabot(ChessPlayer):
    """
    Create your own chess bot by inheriting from ChessPlayer!
    
    To use your bot:
    1. Copy this file and rename it (e.g., my_awesome_bot.py)
    2. Replace 'YourCustomBot' with your bot's name
    3. Implement the make_move() method with your logic
    4. Import and use it in main.py or other files
    
    Example in main.py:
        from my_awesome_bot import MyAwesomeBot
        player1 = SecureBotWrapper(MyAwesomeBot, "My Bot Name")
    """

    def make_move(self, board):
        """
        Args:
            board: chess.Board object representing the current game state

        Returns:
            chess.Move: Your chosen move, or None if no moves available

        Tips:
            - board.legal_moves gives you all valid moves
            - board.is_capture(move) checks if a move captures a piece
            - board.piece_at(square) gets the piece at a square (or None)
            - board.fen() returns the position in FEN notation
            - board.turn returns chess.WHITE or chess.BLACK
        """

        # Get all legal moves
        global random
        legal_moves = list(board.legal_moves)

        if not legal_moves:
            return None

        piece_values = {1: 100, 2: 320, 3: 330, 4: 500, 5: 900, 6: 0}

        safemoves = []
        captures = [m for m in legal_moves if board.is_capture(m)]
        fin = []

        # IMPLEMENT YOUR LOGIC HERE!
        # This prioritizes moves, it prioritizes safe captures, then safe moves, then any legal moves

        for i in legal_moves:
            board.push(i)
            safe = not board.is_attacked_by(not board.turn, i.to_square)
            board.pop()

            if safe:
                safemoves.append(i)

        if safemoves:
            safe_captures = [m for m in safemoves if m in captures]
            if safe_captures:
                safe_captures.sort(
                    key=lambda m: piece_values.get(board.piece_type_at(m.to_square), 0),
                    reverse=True
                )
                return safe_captures[0]
            else:
                fin.extend(safemoves)
                return random.choice(fin)
        else:
            return random.choice(legal_moves)


       # return random.choice(legal_moves)


# ===== EXAMPLE IMPLEMENTATIONS =====

class DefensiveBot(ChessPlayer):
    """Prefers to move pieces to safe squares and avoid captures"""

    def make_move(self, board):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        import random

        # Try to find a move that doesn't leave our piece hanging
        safe_moves = []
        for move in legal_moves:
            board.push(move)
            # Check if our piece is under attack after this move
            is_safe = not board.is_attacked_by(not board.turn, move.to_square)

            board.pop()

            if is_safe:
                safe_moves.append(move)

        if safe_moves:
            return random.choice(safe_moves)
        else:
            return random.choice(legal_moves)


class AggressiveBot(ChessPlayer):
    """Prioritizes capturing opponent pieces"""

    def make_move(self, board):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        import random

        # Separate captures and quiet moves
        captures = [m for m in legal_moves if board.is_capture(m)]

        # Prefer captures, but make regular moves if none available
        if captures:
            return random.choice(captures)
        else:
            return random.choice(legal_moves)
