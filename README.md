# TraceVibe

## About the Tool
TraceVibe is a powerful Open-Source Intelligence (OSINT) tool designed to search for usernames across 33 popular social media, professional, and other online platforms. It helps users identify the presence of a username on platforms like Twitter, GitHub, Instagram, LinkedIn, Reddit, and many more, making it a valuable tool for digital investigations, cybersecurity research, or simply exploring online identities.

Key features include:
- Username search across 33 platforms.
- Platform-specific "not found" checks for improved accuracy.
- Interactive CLI menu with a user-friendly interface powered by Rich.
- Batch processing of usernames via input files.
- Filtering results by platform or status (Found/Not Found).
- Export results to JSON or CSV formats.
- Caching to speed up repeated searches.
- Option to continue or exit after each search.

**Note**: Results may require manual verification for accuracy, as some platforms may return false positives or negatives due to rate limiting, URL patterns, or platform-specific behavior.

## Created by Technical Corp
TraceVibe is proudly created by **Technical Corp**, a team dedicated to building innovative tools for cybersecurity, OSINT, and digital forensics. We aim to empower users with reliable and easy-to-use solutions for exploring the digital landscape.

## Installation

### Prerequisites
Ensure you have Python 3.6+ installed on your system. You can check your Python version by running:
```bash
python --version
```

### Step 1: Clone the Repository
Clone the TraceVibe repository to your local machine:
```bash
git clone https://github.com/techcorp/tracevibe.git
cd tracevibe
```

### Step 2: Install Dependencies
Install the required Python packages using pip:
```bash
pip install requirements.txt
```

- `requests`: For making HTTP requests to check usernames.
- `beautifulsoup4`: For parsing HTML responses.
- `rich`: For the enhanced CLI interface (tables, progress bars, etc.).
- `pandas`: For exporting results to CSV format.

### Step 3: Verify Setup
Ensure the script is ready by running:
```bash
python tracevibe.py --help
```
This should display the help message with available command-line arguments.

## Usage

### Running the Tool
TraceVibe can be run in two modes: interactive or via command-line arguments.

#### Interactive Mode
Run the script without arguments to use the interactive menu:
```bash
python tracevibe.py
```
You'll see the following menu:
```
[bold cyan]Choose an option:[/bold cyan]
1️⃣ Search by username
2️⃣ Process input file
[cyan]Enter your choice (1-2)[/cyan]
```

- **Option 1 (Search by username)**: Enter a single username to search across 33 platforms.
- **Option 2 (Process input file)**: Provide a file with usernames (one per line) for batch processing.

After results are displayed, you can:
- Filter results by status (Found/Not Found) or platform.
- Export results to JSON or CSV.
- Choose to continue with another search or exit.

#### Command-Line Mode
Search for a single username directly:
```bash
python tracevibe.py --username exampleuser
```

Process a file with usernames:
```bash
python tracevibe.py --input-file usernames.txt
```

### Example File Format (usernames.txt)
Create a text file (`usernames.txt`) with one username per line:
```
exampleuser
testuser123
john_doe
```

