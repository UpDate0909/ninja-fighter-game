# Basic Networking Setup for Ninja Game

This document outlines a conceptual plan for implementing online multiplayer in the Ninja Game.

## 1. Recommended Architecture

*   **Choice:** Client-Server.
*   **Justification for a 2-player fighting game:**
    *   **Authority:** A client-server model provides a clear "source of truth." The server is authoritative over the game state (positions, health, etc.), which helps prevent inconsistencies and makes cheating harder to implement by malicious clients. In a P2P setup, resolving conflicting game states between two peers can be complex (e.g., if both players register a hit simultaneously on their own machines, who is correct?).
    *   **Simplicity for 2 Players:** While P2P can work for 2 players, client-server is often simpler to manage for initial implementation, especially regarding who makes the final decision on game events.
    *   **NAT Traversal:** P2P connections often face more significant challenges with Network Address Translation (NAT) traversal, as both peers might be behind routers. In a client-server model (especially with a dedicated server, or if the server player can configure port forwarding), only one side (the server) needs to be directly reachable.
*   **Server Type (Initial):** Listen Server.
    *   One of the players will act as the server (host). This is simpler to implement initially than a dedicated server, as it doesn't require separate server infrastructure. The player who starts the game and waits for another player to join would typically be the server.

## 2. Recommended Protocol

*   **Choice:** Start with TCP, consider UDP for optimization later.
*   **TCP (Transmission Control Protocol):**
    *   **Pros:**
        *   **Reliability:** Guarantees that data arrives in order and without loss. This is crucial for critical game events like "attack initiated," "jump started," or "damage taken." If these messages are lost, the game state becomes inconsistent.
        *   **Connection-Oriented:** Establishes a connection before data transfer, ensuring both ends are ready.
        *   **Simpler to Start:** Python's `socket` module makes TCP programming relatively straightforward.
    *   **Cons:**
        *   **Latency:** The overhead for ensuring reliability (acknowledgments, retransmissions) can introduce more latency than UDP. In a fast-paced fighting game, this could be noticeable.
        *   **Head-of-Line Blocking:** If a packet is lost, subsequent packets in the stream might be delayed until the lost one is retransmitted, even if the later packets are for more up-to-date game states.
*   **UDP (User Datagram Protocol):**
    *   **Pros:**
        *   **Speed/Low Latency:** Minimal overhead as it's connectionless and doesn't guarantee delivery or order. This is good for sending frequent updates like player positions where a lost packet is less critical than a delayed one (the next packet will have newer position data anyway).
        *   **No Head-of-Line Blocking:** Packets are independent.
    *   **Cons:**
        *   **Unreliability:** Packets can be lost, duplicated, or arrive out of order. This requires implementing a custom reliability layer on top of UDP for critical game messages if UDP is used exclusively.
        *   **More Complex for Mixed Data:** If you need both reliable and unreliable messages, you either send everything reliably (e.g., over TCP) or implement your own reliability mechanism over UDP for specific message types.
*   **Starting Point Recommendation:**
    *   Begin with **TCP**. For a 2-player game where initial simplicity of development is key, TCP's reliability for all game events (inputs, state changes) will reduce the number of synchronization bugs. Once the core game logic is working over TCP, and if latency becomes a noticeable issue, specific parts (like continuous position updates) could be considered for optimization, potentially by adding a UDP channel for them or implementing techniques like input prediction and state reconciliation.

## 3. Core Data to Synchronize

The following data needs to be sent between server and client:

*   **Player Inputs/Actions (Client to Server):**
    *   Movement commands (left, right, jump).
    *   Attack initiation.
    *   (Potentially: specific attack types, blocking).
*   **Game State (Server to Client(s)):**
    *   **Player 1 (Server's Player) & Player 2 (Client's Player) Information:**
        *   Position (x, y coordinates).
        *   Current action/state (idle, running, jumping, attacking, taking damage, etc.). This is important for animations and game logic.
        *   Vertical velocity (if jumping).
        *   `is_attacking` status and `attack_timer` (or just the visual effect of attack).
        *   Health.
        *   Facing direction (left/right).
    *   **Game World State (if applicable):**
        *   Positions of any projectiles or dynamic objects (not currently in the game, but for future).
    *   **Game Score/Status:**
        *   Round winner/loser.
        *   Game timer.
        *   Match score.

## 4. Python Libraries/Modules

*   **`socket` module (built-in):**
    *   This is the standard Python library for low-level network programming. It supports both TCP and UDP. For a first implementation, this is sufficient and provides a good learning experience.
*   **`asyncio` (built-in, with `socket` or `asyncio.streams`):**
    *   Can be used for managing multiple connections or non-blocking operations more gracefully, especially on the server side if it were to handle more than one client (though for a listen server with 1 client, it might be overkill initially but good for future scaling).
*   **Third-party libraries (Consider for later, not first implementation):**
    *   **Twisted:** A mature, event-driven networking engine. More complex than `socket` but very powerful.
    *   **PyZMQ:** For message queue patterns, might be an option for more complex communication but likely overkill for this game.
    *   **Game-specific networking libraries (e.g., PodSixNet - though might be old):** These often provide higher-level abstractions for game networking. Research would be needed for current, well-maintained options if `socket` proves too cumbersome.

    For a first, simple implementation, **`socket`** is the recommended starting point.

## 5. Basic Data Flow (Client-Server Example with Listen Server)

