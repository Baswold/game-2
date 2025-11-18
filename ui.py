"""
UI module - User interface utilities and display functions.
"""

import os
import time
from typing import List, Optional, Callable


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_separator(char: str = "=", length: int = 60):
    """Print a separator line."""
    print(char * length)


def print_header(text: str, char: str = "=", length: int = 60):
    """Print a formatted header."""
    print_separator(char, length)
    print(text.center(length))
    print_separator(char, length)


def print_box(lines: List[str], width: int = 60):
    """Print text in a box."""
    print("┌" + "─" * (width - 2) + "┐")
    for line in lines:
        padding = width - len(line) - 4
        print(f"│ {line}{' ' * padding} │")
    print("└" + "─" * (width - 2) + "┘")


def pause(message: str = "\nPress Enter to continue..."):
    """Pause and wait for user input."""
    input(message)


def get_choice(prompt: str, valid_choices: List[str],
                case_sensitive: bool = False) -> str:
    """
    Get user choice from a list of valid options.
    Returns the selected choice.
    """
    while True:
        choice = input(prompt)

        if not case_sensitive:
            choice = choice.lower()
            valid_choices = [c.lower() for c in valid_choices]

        if choice in valid_choices:
            return choice

        print(f"Invalid choice. Please choose from: {', '.join(valid_choices)}")


def get_number(prompt: str, min_val: Optional[int] = None,
                max_val: Optional[int] = None) -> int:
    """
    Get a number from user with optional range validation.
    """
    while True:
        try:
            num = int(input(prompt))

            if min_val is not None and num < min_val:
                print(f"Number must be at least {min_val}")
                continue

            if max_val is not None and num > max_val:
                print(f"Number must be at most {max_val}")
                continue

            return num

        except ValueError:
            print("Please enter a valid number.")


def get_yes_no(prompt: str, default: bool = True) -> bool:
    """
    Get yes/no response from user.
    Returns True for yes, False for no.
    """
    suffix = " (Y/n): " if default else " (y/N): "
    response = input(prompt + suffix).strip().lower()

    if not response:
        return default

    return response in ['y', 'yes']


def display_menu(title: str, options: List[str], allow_back: bool = False) -> int:
    """
    Display a menu and get user selection.
    Returns the index of selected option (0-based), or -1 for back.
    """
    print(f"\n{title}")
    print_separator("-", 40)

    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    if allow_back:
        print("0. Back")

    print_separator("-", 40)

    min_choice = 0 if allow_back else 1
    choice = get_number("Enter choice: ", min_val=min_choice, max_val=len(options))

    if choice == 0 and allow_back:
        return -1

    return choice - 1


def typewriter_print(text: str, delay: float = 0.03):
    """Print text with typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def print_stat_bar(label: str, current: int, maximum: int, width: int = 20,
                    fill_char: str = "█", empty_char: str = "░"):
    """
    Print a stat bar (like health bar).
    """
    percentage = current / maximum if maximum > 0 else 0
    filled = int(width * percentage)
    empty = width - filled

    bar = fill_char * filled + empty_char * empty
    print(f"{label}: [{bar}] {current}/{maximum}")


def display_combat_result(victory: bool, rewards: dict = None):
    """Display combat result with rewards."""
    if victory:
        print_header("⚔️ VICTORY! ⚔️", "=", 50)
        if rewards:
            print(f"\nGained {rewards.get('xp', 0)} XP!")
            print(f"Gained {rewards.get('gold', 0)} Gold!")

            loot = rewards.get('loot', [])
            if loot:
                print("\nLoot obtained:")
                from items import get_item
                for item_id in loot:
                    item = get_item(item_id)
                    if item:
                        print(f"  • {item.name}")
    else:
        print_header("💀 DEFEAT 💀", "=", 50)
        print("\nYou have been defeated...")


def display_level_up(character):
    """Display level up notification."""
    print_header(f"🌟 LEVEL UP! 🌟", "*", 50)
    print(f"\nYou are now level {character.level}!")
    print(f"You have {character.stat_points} stat points to allocate.")
    print_separator("*", 50)
    pause()


def format_time(seconds: int) -> str:
    """Format seconds into readable time string."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def display_title_screen():
    """Display the game title screen."""
    clear_screen()
    title = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        ███████╗██████╗ ██╗ ██████╗                       ║
    ║        ██╔════╝██╔══██╗██║██╔════╝                       ║
    ║        █████╗  ██████╔╝██║██║                            ║
    ║        ██╔══╝  ██╔═══╝ ██║██║                            ║
    ║        ███████╗██║     ██║╚██████╗                       ║
    ║        ╚══════╝╚═╝     ╚═╝ ╚═════╝                       ║
    ║                                                           ║
    ║           ██████╗ ██╗   ██╗███████╗███████╗████████╗     ║
    ║          ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝     ║
    ║          ██║   ██║██║   ██║█████╗  ███████╗   ██║        ║
    ║          ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║        ║
    ║          ╚██████╔╝╚██████╔╝███████╗███████║   ██║        ║
    ║           ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝        ║
    ║                                                           ║
    ║              A Text-Based RPG Adventure                   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(title)


def display_game_over():
    """Display game over screen."""
    clear_screen()
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              ██████╗  █████╗ ███╗   ███╗███████╗         ║
    ║             ██╔════╝ ██╔══██╗████╗ ████║██╔════╝         ║
    ║             ██║  ███╗███████║██╔████╔██║█████╗           ║
    ║             ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝           ║
    ║             ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗         ║
    ║              ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝         ║
    ║                                                           ║
    ║                  ██████╗ ██╗   ██╗███████╗██████╗        ║
    ║                 ██╔═══██╗██║   ██║██╔════╝██╔══██╗       ║
    ║                 ██║   ██║██║   ██║█████╗  ██████╔╝       ║
    ║                 ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗       ║
    ║                 ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║       ║
    ║                  ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝       ║
    ║                                                           ║
    ║                  Your adventure ends here...              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)


def display_victory():
    """Display victory screen."""
    clear_screen()
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║    ██╗   ██╗██╗ ██████╗████████╗ ██████╗ ██████╗ ██╗   ██╗
    ║    ██║   ██║██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝
    ║    ██║   ██║██║██║        ██║   ██║   ██║██████╔╝ ╚████╔╝
    ║    ╚██╗ ██╔╝██║██║        ██║   ██║   ██║██╔══██╗  ╚██╔╝
    ║     ╚████╔╝ ██║╚██████╗   ██║   ╚██████╔╝██║  ██║   ██║
    ║      ╚═══╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝
    ║                                                           ║
    ║         Congratulations, Hero!                            ║
    ║         You have completed your Epic Quest!               ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)


def loading_animation(text: str = "Loading", duration: float = 2.0):
    """Display a loading animation."""
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start_time = time.time()

    i = 0
    while time.time() - start_time < duration:
        print(f"\r{text} {chars[i % len(chars)]}", end='', flush=True)
        time.sleep(0.1)
        i += 1

    print(f"\r{text} Done!   ")
