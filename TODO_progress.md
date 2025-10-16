# Coin System Integration Progress

## Pending Tasks
- [x] Add self.coins = [] in MainGame.__init__.
- [x] Ensure coins are updated in MainGame.update_wave (already partially there).
- [x] Add coin collection handling in MainGame.update (similar to sun collection).
- [ ] Add coin drawing in MainGame.draw (similar to sun drawing).
- [ ] Add coin count display in MainGame.draw_hotbar or similar (bottom left).
- [ ] Save coin_count to user.json on collection (in Coin.collect or MainGame.update).

## Followup steps
- [ ] Test coin spawning on zombie death.
- [ ] Test coin falling animation and ground collision.
- [ ] Test coin rendering.
- [ ] Test coin collection increments count, plays sound, saves.
- [ ] Run game to ensure no errors and full functionality.
