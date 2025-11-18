# Epic Quest - Troubleshooting Guide

## Installation Issues

### Python Version Error
**Problem**: `SyntaxError` or `ImportError` when running

**Solution**:
```bash
# Check Python version
python --version

# Should be 3.8 or higher
# If not, install Python 3.8+
```

### Game Won't Start
**Problem**: `python main.py` does nothing or errors

**Solutions**:
1. Ensure you're in the correct directory:
```bash
cd game-2
ls main.py  # Should show main.py
```

2. Try with explicit python3:
```bash
python3 main.py
```

3. Check file permissions:
```bash
chmod +x main.py
./main.py
```

### Module Not Found
**Problem**: `ModuleNotFoundError: No module named 'X'`

**Solution**: The game uses only standard library. This shouldn't happen unless:
- Python installation is corrupted
- Typo in import statements
- Using very old Python version

Try reinstalling Python 3.8+

---

## Gameplay Issues

### Can't Save Game
**Problem**: Save fails or "Permission denied" error

**Solutions**:
1. Check disk space
2. Ensure write permissions:
```bash
ls -la saves/
chmod 755 saves/  # If saves directory exists
mkdir saves  # If it doesn't exist
```

3. Try saving with a simple name (no special characters)

### Can't Load Save
**Problem**: Save file not appearing or load fails

**Solutions**:
1. Check saves directory exists and has files:
```bash
ls saves/
```

2. Verify save file format:
```bash
cat saves/your_save.json | python -m json.tool
```

3. If corrupted, try loading a different save

4. Last resort - start new game

### Save File Corrupted
**Problem**: JSON parse error when loading

**Solution**:
1. Make backup:
```bash
cp saves/your_save.json saves/your_save_backup.json
```

2. Try to fix JSON:
```bash
python -m json.tool saves/your_save.json > saves/your_save_fixed.json
```

3. If unfixable, revert to older save or start new game

### Game Crashes During Combat
**Problem**: Unexpected exit or error during battle

**Solutions**:
1. Check error message - may indicate:
   - Invalid item use
   - Character state issue
   - Enemy data problem

2. Try:
   - Reloading save before battle
   - Fighting different enemy
   - Reporting bug with error message

### Inventory Full Can't Pick Up Items
**Problem**: Can't collect important items

**Solutions**:
1. Drop or sell unwanted items
2. Increase inventory in save file (advanced):
```json
"inventory": {
    "max_capacity": 100  # Change from 50
}
```

---

## Balance Issues

### Game Too Easy
**Problem**: Breezing through content, no challenge

**Solutions**:
1. Fight higher-level enemies
2. Try harder locations earlier
3. Limit potion use
4. Try a challenge run:
   - No shops
   - No grinding
   - Minimum level attempts

### Game Too Hard
**Problem**: Dying frequently, can't progress

**Solutions**:
1. **Level up more** - Grind easier enemies
2. **Better equipment**:
   - Buy from shops
   - Craft if possible
   - Find treasures
3. **More potions** - Keep 10+ at all times
4. **Stat allocation**:
   - Warriors: HP + Strength
   - Mages: Intelligence + Luck
   - Rogues: Agility + Luck
5. **Save before tough fights**
6. **Return to town to rest** (full HP for 20g)

### Boss Too Strong
**Problem**: Can't beat boss enemy

**Preparation Checklist**:
- [ ] 10+ Health Potions (appropriate tier)
- [ ] Best equipment for your level
- [ ] Full HP before fight
- [ ] Save file before attempt
- [ ] Level at or above boss level

**Strategy**:
- Keep HP above 50%
- Defend if next hit might kill you
- Use potions strategically
- Attack when safe

### Can't Find Quest Items
**Problem**: Quest item not dropping or appearing

**Solutions**:
1. Check quest objectives - might need specific enemy/location
2. Explore all areas of quest location
3. Some quest items are treasures, not drops
4. Check inventory - might already have it
5. Try returning to quest giver

---

## Technical Issues

### Slow Performance
**Problem**: Game lags or responds slowly

**Solutions**:
- This shouldn't happen with this game
- Close other programs
- Check Python version (newer is faster)
- Reduce terminal history buffer

### Terminal Display Issues
**Problem**: Text garbled, boxes broken, weird characters

**Solutions**:
1. Use UTF-8 compatible terminal:
```bash
export LANG=en_US.UTF-8
```

2. Terminal compatibility:
   - Linux: Most terminals work
   - Mac: Terminal.app or iTerm2
   - Windows: Use Windows Terminal or PowerShell

3. Font issues - use monospace font

### Can't See Full Text
**Problem**: Lines cut off or wrapped weirdly

**Solutions**:
1. Increase terminal width (resize window)
2. Terminal settings → Columns: 80 minimum
3. Some displays designed for 60-70 char width

### Colors Not Showing
**Problem**: Expected colors but seeing plain text

**Note**: Game doesn't use colors by default
- Uses ASCII characters and formatting
- Box drawing characters
- Symbols for rarity

If you see weird symbols, your terminal may not support Unicode.

---

## Data Issues

### Lost All Progress
**Problem**: Saves disappeared

**Solutions**:
1. Check saves directory:
```bash
ls -la saves/
```

2. Search for save files:
```bash
find ~ -name "*.json" -path "*/saves/*"
```

