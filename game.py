from task_3_tic_tac_toe.board import Board, InvalidMovement


def main():
    """Run the game"""
    board = Board()
    end = False
    print("Do not despair, you have a big chance to win,"
          " because computer can choose only two possible moves!")
    while not end:
        print(board)
        pos = input("Enter a position to move"
                    " on using ' ' as a separator: ")
        try:
            i, j = [int(value) for value in pos.split()]
        except ValueError:
            print("Invalid format, try again")
            continue
        try:
            board.make_movement('O', (i, j))
        except InvalidMovement:
            print("Your move is invalid")
            continue

        end = board.is_win()
        if end:
            print("You won!")
            break
        comp_pos = board.make_decision()
        board.make_movement('X', comp_pos)


if __name__ == "__main__":
    main()

