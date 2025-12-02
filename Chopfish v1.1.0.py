import math

def generate_moves(current_user_hands, current_comp_hands):
    possible_moves = []

    # 1. Implement 'pass' attacks
    for i in range(2):  # Iterate through user's hands (0 for left, 1 for right)
        if current_user_hands[i] == 0:  # Cannot attack with a dead hand
            continue

        for j in range(2):  # Iterate through computer's hands (0 for left, 1 for right)
            temp_comp_hands = list(current_comp_hands) # Create a temporary copy for modification

            # Calculate new value for the targeted computer hand
            temp_comp_hands[j] = temp_comp_hands[j] + current_user_hands[i]

            # Apply 'five becomes zero' rule
            if temp_comp_hands[j] >= 5:
                temp_comp_hands[j] = 0

            # Add the resulting game state to possible_moves
            possible_moves.append((list(current_user_hands), list(temp_comp_hands)))

    # 2. Implement 'split' actions
    for source_index in range(2):
        for target_index in range(2):
            # Cannot split to the same hand
            if source_index == target_index:
                continue

            # Cannot split from a dead hand
            if current_user_hands[source_index] == 0:
                continue

            # Iterate fingers_to_move from 1 up to the fingers in the source hand
            for fingers_to_move in range(1, current_user_hands[source_index] + 1):

                # Create a temporary copy of user hands for this split attempt
                temp_user_hands = list(current_user_hands)

                # *** REMOVED: Validation rule: Cannot split to a dead hand with any fingers ***
                # This rule has been removed as per the subtask instruction.

                # *** REMOVED: Validation rule: Target hand cannot exceed 4 fingers before 'five becomes zero' rule ***
                # This rule has been removed to allow splits where a hand reaches 5 or more and then becomes 0.
                # if temp_user_hands[target_index] + fingers_to_move >= 5:
                #    continue

                # If validation passes, perform the split
                temp_user_hands[source_index] -= fingers_to_move
                temp_user_hands[target_index] += fingers_to_move

                # Apply 'five becomes zero' rule to both hands after the split
                if temp_user_hands[0] >= 5:
                    temp_user_hands[0] = 0
                if temp_user_hands[1] >= 5:
                    temp_user_hands[1] = 0

                # Add the resulting game state to possible_moves
                possible_moves.append((list(temp_user_hands), list(current_comp_hands)))

    return possible_moves

def evaluate_game_state(user_hands, comp_hands):
    # Check for AI (computer) win
    if user_hands[0] == 0 and user_hands[1] == 0:
        return 1000

    # Check for user win
    if comp_hands[0] == 0 and comp_hands[1] == 0:
        return -1000

    # Neutral score if no one has won yet
    return 0

