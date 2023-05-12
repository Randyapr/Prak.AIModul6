def draw_board(board):
     "Fungsi untuk menggambar papan permainan"
     print(board[0] + "|" + board[1] + "|" + board[2])
     print("-+-+-")
     print(board[3] + "|" + board[4] + "|" + board[5])
     print("-+-+-")
     print(board[6] + "|" + board[7] + "|" + board[8])
def check_win(board, player):
     "Fungsi untuk memeriksa apakah seorang pemain menang"
     win_positions = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
     for positions in win_positions:
          if board[positions[0]] == player and board[positions[1]] == player and board[positions[2]] == player:
            return True
     return False
def tic_tac_toe():
     "Fungsi untuk menjalankan permainan Tic Tac Toe"
     board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
     players = ["X", "O"]
     turn = 0
     while True:
          draw_board(board)
          print("Player " + players[turn] + "'s turn.")
          position = int(input("Ambil Posisi (1-9): ")) - 1
          if board[position] != " ":
               print("Position already taken. Choose another one.")
               continue
          board[position] = players[turn]
          if check_win(board, players[turn]):
               draw_board(board)
               print("Player " + players[turn] + " wins!")
               break
          if " " not in board:
               draw_board(board)
               print("It's a tie!")
               break
          turn = (turn + 1) % 2
if __name__ == "__main__":
  tic_tac_toe()