### Example Output
#### Interactive Mode (Option 1)
```
[bold magenta]
___________                        ____   ____._____.           
\__    ___/___________    ____  ___\   \ /   /|__\_ |__   ____  
  |    |  \_  __ \__  \ _/ ___\/ __ \   Y   / |  || __ \_/ __ \ 
  |    |   |  | \// __ \\  \__\  ___/\     /  |  || \_\ \  ___/ 
  |____|   |__|  |____  /\___  >___  >\___/   |__||___  /\___  >
                      \/     \/    \/                 \/     \/ 

    [/bold magenta]
[bold cyan]Welcome to TraceVibe! 🔍[/bold cyan]
Trace usernames across platforms with ease.
Choose an option below to start!

[bold cyan]Choose an option:[/bold cyan]
1️⃣ Search by username
2️⃣ Process input file
[cyan]Enter your choice (1-2)[/cyan] 1
[cyan]Enter username (or press Enter to skip)[/cyan] exampleuser

[Spinner] Searching for username 'exampleuser'...

[bold blue]Username Search Results[/bold blue]
[yellow]Note: Results may require manual verification for accuracy.[/yellow]
┌────────────┬───────────────────────────────────────┬───────────┐
│ Platform   │ URL                                   │ Status    │
├────────────┼───────────────────────────────────────┼───────────┤
│ Twitter    │ https://twitter.com/exampleuser       │ Found     │
│ GitHub     │ https://github.com/exampleuser        │ Not Found │
│ Instagram  │ https://instagram.com/exampleuser     │ Found     │
...
└────────────┴───────────────────────────────────────┴───────────┘

[cyan]Filter profiles by status? (Found/Not Found/None)[/cyan] Found
[cyan]Filter profiles by platform? (e.g., Twitter, or press Enter for none)[/cyan]

[bold blue]Username Search Results[/bold blue]
[yellow]Note: Results may require manual verification for accuracy.[/yellow]
┌────────────┬───────────────────────────────────────┬───────────┐
│ Platform   │ URL                                   │ Status    │
├────────────┼───────────────────────────────────────┼───────────┤
│ Twitter    │ https://twitter.com/exampleuser       │ Found     │
│ Instagram  │ https://instagram.com/exampleuser     │ Found     │
...
└────────────┴───────────────────────────────────────┴───────────┘

[cyan]Export results? (yes/no)[/cyan] yes
[cyan]Export format (json/csv)[/cyan] json
[cyan]Enter output filename[/cyan] tracevibe_results.json
[green]Results exported to tracevibe_results.json (JSON)[/green]

[cyan]Continue with another search? (yes/no)[/cyan] no
[bold green]Thank you for using TraceVibe! Goodbye! 👋[/bold green]
```

#### Command-Line Mode
```bash
python tracevibe.py --username exampleuser
```
Output:
```
[bold blue]Username Search Results[/bold blue]
[yellow]Note: Results may require manual verification for accuracy.[/yellow]
┌────────────┬───────────────────────────────────────┬───────────┐
│ Platform   │ URL                                   │ Status    │
├────────────┼───────────────────────────────────────┼───────────┤
│ Twitter    │ https://twitter.com/exampleuser       │ Found     │
│ GitHub     │ https://github.com/exampleuser        │ Not Found │
...
└────────────┴───────────────────────────────────────┴───────────┘

[cyan]Filter profiles by status? (Found/Not Found/None)[/cyan] None
[cyan]Filter profiles by platform? (e.g., Twitter, or press Enter for none)[/cyan]

[cyan]Export results? (yes/no)[/cyan] no
[cyan]Continue with another search? (yes/no)[/cyan] no
[bold green]Thank you for using TraceVibe! Goodbye! 👋[/bold green]
```

## Supported Platforms
TraceVibe searches across the following 33 platforms:
- Twitter
- GitHub
- Instagram
- LinkedIn
- Reddit
- Facebook
- TikTok
- Snapchat
- Pinterest
- Tumblr
- Discord
- Telegram
- Medium
- Quora
- Vimeo
- SoundCloud
- Twitch
- Clubhouse
- Patreon
- Behance
- DeviantArt
- Flickr
- Meetup
- WeChat
- Viber
- Line
- KakaoTalk
- Dribbble
- GitLab
- Bitbucket
- Stack Overflow
- Fiverr
- Upwork
- Freelancer
- Kaggle
- CodePen
- Replit
- AngelList
- Crunchbase
- Etsy
- Goodreads
- Myspace
- Last.fm
- Steam
- Xbox
- PlayStation Network
- Spotify
- Strava
- Duolingo
- Wattpad
- Tripadvisor

**Note**: Some platforms (e.g., Discord, Stack Overflow, Strava) may require numeric IDs in URLs, so results should be manually verified.

## Limitations
- **Accuracy**: Results may vary due to platform-specific behavior, rate limiting, or changes in "not found" messages. Always verify "Found" results manually.
- **Rate Limiting**: The tool includes a 0.5-second delay between requests to minimize rate limits, but heavy use may still trigger restrictions.
- **Platform Coverage**: Some platforms may have complex URL patterns or require authentication, affecting detection reliability.
- **Local Execution**: The tool must be run locally, as it does not support web hosting.

## Contributing
We welcome contributions to improve TraceVibe! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code follows the project's style and includes appropriate documentation.

## License
TraceVibe is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For questions, suggestions, or issues, please open an issue on the GitHub repository or contact Technical Corp at [insert contact email or link].

Happy tracing with TraceVibe! 🔍
