# TODO: Implement Chomper Mechanics and Animations

## Tasks
- [x] Add state management variables in Chomper.__init__ (current_action, timers, cooldown)
- [x] Implement zombie detection and eating logic in Chomper.update()
- [x] Add animation handling for 'attack', 'chewing', 'chewing_to_idle' in Chomper.update()
- [x] Update Chomper.draw() to handle all animation states
- [x] Test the implementation (run the game and place Chomper)

## Notes
- Eating range: 1 cell ahead in the same row
- Instantly kill zombie on eat
- Chewing duration: ~2 seconds (adjust based on animation length)
- Cooldown after eating: 10 seconds
- Animations: 'idle', 'attack', 'chewing', 'chewing_to_idle'
