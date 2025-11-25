# Distributed Multiplayer Tic-Tac-Toe

This project is a distributed multiplayer Tic-Tac-Toe game built using **Python** and **socket programming**.  
It uses a **broker-based architecture**, where all communication flows through a dedicated broker process before reaching the controller or clients.

Players connect as clients, the controller manages the game logic, and the broker forwards all messages between them.

---

## 📁 Project Structure

 File Description 
| **broker.py** | The central message broker. All communication between clients and the controller goes through this process. Must be started first. |
| **controller.py** | The game server. Manages game state, validates turns, and updates players through the broker. |
| **client.py** | Player client. Connects to the broker, sends moves, and receives board updates. |
| **worker.py** | Optional helper process for move validation or offloading logic. |
| **README.md** | Documentation for the project. |

---

# 🚀 How to Run the Game

## **Step 1: Start the Broker (REQUIRED)**  
The broker handles all message passing. It must be running **before the controller or clients**.

Open a terminal in the project directory and start the broker:

```bash
python broker.py

In the second terminal
python controller.py

Run two separate terminals
python client.py

🔮 Future Improvements

Add a GUI or browser-based interface.

Persist games or add rematch handling.

Improve broker to handle multiple game rooms.



