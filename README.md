# Distributed Multiplayer Tic-Tac-Toe

This project is a distributed multiplayer Tic-Tac-Toe game built using Python and socket programming. It allows two players to play Tic-Tac-Toe over the network, where one machine acts as the controller and both players act as clients.

## Project Structure

- `controller.py`: The server that manages the game state and handles communication with the clients.
- `client.py`: The client code that connects to the controller and allows players to make their moves.
- `worker.py`: A separate process responsible for validating player moves (optional depending on how you set up).
- `README.md`: This file that explains the project.

## How to Run the Game

### Step 1: Start the Controller
1. Open a terminal in the project directory.
2. Run the following command to start the game server (controller):
   ```bash
   python controller.py
### Step 2: Run Player     You're absolutely right! Step 2 and Step 3 should be included in the `README.md` to make it complete and clear. Here's the revised version of the `README.md` with the missing steps:

---

### **Revised `README.md`**

````markdown
# Distributed Multiplayer Tic-Tac-Toe

This project is a distributed multiplayer Tic-Tac-Toe game built using Python and socket programming. It allows two players to play Tic-Tac-Toe over the network, where one machine acts as the controller and both players act as clients.

## Project Structure

- `controller.py`: The server that manages the game state and handles communication with the clients.
- `client.py`: The client code that connects to the controller and allows players to make their moves.
- `worker.py`: A separate process responsible for validating player moves (optional depending on how you set up).
- `README.md`: This file that explains the project.

## How to Run the Game

### Step 1: Start the Controller
1. Open a terminal in the project directory.
2. Run the following command to start the game server (controller):
   ```bash
   python controller.py
````

The controller will start and wait for clients to connect.

### Step 2: Run Player Clients

1. Open two separate terminals (one for Player X and one for Player O).
2. In the first terminal, run the following command to start Player X:

   ```bash
   python client.py
   ```
3. In the second terminal, run the following command to start Player O:

   ```bash
   python client.py
   ```

   Both clients will connect to the controller, and you will see a message welcoming each player to the game.

### Step 3: Play the Game

* Once both players are connected, they can take turns making moves by entering numbers between 0 and 8, corresponding to the positions on the Tic-Tac-Toe board. The game will display the updated board after each move.
* The game ends when a player wins or the game is a draw.
* Players will be prompted for their move with messages like:

  * `Your move (0-8):`
* After the game ends, the result will be displayed, and the game can be restarted by running the `controller.py` and `client.py` again.

### Step 4: Enjoy the Game

* The game will print the board and announce the winner after a player wins or if the game is a draw.
* Players can continue making moves until the game ends.

## Notes

* This game works locally on a single machine for testing purposes, with both players running on the same computer in separate terminal windows.

## Future Enhancements

* Add the ability to play over the internet (by using public IPs and appropriate port forwarding).
* Introduce a better UI (e.g., web-based or with a graphical user interface).


This should now provide a complete guide for anyone wanting to run the game, whether on the same machine or across different terminals. Let me know if you have any more questions or need further clarification!
