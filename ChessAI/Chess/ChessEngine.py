class GameState:
    # ve ban co
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        # self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = ()  # toa do o vuong noi bat tot qua duong kha thi
        self.enpassantPossibleLog = [self.enpassantPossible]
        # nhap thanh
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    # nhap mot buoc di chuyen lam tham so va thuc hien no
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # ghi lai qua trinh di chuyen
        self.whiteToMove = not self.whiteToMove  # doi luot choi

        # cap nhat vi tri cua vua neu di chuyen
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # tot thang cap
        if move.isPawnPromotion:
            # promotion = input('Select Q, R, N, B:')
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # neu tot tien 2 o, co the bat tot qua duong
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:  # tot tien 2 buoc
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.endCol)
        else:
            self.enpassantPossible = ()

        # bat tot qua duong
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'

        # nhap thanh
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # vi tri vua
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]  # di chuyen xe
                self.board[move.endRow][move.endCol + 1] = '--'  # vi tri trong noi xe o
            else:  # vi tri hau
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # xe di chuyen
                self.board[move.endRow][move.endCol - 2] = '--'  # vi tri trong noi xe o

        self.enpassantPossibleLog.append(self.enpassantPossible)

        # cap nhat nhap thanh
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        #
        # self.checkmate = True
        # self.stalemate = True

    # hoan tac dong tac cuoi cung duoc thuc hien
    def undoMove(self):
        if len(self.moveLog) != 0:  # dam bao co dong thai de hoan tac
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved  # dat quan vao o vuong
            self.board[move.endRow][move.endCol] = move.pieceCaptured   # dat lai quan
            self.whiteToMove = not self.whiteToMove  # chuyen doi quay lai
            # cap nhật vị trí cua vua
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            # hoan tac tot qua duong
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'  # de trong o vuong ha canh
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                # self.enpassantPossible = (move.endRow, move.endCol)
            # hoan tac 2 o vuong tot thang tien
            # if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            #    self.enpassantPossible = ()
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            # tra lai nhap thanh neu da di chuyen
            self.castleRightsLog.pop()  # xoa su cap nhat di chuyen
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            # hoan tac nhap thanh
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # ben vua
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:  # ben hau
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'

            self.checkmate = False
            self.stalemate = False

    # kiem tra tat ca cac trang thai
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        # 1. tao ra tat ca cac nuoc di co the
        moves = self.getAllPossibleMoves()
        # 2. cho moi lan di chuyen, hay di chuyen
        for i in range(len(moves) - 1, -1, -1):  # khi xoa khoi danh sach, quay nguoc lai danh sach do
            self.makeMove(moves[i])
            # 3. tao ra tat ca cac nuoc di cua doi thu
            # 4. voi moi nuoc di cua doi thu, hay ..
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])   # 5. neu doi thu tan cong vua, do khong la nuoc di hop le
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:  # thang hoac hoa
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    def getValidMove(self):
        moves = []
        self.inCheck, self.pins, self.checks, self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:  # only 1 check, block check or move king
                moves = self.getAllPossibleMoves()
                # to block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]  # enemy piece causing the check
                validSquares = []  # squares that pieces can make to
                # if knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquares = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquares)
                        if validSquares[0] == checkRow and validSquares[1] == checkCol:
                            break

                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return moves


    # xac dinh xem nguoi choi hien tai co duoc kiem tra khong
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # xac dinh xem ke thu co tan cong o (r, c)
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # chuyen sang luot di cua doi thu
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # chuyen doi quay lai
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # o vuong bi tan cong
                return True
        return False

    # kiem tra cac buoc di chuyen
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # so hang
            for c in range(len(self.board[r])):  # so cot cho hang
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # goi ham di chuyen dua tren loai quan co
        return moves

    # nhan tat ca nuoc di cua con tot o hang, cot va them nuoc di nay vao danh sach
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == '--':
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == '--':
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnPassantMove=True))
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnPassantMove=True))
        else:
            if self.board[r + 1][c] == '--':
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnPassantMove=True))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnPassantMove=True))

    # nhan tat ca nuoc di cua con xe o hang, cot va them nuoc di nay vao danh sach
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # khong gian trong hop le
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # quan khong hop le
                        break
                else:
                    break

    # nhan tat ca nuoc di cua con ma o hang, cot va them nuoc di nay vao danh sach
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # khong phai quan dong minh
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # nhan tat ca nuoc di cua con tuong o hang, cot va them nuoc di nay vao danh sach
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # khong gian trong hop le
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # quan khong hop le
                        break
                else:
                    break

    # nhan tat ca nuoc di cua con hau o hang, cot va them nuoc di nay vao danh sach
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    # nhan tat ca nuoc di cua con vua o hang, cot va them nuoc di nay vao danh sach
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # khong phai quan dong minh
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # tao ra tat ca cac nhap thanh hop le va them vao danh sach di chuyen
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return  # khong nhap thanh khi dang chieu
        if (self.whiteToMove and self.currentCastlingRight.wks) or\
                (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or\
                (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    # nhap thanh ben vua hop le
    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    # nhap thanh ben hau hop le
    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3]:
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    # cap nhat nhap thanh
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:  # xe ben trai
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:  # xe ben phai
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # xe ben trai
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:  # xe ben phai
                    self.currentCastlingRight.bks = False


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassantMove=False, isPawnPromotion=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # self.isPawnPromotion = isPawnPromotion
        # thang cap cho tot
        self.isPawnPromotion = self.pieceMoved[1] == 'p' and (self.endRow == 0 or self.endRow == 7)

        # bat tot qua duong
        self.isEnpassantMove = isEnPassantMove
        self.isEnpassantMove = isEnPassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        # nhap thanh
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        # print(self.moveID)

    # ghi de phuong thuc bang
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # co the them de cho giong ki hieu co vua
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