Let Player 1 be the Server and Player 2 be the Client.

**Server (Player 1's machine):**
1.  **Initialization:**
    *   Starts its Pygame instance.
    *   Creates its Ninja object (Player 1).
    *   Creates a placeholder Ninja object for Player 2.
    *   Opens a TCP listening socket on a specific IP address and port.
    *   Waits for Player 2 (Client) to connect.
2.  **Connection Established:**
    *   Accepts the client's connection. Now has a dedicated socket for communication with Player 2.
3.  **Game Loop:**
    *   **Input:** Processes Player 1's local inputs (keyboard) for movement, jump, attack.
    *   **Receive from Client:**
        *   Receives a message (e.g., a string or JSON object) from Player 2 containing Player 2's inputs/actions (e.g., "LEFT", "JUMP", "ATTACK"). This should be non-blocking or handled in a separate thread/async task to avoid freezing the server's game.
    *   **Update Game State:**
        *   Updates Player 1's Ninja object based on Player 1's local input.
        *   Updates Player 2's Ninja object based on the received inputs from Player 2.
        *   Runs the game logic (physics, collision detection - including hit detection between players, health updates). The server is the authority here.
    *   **Send to Client:**
        *   Serializes the relevant game state (positions of both ninjas, health of both, current actions, etc.) into a message (e.g., JSON string).
        *   Sends this complete game state to Player 2 (Client).
    *   **Render:** Updates its local Pygame display based on the new game state.

**Client (Player 2's machine):**
1.  **Initialization:**
    *   Starts its Pygame instance.
    *   Creates its Ninja object (Player 2).
    *   Creates a placeholder Ninja object for Player 1.
    *   Gets the server's IP address and port (e.g., entered by the user).
2.  **Connection:**
    *   Creates a TCP socket and connects to the server.
3.  **Game Loop:**
    *   **Input:** Processes Player 2's local inputs (keyboard).
    *   **Send to Server:**
        *   Serializes Player 2's inputs/actions into a message.
        *   Sends this message to the server.
    *   **Receive from Server:**
        *   Receives the authoritative game state message from the server. This should be non-blocking or handled carefully.
    *   **Update Local State:**
        *   Deserializes the message.
        *   Updates its local representations of Player 1's Ninja and Player 2's Ninja (and any other relevant game objects) based *entirely* on the data received from the server. The client's own Ninja object's state is overridden by the server's state for synchronization. (Client-side prediction can be added later to make client's own movements feel more responsive, but the server state is still the truth).
    *   **Render:** Updates its local Pygame display.

**Data Serialization:**
*   Data like positions, actions, etc., needs to be converted into a byte stream for sending over the network and then parsed back. JSON strings are a common and human-readable way to do this for simple structures. For performance, more compact binary formats could be used later.

This outline provides a starting point. Actual implementation will involve handling many details like error conditions, disconnections, message formatting, and potentially more advanced synchronization techniques as the game grows.
---
This markdown file contains the requested research and outline.
I have covered:
1.  **Architecture:** Client-Server (Listen Server).
2.  **Protocol:** Start with TCP, consider UDP later.
3.  **Core Data:** Player inputs and comprehensive game state.
4.  **Python Libraries:** `socket` module as the primary choice.
5.  **Basic Data Flow:** Detailed steps for server and client.

I believe this fulfills all the requirements of the subtask.



*******************************************************************


# 🚀 Ninja Fighter Game

2D-файтинг, посвящённый боевым искусствам ниндзя. Прототип в активной разработке, демонстрирующий ключевые механики файтинга.

## 📋 Содержание
- [Основные возможности](#основные-возможности)
- [Требования](#требования)
- [Установка](#установка)
- [Как запустить игру](#как-запустить-игру)

## 🥷 Основные возможности
- 🥷 Два игровых персонажа-ниндзя.
- 🕹️ Базовые движения: ходьба влево/вправо и прыжки с учётом гравитации.
- ⚔️ Атака с определённым хитбоксом и системой обнаружения попаданий.
- ❤️ Полоски здоровья, уменьшающиеся при получении урона.
- 👥 Локальный мультиплеер для двух игроков на одном устройстве.
- 🏁 Условие окончания игры и перезапуск матча.
- 🎨 Визуальная обратная связь:
  - Анимации бездействия/ходьбы (изменение цвета).
  - Анимация атаки (изменение цвета и увеличение размера).
  - Реакция на удар (изменение цвета и прерывание).
- 🔊 Звуковые эффекты для прыжков, атак, попаданий и окончания игры

## 📋 Требования
- Python 3.x
- Библиотека Pygame

## 🛠️ Установка
Установите Pygame:
pip install pygame

## Как запустить игру
Вариант 1: Клонирование репозитория
Откройте терминал.

Перейдите в нужный каталог:
cd путь/к/папке

Клонируйте репозиторий:
git clone <https://github.com/UpDate0909/ninja-game-test.git>

Перейдите в папку проекта:
cd ninja_game

Запустите игру:
python src/main.py

Вариант 2: Скачивание ZIP-архива
Скачайте ZIP-архив со страницы репозитория (кнопка «Code» → «Download ZIP»).

Распакуйте архив.

Перейдите в папку:
cd путь/к/папке/ninja_game-main

Запустите игру:
python src/main.py

 Общие замечания
Убедитесь, что Python и Pygame добавлены в PATH.

Главный скрипт: src/main.py.
