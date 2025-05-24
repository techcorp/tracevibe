import argparse
import json
import requests
import os
import sys
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
import pandas as pd
import time

console = Console()

def print_welcome():
    """Display the ASCII art banner and welcome message."""
    ascii_banner = r"""

    ___________                        ____   ____._____.           
    \__    ___/___________    ____  ___\   \ /   /|__\_ |__   ____  
      |    |  \_  __ \__  \ _/ ___\/ __ \   Y   / |  || __ \_/ __ \ 
      |    |   |  | \// __ \\  \__\  ___/\     /  |  || \_\ \  ___/ 
      |____|   |__|  (____  /\___  >___  >\___/   |__||___  /\___  >
                          \/     \/    \/                 \/     \/ 
                                                                
                                 Created By Technical Corp
    """
    console.print(Panel(
        f"[bold magenta]{ascii_banner}[/bold magenta]\n"
        "[bold cyan]Welcome to TraceVibe! 🔍[/bold cyan]\n"
        "Trace usernames across platforms with ease.\n"
        "Choose an option below to start!",
        title="Created by Technical Corp",
        border_style="blue"
    ))

def check_url(url, platform):
    """Check if a URL corresponds to an existing account with platform-specific validation."""
    try:
        for _ in range(2):  # Retry once if it fails
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                not_found_indicators = {
                    "Twitter": ["This account doesn’t exist", "Page not found"],
                    "GitHub": ["Page not found", "There isn’t a GitHub Pages site here"],
                    "Instagram": ["Sorry, this page isn't available", "User not found"],
                    "LinkedIn": ["Page not found", "We can't find that page"],
                    "Reddit": ["Page not found", "User does not exist"],
                    "Facebook": ["Page Not Found", "This content is not available"],
                    "TikTok": ["User does not exist", "Page not found"],
                    "Snapchat": ["Page not found", "Oops! We couldn’t find that page"],
                    "Pinterest": ["Page not found", "Looks like this page doesn’t exist"],
                    "Tumblr": ["There's nothing here", "Page not found"],
                    "Discord": ["Invite Invalid", "Unknown Invite"],
                    "Telegram": ["This chat does not exist", "Page not found"],
                    "Medium": ["Page not found", "This page doesn’t exist"],
                    "Quora": ["Page Not Found", "404"],
                    "Vimeo": ["Page not found", "Sorry, we can’t find that page"],
                    "SoundCloud": ["Page not found", "We can’t find that user"],
                    "Twitch": ["Page not found", "Sorry, unless you’ve got a time machine"],
                    "Clubhouse": ["User not found", "Page not found"],
                    "Patreon": ["Page not found", "This page doesn’t exist"],
                    "Behance": ["Page Not Found", "404"],
                    "DeviantArt": ["Page Not Found", "The page you’re looking for isn’t here"],
                    "Flickr": ["Page Not Found", "This member does not exist"],
                    "Meetup": ["Page Not Found", "This page does not exist"],
                    "WeChat": ["User not found", "Page not found"],
                    "Viber": ["User not found", "Page not found"],
                    "Line": ["User not found", "Page not found"],
                    "KakaoTalk": ["User not found", "Page not found"],
                    "Dribbble": ["Page Not Found", "404"],
                    "GitLab": ["Page not found", "404"],
                    "Bitbucket": ["Repository not found", "Page not found"],
                    "Stack Overflow": ["Page Not Found", "This user does not exist"],
                    "Fiverr": ["Page Not Found", "404"],
                    "Upwork": ["Page Not Found", "We couldn’t find that page"],
                    "Freelancer": ["Page Not Found", "404"],
                    "Kaggle": ["Page Not Found", "404"],
                    "CodePen": ["Pen Not Found", "Page not found"],
                    "Replit": ["Not Found", "404"],
                    "AngelList": ["Page Not Found", "404"],
                    "Crunchbase": ["Page Not Found", "404"],
                    "Etsy": ["Shop not found", "Page not found"],
                    "Goodreads": ["Page Not Found", "404"],
                    "Myspace": ["Page Not Found", "404"],
                    "Last.fm": ["User not found", "Page not found"],
                    "Steam": ["The specified profile could not be found", "404"],
                    "Xbox": ["Gamer not found", "Page not found"],
                    "PlayStation Network": ["User not found", "Page not found"],
                    "Spotify": ["Page not found", "404"],
                    "Strava": ["Athlete not found", "Page not found"],
                    "Duolingo": ["User not found", "Page not found"],
                    "Wattpad": ["User not found", "Page not found"],
                    "Tripadvisor": ["Page not found", "404"]
                }
                if any(indicator in response.text for indicator in not_found_indicators.get(platform, [])):
                    return False
                return True
            elif response.status_code == 404:
                return False
            time.sleep(1)  # Wait before retry
        return False
    except requests.RequestException:
        return False

def load_cache(cache_file="tracevibe_cache.json"):
    """Load cached results."""
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return {"profiles": {}}

