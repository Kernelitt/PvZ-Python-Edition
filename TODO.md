# TODO: Доработка меню выбора уровней

## добавить прогрессию по уровням тоесть на 1-2 не попасть пока 1-1 не пройден
    1. images/MiniGame_trophy.png - можно использовать чтобы отметить что уровень пройден (нужно распологать на тех же координатах что и self.window_image)
    2. images/lock.png - можно использовать чтобы отметить что уровень закрыт (нужно отображать в центре self.window_image)
    3. нужно создать словарь user. он будет использоваться для хранения всего прогресса в игре (пройденные уровни, растения в коллекции). изначально у игрока будет только Peashooter
    4. нужно добавить награду за прохождение уровней (например новые растения)

## Implementation Steps
- [ ] Load trophy and lock images in Menu.__init__
- [ ] Determine unlocked and completed status for each level in Menu.__init__
- [ ] Modify Menu.draw to show lock for locked levels and trophy for completed
- [ ] Modify Menu.handle_events to prevent clicking locked levels
- [ ] Modify SeedSelect.__init__ to filter plants by unlocked_plants
- [ ] Modify MainGame win condition to update user progress and save user.json
