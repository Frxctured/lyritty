import os
import warnings
# These must come before apparently
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
warnings.filterwarnings('ignore', category=RuntimeWarning)
import argparse
import subprocess
import sys
import time
import pygame
import pylrc
from typing import Optional

def clear_screen():
    if os.name != "nt":
        subprocess.run(["clear"])
    else:
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    pass

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


BLOCKS = {
    '(': [' █', '█ ', '█ ', '█ ', ' █'],
    ')': ['█ ', ' █', ' █', ' █', '█ '],
    ',': ['  ', '  ', '  ', ' █', '█ '],
    '\'': ['█', '█', ' ', ' ', ' '],
    '0': ['█████', '█   █', '█   █', '█   █', '█████'],
    '1': ['    █', '    █', '    █', '    █', '    █'],
    '2': ['█████', '    █', '█████', '█    ', '█████'],
    '3': ['█████', '    █', '█████', '    █', '█████'],
    '4': ['█   █', '█   █', '█████', '    █', '    █'],
    '5': ['█████', '█    ', '█████', '    █', '█████'],
    '6': ['█████', '█    ', '█████', '█   █', '█████'],
    '7': ['█████', '    █', '    █', '    █', '    █'],
    '8': ['█████', '█   █', '█████', '█   █', '█████'],
    '9': ['█████', '█   █', '█████', '    █', '█████'],
    'A': ['█████', '█   █', '█████', '█   █', '█   █'],
    'B': ['████ ', '█   █', '████ ', '█   █', '████ '],
    'C': ['█████', '█    ', '█    ', '█    ', '█████'],
    'D': ['████ ', '█   █', '█   █', '█   █', '████ '],
    'E': ['█████', '█    ', '███  ', '█    ', '█████'],
    'F': ['█████', '█    ', '███  ', '█    ', '█    '],
    'G': ['█████', '█    ', '█  ██', '█   █', '█████'],
    'H': ['█   █', '█   █', '█████', '█   █', '█   █'],
    'I': ['█████', '  █  ', '  █  ', '  █  ', '█████'],
    'J': ['█████', '    █', '    █', '█   █', '█████'],
    'K': ['█   █', '█  █ ', '███  ', '█  █ ', '█   █'],
    'L': ['█    ', '█    ', '█    ', '█    ', '█████'],
    'M': ['█   █', '██ ██', '█ █ █', '█   █', '█   █'],
    'N': ['█   █', '██  █', '█ █ █', '█  ██', '█   █'],
    'O': ['█████', '█   █', '█   █', '█   █', '█████'],
    'P': ['████ ', '█   █', '████ ', '█    ', '█    '],
    'Q': ['█████', '█   █', '█   █', '█  ██', '█████'],
    'R': ['████ ', '█   █', '████ ', '█   █', '█   █'],
    'S': ['█████', '█    ', '█████', '    █', '█████'],
    'T': ['█████', '  █  ', '  █  ', '  █  ', '  █  '],
    'U': ['█   █', '█   █', '█   █', '█   █', ' ███ '],
    'V': ['█   █', '█   █', ' █ █ ', ' █ █ ', '  █  '],
    'W': ['█   █', '█   █', '█ █ █', '██ ██', '█   █'],
    'X': ['█   █', ' █ █ ', '  █  ', ' █ █ ', '█   █'],
    'Y': ['█   █', '█   █', ' █ █ ', '  █  ', '  █  '],
    'Z': ['█████', '    █', ' ███ ', '█    ', '█████'],
    ' ': ['     ', '     ', '     ', '     ', '     '],
}

def text_to_blocks(text: str) -> str:
    """Convert text to big unicode block letters"""
    text = text.upper()
    lines = ['', '', '', '', '']
    for char in text:
        if char in BLOCKS:
            block = BLOCKS[char]
            for i in range(5):
                lines[i] += block[i] + '  '
        else:
            # Unknown character, just add spaces
            for i in range(5):
                lines[i] += '       '
    return '\n'.join(lines)

def center_text(text: str, width: int) -> str:
    """Center multi-line text"""
    lines = text.split('\n')
    centered_lines = []
    for line in lines:
        centered_lines.append(line.center(width))
    return '\n'.join(centered_lines)