def save_cache(cache, cache_file="tracevibe_cache.json"):
    """Save results to cache."""
    with open(cache_file, "w") as f:
        json.dump(cache, f, indent=2)

def search_username(username, progress, cache):
    """Search for social media profiles by username."""
    if username in cache["profiles"]:
        console.print(f"[yellow]Using cached results for username '{username}'[/yellow]")
        return cache["profiles"][username]

    platforms = [
        {"name": "Twitter", "url": f"https://twitter.com/{username}"},
        {"name": "GitHub", "url": f"https://github.com/{username}"},
        {"name": "Instagram", "url": f"https://instagram.com/{username}"},
        {"name": "LinkedIn", "url": f"https://linkedin.com/in/{username}"},
        {"name": "Reddit", "url": f"https://www.reddit.com/user/{username}"},
        {"name": "Facebook", "url": f"https://www.facebook.com/{username}"},
        {"name": "TikTok", "url": f"https://www.tiktok.com/@{username}"},
        {"name": "Snapchat", "url": f"https://www.snapchat.com/add/{username}"},
        {"name": "Pinterest", "url": f"https://www.pinterest.com/{username}"},
        {"name": "Tumblr", "url": f"https://{username}.tumblr.com"},
        {"name": "Discord", "url": f"https://discord.com/users/{username}"},  # Note: Requires user ID, but testing for username
        {"name": "Telegram", "url": f"https://t.me/{username}"},
        {"name": "Medium", "url": f"https://medium.com/@{username}"},
        {"name": "Quora", "url": f"https://www.quora.com/profile/{username}"},
        {"name": "Vimeo", "url": f"https://vimeo.com/{username}"},
        {"name": "SoundCloud", "url": f"https://soundcloud.com/{username}"},
        {"name": "Twitch", "url": f"https://www.twitch.tv/{username}"},
        {"name": "Clubhouse", "url": f"https://www.clubhouse.com/@{username}"},
        {"name": "Patreon", "url": f"https://www.patreon.com/{username}"},
        {"name": "Behance", "url": f"https://www.behance.net/{username}"},
        {"name": "DeviantArt", "url": f"https://{username}.deviantart.com"},
        {"name": "Flickr", "url": f"https://www.flickr.com/people/{username}"},
        {"name": "Meetup", "url": f"https://www.meetup.com/members/{username}"},  # Note: May require numeric ID
        {"name": "WeChat", "url": f"https://www.wechat.com/en/user/{username}"},  # Note: WeChat URLs may vary
        {"name": "Viber", "url": f"https://viber.com/{username}"},  # Note: Viber URLs may vary
        {"name": "Line", "url": f"https://line.me/ti/p/~{username}"},
        {"name": "KakaoTalk", "url": f"https://www.kakaotalk.com/{username}"},  # Note: KakaoTalk URLs may vary
        {"name": "Dribbble", "url": f"https://dribbble.com/{username}"},
        {"name": "GitLab", "url": f"https://gitlab.com/{username}"},
        {"name": "Bitbucket", "url": f"https://bitbucket.org/{username}"},
        {"name": "Stack Overflow", "url": f"https://stackoverflow.com/users/{username}"},  # Note: May require numeric ID
        {"name": "Fiverr", "url": f"https://www.fiverr.com/{username}"},
        {"name": "Upwork", "url": f"https://www.upwork.com/freelancers/~{username}"},  # Note: Upwork URLs may vary
        {"name": "Freelancer", "url": f"https://www.freelancer.com/u/{username}"},
        {"name": "Kaggle", "url": f"https://www.kaggle.com/{username}"},
        {"name": "CodePen", "url": f"https://codepen.io/{username}"},
        {"name": "Replit", "url": f"https://replit.com/@{username}"},
        {"name": "AngelList", "url": f"https://angel.co/{username}"},
        {"name": "Crunchbase", "url": f"https://www.crunchbase.com/person/{username}"},
        {"name": "Etsy", "url": f"https://www.etsy.com/shop/{username}"},
        {"name": "Goodreads", "url": f"https://www.goodreads.com/user/show/{username}"},  # Note: May require numeric ID
        {"name": "Myspace", "url": f"https://myspace.com/{username}"},
        {"name": "Last.fm", "url": f"https://www.last.fm/user/{username}"},
        {"name": "Steam", "url": f"https://steamcommunity.com/id/{username}"},
        {"name": "Xbox", "url": f"https://xboxgamertag.com/search/{username}"},
        {"name": "PlayStation Network", "url": f"https://psnprofiles.com/{username}"},
        {"name": "Spotify", "url": f"https://open.spotify.com/user/{username}"},
        {"name": "Strava", "url": f"https://www.strava.com/athletes/{username}"},  # Note: May require numeric ID
        {"name": "Duolingo", "url": f"https://www.duolingo.com/profile/{username}"},
        {"name": "Wattpad", "url": f"https://www.wattpad.com/user/{username}"},
        {"name": "Tripadvisor", "url": f"https://www.tripadvisor.com/members/{username}"}
    ]
    results = []
    task = progress.add_task(f"[cyan]Searching for username '{username}'...", total=len(platforms))
    for platform in platforms:
        status = "Found" if check_url(platform["url"], platform["name"]) else "Not Found"
        results.append({"platform": platform["name"], "url": platform["url"], "status": status})
        progress.update(task, advance=1)
        time.sleep(0.5)  # Delay to avoid rate limiting
    cache["profiles"][username] = results
    return results

