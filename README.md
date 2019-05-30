# Official Discord Bot for Intralism

## Available Commands
- [User cooldown: 30s] rank
> Shows your current ranking (e.g. Global Ranking, Country Ranking) and statistics (e.g. Average Misses, Average Accuracy)
> Note that this command can only be used when you're linked to an Account
- [User cooldown: 30s] rank \<steamID> or \<steam URL> or \<custom URL>
> Shows the current ranking of the user with specified Steam ID / URL.
- [Global cooldown: 1m] top10, top
> Displays the current top tier players in Intralism, displayed as an Image in a Table.
- [User Cooldown 30s] link \<steamID> or \<team URL> or \<custom URL>
> Links your Account to the specified Steam ID / URL.
> If you mistakenly entered another URL / ID, you can redo this process.

## F.A.Q
- My Account Information is not up to date! Why?
    - This happens due to Intralism updating their Website slower than you made this request.
    - We suggest to wait for some minutes and retry

- My Information isn't displayed at all or is displayed partly!
    - This might be due to you linking a wrong ID / Steam URL (Valid, but non-existant)
    - If not please, tell us what ID you've picked and we'll reproduce and fix it!
    
## For Developers
### Fetching Player Data
Player Data and Top10 is fetched from `rank_scraper`, using `https://intralism.khb-soft.ru/?player={playerID}` as link.

Thanks @github/mishka for helping with scraping Data.

We have decided to scrape Data due to `?GetRanks` being horribly slow and `?GetServerData` even slower.

### Using Cogs
I'm using Discord Cogs to split everything up.

Handling Database related things goes to `userdata`

Handling Administrative things, such as disabling cogs, enabling or reinitializing cogs goes to `admin`

Handling Rank Commands such as top10 goes to `ranking`

This is to organize the code into collections of commands and listeners and handle things faster.

>There comes a time in the bot development when you want to extend the bot functionality at run-time and quickly unload and reload code (also called hot-reloading). The command framework comes with this ability built-in, with a concept called extensions.

[More Information over here](https://discordpy.readthedocs.io/en/latest/ext/commands/extensions.html#ext-commands-extensions)

## Special thanks to
@github/mishka for introducing me into Python and helping me at Data collection from Websites

@github/incetarik for prettifying a lot of the Code.
