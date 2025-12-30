# PixelSoundAlert

A desktop application that monitors specific screen pixels and plays sounds when their colors change from a baseline. Perfect for gaming alerts, automation, or any scenario where you need audio notifications based on visual changes.

## Features

- **Multi-Area Monitoring**: Monitor multiple screen pixels simultaneously
- **Color Change Detection**: Detects when pixel colors deviate from a baseline color
- **Customizable Thresholds**: Adjustable sensitivity for color change detection (0-100)
- **Conditional Logic**: Optional secondary pixel (Pixel B) condition to control when sounds play
- **Audio Support**: Supports WAV and MP3 audio files with volume control (0-100%)
- **Real-time Color Display**: Live preview of monitored pixel colors with RGB values
- **Save/Load Configurations**: Save and load monitoring area configurations as JSON files
- **Easy Setup**: Click-to-select pixel coordinates with visual overlay

## Requirements

- Python 3.7 or higher
- Windows OS (uses `winsound` for audio playback)
- Dependencies:
  - `pillow>=10.0.0` - For screen capture and pixel color reading
  - `pydub>=0.25.1` - For audio file handling and format conversion

## Installation

### Option 1: Using Pre-built Executable

1. Download `PixelSoundAlert.exe` from the [Releases](https://github.com/MertenNor/PixelSoundAlert/releases) page
2. Run the executable - no installation required!

### Option 2: From Source

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/PixelSoundAlert.git
   cd PixelSoundAlert
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Building from Source

To create a standalone executable:

### Windows
```bash
build.bat
```

### Linux/Mac
```bash
chmod +x build.sh
./build.sh
```

The executable will be created in the `dist` folder.

**Note**: Building requires PyInstaller, which will be automatically installed if missing.

## Usage

### Basic Setup

1. **Select Pixel Coordinates**: Click "Select Pixel A" and click anywhere on your screen to set the monitoring pixel
2. **Capture Baseline Color**: Click "Capture Baseline" to record the current pixel color as the baseline
3. **Select Sound File**: Click "Select Sound" and choose a WAV or MP3 file to play when color changes
4. **Configure Settings**:
   - **Threshold** (0-100): Sensitivity for color change detection (default: 30)
   - **Volume** (0-100): Sound playback volume percentage
5. **Start Monitoring**: Click "START ALL" to begin monitoring

### Advanced: Conditional Logic

Enable the "Use Condition" checkbox to add a secondary pixel check:

1. **Select Pixel B**: Click "Select Pixel B" and choose a secondary pixel
2. **Capture Condition Color**: Click "Capture Condition" to record the required color for Pixel B
3. **How it works**: The sound will only play when:
   - Pixel A changes from baseline color **AND**
   - Pixel B matches the condition color

This is useful for scenarios where you want to play a sound only when multiple conditions are met.

### Managing Multiple Areas

- **Add Area**: Click the "Add Area" button to monitor additional pixels
- **Remove Area**: Click "Remove" on any area (at least one area must remain)
- **Save Configuration**: Use "Save Layout" to save all area settings to a JSON file
- **Load Configuration**: Use "Load Layout" to restore previously saved settings

## Project Structure

```
PixelSoundAlert/
├── main.py                 # Application entry point
├── src/
│   └── pixel_monitor/
│       ├── app.py          # Main application class
│       ├── audio/
│       │   └── player.py   # Audio playback handling
│       ├── config/
│       │   ├── settings.py # Settings management
│       │   └── layout_manager.py  # Configuration save/load
│       ├── gui/
│       │   ├── main_window.py     # Main GUI window
│       │   └── area_widget.py     # Individual area UI components
│       └── monitor/
│           ├── pixel_monitor.py   # Core monitoring logic
│           └── color_utils.py    # Color comparison utilities
├── assets/                 # Sound files and resources
├── build/                  # Build artifacts
├── dist/                   # Compiled executables
├── requirements.txt        # Python dependencies
└── PixelSoundAlert.spec   # PyInstaller configuration
```

## How It Works

1. The application continuously monitors specified screen pixels at a high frequency (50ms intervals)
2. It compares the current pixel color with the stored baseline color
3. When the color difference exceeds the threshold, it triggers the sound
4. If conditional logic is enabled, it also checks that Pixel B matches the condition color
5. The sound plays once per color change event (won't repeat until color returns to baseline)

## Troubleshooting

- **Sound not playing**: Ensure the sound file path is valid and the file format is supported (WAV/MP3)
- **Color not detected**: Try adjusting the threshold value - lower values are more sensitive
- **Application not responding**: Check that all required fields are filled (coordinates, baseline, sound file)
- **Build errors**: Ensure PyInstaller is installed: `pip install pyinstaller`

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Built with:
- Python
- Tkinter (GUI)
- Pillow (Image processing)
- PyDub (Audio processing)
- PyInstaller (Executable building)

