def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-"*(4*len(row)-1))
def check_winner(board,player):
    #рядків
    for row in board:
        if all(cell==player for cell in row):
            return True
    #стовпці
    for col in range(len(board[0])):
        if all(board[row][col]==player for row in range(len(board))):
            return True
    #діагоналі
    if all(board[i][i]==player for i in range(len(board))) or all(board[i][len(board)-1-i]==player for i in range(len(board))):
        return True
    return False
def main():
    board_size=3
    board = [[" " for _ in range(board_size)] for _ in range(board_size)]
    players = ['X','O']
    current_player = 0
    while True:
        print_board(board)
        print(f"Гравець {players[current_player]} ходить.")
        try:
            row_input=input("номер рядка(1-3) ")
            row=int(row_input)-1
            col_input = input("номер стовпця(1-3) ")
            col=int(col_input)-1
            if board[row][col] !=" ":
                print("клітинка зайнята.")
                continue
            board[row][col]=players[current_player]
            if check_winner(board,players[current_player]):
                print_board(board)
                print(f"{players[current_player]} переміг!")
                break
            if all(cell !=" " for row in board for cell in row):
                print_board(board)
                print("нічия!")
                break
            current_player = (current_player + 1) % 2
        except ValueError:
            print("коректні координати.")
if __name__ == "__main__":
    main()

