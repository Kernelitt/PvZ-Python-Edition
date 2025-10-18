# Store Implementation Tasks

## 1. Create StoreItem Class
- Define StoreItem class with attributes: icon (pygame image), cost (int), position (tuple), page (int or str)
- Use SimpleImageButton for interaction

## 2. Integrate StoreItem into Store Class
- Add a list of StoreItem instances to Store.__init__
- Populate the list with sample items (e.g., plants with costs from definitions.py)
- Modify draw method to render items on the current page
- Add page navigation if multiple pages

## 3. Add Item Purchase Logic
- Implement on_click for StoreItem to check user coins and deduct if sufficient
- Update user.json with purchased items or upgrades

## 4. Test Store Functionality
- Run the game, navigate to store, verify items display
- Test purchasing items and coin deduction