def minimax(current_user_hands, current_comp_hands, depth, maximizing_player, alpha, beta):
    score = evaluate_game_state(current_user_hands, current_comp_hands)
    if depth == 0 or score != 0:
        return score

    if maximizing_player: # AI's turn
        max_eval = -math.inf
        possible_next_states = generate_moves(current_comp_hands, current_user_hands) # AI's hands are 'user_hands' in generate_moves
        for ai_next_hands, user_next_hands in possible_next_states:
            eval = minimax(user_next_hands, ai_next_hands, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else: # User's turn
        min_eval = math.inf
        possible_next_states = generate_moves(current_user_hands, current_comp_hands)
        for user_next_hands, ai_next_hands in possible_next_states:
            eval = minimax(user_next_hands, ai_next_hands, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(user_hands, comp_hands, depth):
    best_eval = -math.inf
    best_move = None

    possible_moves_for_ai = generate_moves(comp_hands, user_hands)

    if not possible_moves_for_ai: # No moves for AI, might be a losing state
      return None, evaluate_game_state(user_hands, comp_hands)

    for ai_next_hands, user_next_hands in possible_moves_for_ai:
        eval = minimax(user_next_hands, ai_next_hands, depth - 1, False, -math.inf, math.inf)
        if eval > best_eval:
            best_eval = eval
            best_move = (ai_next_hands, user_next_hands)

    return best_move, best_eval


# --- Main Game Loop Implementation ---

user_hands = [1, 1]
comp_hands = [1, 1]
search_depth = 3 # Can be adjusted for difficulty

print("Welcome to Chopsticks!")
print(f"Initial State - Your hands: {user_hands}, Computer's hands: {comp_hands}")

while True:
    # 1. Check for game over before user's turn
    if (user_hands[0] == 0 and user_hands[1] == 0):
        print("\n--- Game Over ---")
        print("Computer Wins! Your hands are both 0.")
        break
    if (comp_hands[0] == 0 and comp_hands[1] == 0):
        print("\n--- Game Over ---")
        print("You Win! Computer's hands are both 0.")
        break

    # --- User's Turn ---
    print("\n--- Your Turn ---")
    print(f"Your hands: {user_hands}, Computer's hands: {comp_hands}")

    player_move_valid = False
    while not player_move_valid:
        play_choice = ""
        while play_choice not in ["pass", "stay"]:
            play_choice = input("Pass or Stay? ").lower()
            if play_choice not in ["pass", "stay"]:
                print("Invalid choice. Please enter 'Pass' or 'Stay'.")

        if play_choice == "pass":
            user_attack_index = -1
            while user_attack_index == -1:
                user_attack_choice = input("Which of your hands (Left 'l' or Right 'r') do you want to attack with? ").lower()
                if user_attack_choice == 'l':
                    if user_hands[0] == 0:
                        print("Cannot attack with a dead hand (0 fingers). Please choose another hand.")
                    else:
                        user_attack_index = 0
                elif user_attack_choice == 'r':
                    if user_hands[1] == 0:
                        print("Cannot attack with a dead hand (0 fingers). Please choose another hand.")
                    else:
                        user_attack_index = 1
                else:
                    print("Invalid choice. Please enter 'l' or 'r' for your attacking hand.")

            if user_hands[user_attack_index] == 0: # Double check in case of unexpected flow
                continue

            comp_target_index = -1
            while comp_target_index == -1:
                comp_target_choice = input("Which of the computer's hands (Left 'l' or Right 'r') do you want to attack? ").lower()
                if comp_target_choice == 'l':
                    if comp_hands[0] == 0:
                        print("Cannot attack a dead hand (0 fingers). Please choose another hand.")
                    else:
                        comp_target_index = 0
                elif comp_target_choice == 'r':
                    if comp_hands[1] == 0:
                        print("Cannot attack a dead hand (0 fingers). Please choose another hand.")
                    else:
                        comp_target_index = 1
                else:
                    print("Invalid choice. Please enter 'l' or 'r' for the computer's target hand.")

            if comp_hands[comp_target_index] == 0: # Double check in case of unexpected flow
                continue

            # Apply attack
            comp_hands[comp_target_index] += user_hands[user_attack_index]

            # Apply 'five becomes zero' rule
            if comp_hands[comp_target_index] >= 5:
                comp_hands[comp_target_index] = 0
            player_move_valid = True

        elif play_choice == "stay":
            split_successful = False
            while not split_successful:
                print("You chose to stay and split fingers.")

                source_index = -1
                while source_index == -1:
                    source_hand_choice = input("Which of your hands (Left 'l' or Right 'r') do you want to split from? ").lower()
                    if source_hand_choice == 'l':
                        if user_hands[0] == 0:
                            print("Cannot split from a dead hand (0 fingers). Please choose another hand.")
                        else:
                            source_index = 0
                    elif source_hand_choice == 'r':
                        if user_hands[1] == 0:
                            print("Cannot split from a dead hand (0 fingers). Please choose another hand.")
                        else:
                            source_index = 1
                    else:
                        print("Invalid choice. Please enter 'l' or 'r' for the source hand.")

                if user_hands[source_index] == 0: # Re-check after loop if needed
                    print("Invalid split move. Let's try selecting hands and fingers again.")
                    continue

                target_index = -1
                while target_index == -1:
                    target_hand_choice = input("Which of your hands (Left 'l' or Right 'r') do you want to split to? ").lower()
                    if target_hand_choice == 'l':
                        target_index = 0
                    elif target_hand_choice == 'r':
                        target_index = 1
                    else:
                        print("Invalid choice. Please enter 'l' or 'r' for the target hand.")

                fingers_to_move = -1
                while fingers_to_move == -1:
                    try:
                        fingers_input = input("How many fingers do you want to move? ")
                        fingers_to_move = int(fingers_input)
                        if fingers_to_move <= 0:
                            print("Number of fingers to move must be a positive whole number.")
                            fingers_to_move = -1
                    except ValueError:
                        print("Invalid number of fingers. Please enter a whole number.")
                        fingers_to_move = -1

                # Apply the same validation rules as in generate_moves
                if source_index == target_index:
                    print("Cannot split to the same hand! Please try again.")
                elif user_hands[source_index] < fingers_to_move:
                    print(f"Not enough fingers in your {source_hand_choice} hand to move {fingers_to_move} fingers! Please try again.")
                # The following validation for target hand exceeding 4 fingers is REMOVED as per the new rule:
                # elif user_hands[target_index] + fingers_to_move >= 5:
                #     print("Split would result in target hand having 5 or more fingers immediately, which is not allowed for splits. Please try again.")
                else:
                    # Perform the split
                    user_hands[source_index] -= fingers_to_move
                    user_hands[target_index] += fingers_to_move

                    # Apply 'five becomes zero' rule
                    if user_hands[0] >= 5:
                        user_hands[0] = 0
                    if user_hands[1] >= 5:
                        user_hands[1] = 0
                    split_successful = True
            player_move_valid = True

    print(f"Your move resulted in: Your hands: {user_hands}, Computer's hands: {comp_hands}")

    # Check for user win after their move
    if comp_hands[0] == 0 and comp_hands[1] == 0:
        print("\n--- Game Over ---")
        print("You Win! Computer's hands are both 0.")
        break

    # --- AI's Turn ---
    print("\n--- Computer's Turn ---")
    # Re-check for AI win/user win after user's move, before AI's move (should be handled by above check, but good to be safe)
    if user_hands[0] == 0 and user_hands[1] == 0:
        print("Computer Wins! Your hands are both 0.")
        break
    if comp_hands[0] == 0 and comp_hands[1] == 0:
        print("You Win! Computer's hands are both 0.")
        break

    best_move, evaluation = find_best_move(user_hands, comp_hands, search_depth)

    if best_move:
        # Unpack the best move into comp_hands (AI's hands) and user_hands (opponent's hands)
        # Note: find_best_move returns (ai_next_hands, user_next_hands)
        comp_hands_new = best_move[0]
        user_hands_new = best_move[1]

        # Update the game state with the AI's chosen move
        user_hands = user_hands_new
        comp_hands = comp_hands_new

        print(f"Computer made its move. Current state: Your hands: {user_hands}, Computer's hands: {comp_hands}")
    else:
        print("Computer found no valid moves. This shouldn't happen in a non-terminal state.")
        # This could imply a game over state that wasn't caught, or a bug.
        # For now, let's assume it leads to a loss for the computer if it can't move.
        if evaluate_game_state(user_hands, comp_hands) == 1000: # If user hands are 0, computer won
            print("Computer wins!")
        elif evaluate_game_state(user_hands, comp_hands) == -1000: # If computer hands are 0, user won
            print("You win!")
        else:
             print("Game error: AI couldn't find a move in a non-terminal state.")
        break

    # Check for AI win after their move
    if user_hands[0] == 0 and user_hands[1] == 0:
        print("\n--- Game Over ---")
        print("Computer Wins! Your hands are both 0.")
        break
