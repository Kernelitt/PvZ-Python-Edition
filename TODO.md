# TODO: Add Mechanics for Remaining Plants, Water Cells, and New Levels

## 1. Update levels.json
- [x] Add levels 3-1, 3-2, 4-1, 4-2 with water_rows: [2,3], background: "background3.png" for pool, "background4.png" for fog, waves: 10/20, etc.

## 2. Modify main.py GameField
- [x] Add water_rows from level_data
- [x] Draw water tiles for water rows (blue instead of green)
- [x] Restrict planting: only LilyPad on water, aquatic plants on land/LilyPad
- [ ] Allow planting on LilyPad by modifying grid to hold base + planted

## 3. Update plants.py
- [ ] Add shooting to PuffShroom (spores)
- [ ] Add sun production to SunShroom
- [ ] Add fume shooting to FumeShroom
- [ ] Add Chomper eating mechanics
- [ ] Make Repeater shoot two peas
- [ ] Modify LilyPad to allow planted_plant

## 4. Test
- [ ] Test planting restrictions
- [ ] Test plant mechanics
- [ ] Play new levels