class Song:
    def __init__(
            self, 
            song_path: Optional[str], 
            lyrics_path: Optional[str], 
            audio_path: Optional[str]
            ):
        
        self.song_path = song_path
        self.lyrics_path = lyrics_path
        self.audio_path = audio_path
        self.lyrics = self._get_lyrics()
        self.audio = self._get_audio()

    def _get_lyrics(self):
        if self.song_path != None:
            lrc_file = open(f"{self.song_path}.lrc")
            lrc_string = ''.join(lrc_file.readlines())
            return pylrc.parse(lrc_string)
        elif self.lyrics_path != None:
            lrc_file = open(self.lyrics_path)
            lrc_string = ''.join(lrc_file.readlines())
            return pylrc.parse(lrc_string)
        else:
            sys.exit(1)

    def _get_audio(self):
        if os.path.exists(f"{self.song_path}.mp3"):
            return f"{self.song_path}.mp3"
        elif self.audio_path != None and os.path.exists(self.audio_path):
            return self.audio_path
        else:
            return None
    
    def display_with_timing(self):
        if self.audio != None:
            pygame.mixer.init()
            pygame.mixer.music.load(self.audio)
            pygame.mixer.music.play()
        
        # Clear screen and hide cursor
        clear_screen()
        hide_cursor()
        
        start_time = time.time()
        
        # Get the last lyric time to know when to stop
        last_lyric_time = self.lyrics[-1].time if self.lyrics else 0
        
        previous_lyric = None  # Track previous lyric to avoid redrawing
        
        try:
            while True:
                # If audio is playing, check if it's still busy
                if self.audio != None and not pygame.mixer.music.get_busy():
                    break
                
                elapsed = time.time() - start_time
                
                # If no audio, exit when we've passed the last lyric
                if self.audio == None and elapsed > last_lyric_time + 5:
                    break
                
                # Find the appropriate lyric for current time
                current_lyric = None
                for lyric_line in self.lyrics:
                    if lyric_line.time <= elapsed:
                        current_lyric = lyric_line.text
                    else:
                        break
                
                # Only update display if lyric changed
                if current_lyric and current_lyric != previous_lyric:
                    previous_lyric = current_lyric
                    big_text = text_to_blocks(current_lyric)
                    # Get terminal dimensions
                    try:
                        size = os.get_terminal_size()
                        width = size.columns
                        height = size.lines
                    except:
                        width = 80
                        height = 24
                    
                    # Center horizontally
                    centered_text = center_text(big_text, width)
                    
                    # Center vertically
                    text_lines = centered_text.split('\n')
                    blank_lines_before = (height - len(text_lines)) // 2
                    
                    # Clear screen and move cursor to home
                    clear_screen()
                    # Move down to vertical center
                    for _ in range(blank_lines_before):
                        sys.stdout.write("\033[B")
                    sys.stdout.write(centered_text)
                    sys.stdout.flush()
                
                time.sleep(0.01)  # Avoid CPU spinning
        
        finally:
            if self.audio != None:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            show_cursor()
            clear_screen()

def main():
    parser = argparse.ArgumentParser(description="A command line lyrics tool")

    parser.add_argument(
        'path', 
        nargs='?', 
        help="song path without the extention (e.g: path/to/song not path/to/song.mp3)"
    )

    parser.add_argument(
        '-l', '--lyrics', 
        help="Path to the .lrc file"
    )
    parser.add_argument(
        '-a', '--audio', 
        help="Path to the .mp3 file"
    )

    args = parser.parse_args()

    if not args.path and not args.lyrics:
        parser.error("the following arguments are required: -l/--lyrics (when 'path' is omitted)")

    if args.path and (args.lyrics or args.audio):
        parser.error("You cannot mix the positional 'path' argument with -l or -a flags.")

    if args.path:
        song = Song(args.path, None, None)
        try:
            song.display_with_timing()
        except KeyboardInterrupt:
            sys.exit(0)
    else:
        song = Song(None, args.lyrics, args.audio)
        try:
            song.display_with_timing()
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    main()