def display_results(profiles, filter_status=None, filter_platform=None):
    """Display results in a styled table with accuracy warning."""
    if profiles:
        console.print("\n[bold blue]Username Search Results[/bold blue]")
        console.print("[yellow]Note: Results may require manual verification for accuracy.[/yellow]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Platform", style="cyan")
        table.add_column("URL", style="green")
        table.add_column("Status", style="yellow")
        for profile in profiles:
            if filter_status and profile["status"] != filter_status:
                continue
            if filter_platform and profile["platform"].lower() != filter_platform.lower():
                continue
            status_style = "green" if profile["status"] == "Found" else "red"
            table.add_row(profile["platform"], profile["url"], f"[{status_style}]{profile['status']}[/{status_style}]")
        console.print(table)
    else:
        console.print("[yellow]No profile results to display.[/yellow]")

def export_results(profiles, filename, format="json"):
    """Export results to JSON or CSV."""
    results = {"profiles": profiles}
    if format == "json":
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        console.print(f"[green]Results exported to {filename} (JSON)[/green]")
    elif format == "csv":
        profile_df = pd.DataFrame(profiles) if profiles else pd.DataFrame(columns=["platform", "url", "status"])
        profile_df.to_csv(f"profiles_{filename}", index=False)
        console.print(f"[green]Results exported to profiles_{filename} (CSV)[/green]")

def read_input_file(file_path):
    """Read usernames from a file."""
    if not os.path.exists(file_path):
        console.print(f"[red]Error: File '{file_path}' not found.[/red]")
        return []
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    while True:
        parser = argparse.ArgumentParser(description="TraceVibe: OSINT Tool for username search")
        parser.add_argument("--username", help="Username to search for")
        parser.add_argument("--input-file", help="File with usernames (one per line)")
        args = parser.parse_args()

        print_welcome()
        cache = load_cache()

        # Interactive menu
        console.print("\n[bold cyan]Choose an option:[/bold cyan]")
        console.print("1️⃣ Search by username")
        console.print("2️⃣ Process input file")
        choice = IntPrompt.ask("[cyan]Enter your choice (1-2)[/cyan]", choices=["1", "2"], default=1)

        usernames = []
        if args.input_file and choice != 2:
            console.print("[yellow]Ignoring --input-file since interactive mode is selected.[/yellow]")

        if choice == 1:
            if args.username:
                usernames = [args.username]
            else:
                username = Prompt.ask("[cyan]Enter username (or press Enter to skip)[/cyan]", default="")
                if username:
                    usernames = [username]
        elif choice == 2:
            file_path = args.input_file or Prompt.ask("[cyan]Enter path to input file[/cyan]")
            usernames = read_input_file(file_path)

        if not usernames:
            console.print("[red]Error: Please provide at least a username or input file.[/red]")
            sys.exit(1)

        # Perform searches
        all_profiles = []
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            for username in usernames:
                profiles = search_username(username, progress, cache)
                all_profiles.extend(profiles)

        # Save cache
        save_cache(cache)

        # Filter results
        filter_status = Prompt.ask(
            "[cyan]Filter profiles by status? (Found/Not Found/None)[/cyan]",
            choices=["Found", "Not Found", "None"], default="None"
        )
        filter_platform = Prompt.ask(
            "[cyan]Filter profiles by platform? (e.g., Twitter, or press Enter for none)[/cyan]",
            default=""
        )
        filter_status = filter_status if filter_status != "None" else None
        filter_platform = filter_platform if filter_platform else None

        # Display results
        display_results(all_profiles, filter_status, filter_platform)

        # Export results
        if all_profiles:
            export = Prompt.ask("[cyan]Export results? (yes/no)[/cyan]", choices=["yes", "no"], default="no")
            if export == "yes":
                format = Prompt.ask("[cyan]Export format (json/csv)[/cyan]", choices=["json", "csv"], default="json")
                filename = Prompt.ask("[cyan]Enter output filename[/cyan]", default=f"tracevibe_results.{format}")
                export_results(all_profiles, filename, format)

        # Exit or continue prompt
        continue_exit = Prompt.ask("[cyan]Continue with another search? (yes/no)[/cyan]", choices=["yes", "no"], default="no")
        if continue_exit.lower() != "yes":
            console.print("[bold green]Thank you for using TraceVibe! Goodbye! 👋[/bold green]")
            break

if __name__ == "__main__":
    main()