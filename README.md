Zombie Escape
Top-down wave survival shooter built with Python and Pygame. Move around
the arena, aim with the mouse, and survive waves of zombies.
Getting Started
Requirements
- Python 3.12 or newer
- pygame-ce (Community Edition)
Install the dependency:
py -m pip install pygame-ce
Run the game from the project folder:
py game.py
Note: pygame-ce is a drop-in replacement for the Pygame API and
is recommended by the project instructions for Python 3.12 or newer.

Controls
  Key                           Action
  W / A / S / D or Arrow keys   Move
  Left mouse button             Shoot toward the cursor
  E                             Reload the magazine
  R                             Restart the game
Before Changing the Code
Play several waves and observe how zombies spawn, move, and are killed.
Trace the shooting logic from the mouse-click event through Player to
bullet collision. Understand wave progression and how score and kill
counters interact before making modifications.
Task 1 --- Health System
- The player starts with 3 HP.
- Zombie contact subtracts 1 HP.
- A brief invincibility window after a hit prevents repeated damage.
- The HUD displays current health.
- Game over occurs only when HP reaches 0.
Done when: the player survives multiple zombie touches, the
invincibility window is visible, and the game-over screen appears only
at 0 HP.
Task 2 --- Ammo System
- Magazine capacity is 12 bullets.
- Each successful shot consumes one bullet.
- Shooting is blocked when the magazine is empty or while reloading.
- Press E to reload; reloading takes 2 seconds.
- The HUD displays current ammo and reload status.
Done when: shooting is blocked at 0 ammo, reloading completes after
the full two-second duration, and ammo is restored only when reloading
finishes.
Task 3 --- Explosive Barrels
- Four barrels are placed on the map.
- A bullet hitting an active barrel triggers an explosion.
- The explosion damages zombies within a fixed radius.
- An exploded barrel is removed and cannot explode again.
Current implementation settings: 100-pixel explosion radius and 3
damage per explosion.
Done when: barrels are visible, a bullet collision triggers the
explosion effect, nearby zombies are damaged or removed when defeated,
and the barrel disappears.
Task 4 --- Zombie Types
Add two zombie variants alongside standard zombies:
- Fast Zombie: smaller, faster, and has 1 HP.
- Tank Zombie: larger, slower, and has 6 HP.
Mix both variants into wave spawning while preserving standard zombie
behaviour and wave progression.
Status: Fast and Tank zombie variants are not included in the
current implementation yet.
Done when: both variants spawn in waves, their different stats are
reflected in combat, and wave progression continues to work.
Required Testing
- Survive several waves and verify health and invincibility.
- Empty the magazine and reload it.
- Shoot a barrel beside a group of zombies and check the blast radius.
- Verify Fast and Tank zombies spawn and behave correctly once Task 4
  is implemented.
- Confirm game over occurs only at 0 HP.
- Test restarting after game over.
- Confirm scoring, movement, shooting, and wave progression still
  work.
LLM Usage
The lab permits use of an LLM as a coding assistant while the student
remains responsible for understanding and testing the result.
- Inspect existing code before requesting changes.
- Ask for explanations when a proposed change is unclear.
- Test generated code against the stated behaviour and edge cases.
- Keep the complete LLM chat history for submission.
- Do not replace the project with an unrelated implementation.
Submission Checklist
- [ ] Tasks 1--4 completed and tested.
- [ ] Health and invincibility work correctly.
- [ ] Ammo limit and reload mechanic work correctly.
- [ ] Barrels explode and damage nearby zombies.
- [ ] Fast and Tank zombie types spawn and behave as specified.
- [ ] No unnecessary external dependencies beyond Pygame.
- [ ] Code remains understandable and modular.
- [ ] Complete LLM chat-history link is included.
Lab 4 Deliverables
Submit the following three items as required by the lab instructions:
1. A 10-second gameplay video before making changes.
2. A 10-second gameplay video after making changes, showing the new
   features working.
3. The ChatGPT/LLM page link with the complete chat history.
Suggested video filenames: - before.mp4 - after.mp4
Repository
Personal project repository:
https://github.com/vikhyathks-10/25_zombie_escape