3. Check backup if you made one

4. If truly lost, start new game
   - Experience will help you progress faster
   - Try different class/build

### Stats Seem Wrong
**Problem**: Stats don't match what you expect

**Checks**:
1. Remember: Displayed stats = Base + Equipment bonuses
2. Unequip items to see base stats
3. Equipment might have negative stats
4. Some classes start with stat penalties

### Duplicate Items
**Problem**: Items appearing multiple times

**Note**: This is normal for:
- Stackable items (materials, potions)
- Items bought/found multiple times

Not normal for:
- Quest items (usually unique)
- Some equipment (might indicate bug)

If truly bugged, edit save file to remove.

---

## Quest Issues

### Quest Not Progressing
**Problem**: Killed enemy/found item but quest not updating

**Checks**:
1. Right enemy? Check exact name
2. Right item? Check quest log
3. Quest active? Must accept quest first
4. Try completing objective again

**Solutions**:
- Save and reload
- Check quest manager
- Report if persistent bug

### Quest Can't Complete
**Problem**: All objectives done but can't turn in

**Checks**:
1. Visit quest giver location
2. Use "Complete Quest" menu option
3. All objectives actually complete?

**Solutions**:
- Save and reload
- Check quest log for missed objectives

### Quest Disappeared
**Problem**: Quest was active, now gone

**Checks**:
1. Check completed quests
2. Check available quests
3. Might have been removed accidentally

**Solution**: Quest progress saved in save file, can be restored

---

## Character Issues

### Can't Allocate Stats
**Problem**: Stat allocation fails or not available

**Checks**:
1. Do you have stat points? (Level up to get)
2. Trying to allocate to valid stat?
3. Can't allocate directly to current HP

**Solutions**:
- Allocate to max_hp instead of hp
- Check stat_points value in character screen

### Equipment Won't Equip
**Problem**: Can't equip item you own

**Checks**:
1. Level requirement met?
2. Right slot for item type?
3. Item in inventory (not equipped)?

**Solutions**:
- Level up if req not met
- Unequip current item first (if inventory full)
- Check item type matches slot

### Lost Equipped Items
**Problem**: Items disappeared when equipping/unequipping

**This shouldn't happen** - items should:
- Go to inventory when unequipped
- Previous item return when replacing

If this happens:
1. Check inventory thoroughly
2. Check save file
3. Report bug

---

## Combat Issues

### Damage Seems Wrong
**Problem**: Dealing too much/little damage

**Damage Formula**:
- Player: (Strength × 2) + Weapon Damage
- Critical: 1.5x damage
- Enemy Defense: Reduces damage (Defense × 0.5)
- Minimum: Always at least 1 damage

**Check**:
- Your strength stat
- Weapon damage
- Enemy defense
- Critical hit?

### Can't Flee from Battle
**Problem**: Flee fails repeatedly

**Flee Mechanics**:
- Base 50% chance
- Agility increases chance
- Higher level enemy reduces chance
- Multiple attempts reduce chance

**Solutions**:
- Keep trying (RNG)
- Increase agility
- Fight lower-level enemies
- Use potions and fight through

### Battle Frozen
**Problem**: Combat stuck, can't select action

**Solutions**:
1. Check for input prompt
2. Try entering a number
3. Press Enter
4. Ctrl+C to abort, reload save

---

## Advanced Troubleshooting

### Edit Save File
**Backup first!**
```bash
cp saves/your_save.json saves/backup.json
```

**Edit carefully**:
```bash
nano saves/your_save.json
# or
vim saves/your_save.json
```

**Common edits**:
- Restore gold: `"gold": 9999`
- Fix HP: `"hp": 100`
- Add items: `"items": {"health_potion_small": 99}`
- Fix level: `"level": 10`

**Validate after editing**:
```bash
python -m json.tool saves/your_save.json
```

### Debug Mode
Currently no debug mode, but can add print statements:

In main.py, add after imports:
```python
DEBUG = True
if DEBUG:
    print(f"Character HP: {character.hp}")
```

### Report a Bug

If you find a real bug:
1. Note exact steps to reproduce
2. Save the game state
3. Note error message (if any)
4. Create issue on GitHub with:
   - Python version
   - OS
   - Steps to reproduce
   - Expected vs actual behavior
   - Save file (if relevant)

---

## Still Having Issues?

### Resources
- [README](README.md) - Basic info
- [Game Guide](GAME_GUIDE.md) - Complete guide
- [Quick Start](QUICK_START.md) - Fast tutorial

### Getting Help
1. Read documentation thoroughly
2. Check if issue is in FAQ
3. Try searching error message
4. Create GitHub issue with details

### Worst Case
- Start new game
- Try different approach
- Consider it a learning experience!

---

## Preventative Measures

### Best Practices
1. **Save frequently** - Multiple slots
2. **Backup saves**:
```bash
cp -r saves saves_backup
```
3. **Update regularly** - Check for game updates
4. **Read patch notes** - Know what changed
5. **Test new features** - On backup save first

### Healthy Gaming
- Take breaks every hour
- Don't play while tired (mistakes happen)
- Save before risky decisions
- Have fun - it's a game!

---

*Most issues can be solved by saving and reloading. When in doubt, save often!*
