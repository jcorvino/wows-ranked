# Description:
This project estimates the number of battles needed to get to rank 1 in World of Warships.

# Example Usage:
```bash
python wows-ranked.py -f 0.15 -m 3000 -s 20000 -o ./output
```

This will run the program with the following settings: 
* a first place rate of 0.20 (20% chance of getting first place in a battle),
* a maximum of 3,000 battles per simulation (to prevent infinite loops),
* 20,000 simulation runs for each win rate.
* a player win rate of 0.48 to 1.0 (48% to 100% chance of winning a battle),
* The plot will be saved as a file called "example.png"

Adding a `--sprint` flag will simulate a ranked sprint season instead of the regular ranked season.

Run `python wows-ranked.py -h` for the full help menu.

# Example Output:
The program will save a histogram for each win rate simulated. 
It will also save a summary plot of win rate vs median battles.

## Regular Season:
```bash
python wows-ranked.py -f 0.15 -m 3000 -s 20000 -o ./example-regular-season
```
### Example Summary Plot:
![Example summary plot][example-regular]
### Example Histogram:
![Example histogram][example-histogram]

## Sprint Season
```bash
python wows-ranked.py -f 0.15 -m 3000 -s 20000 --sprint -o ./example-sprint-season
```
### Example Summary Plot:
![Example summary plot][example-sprint]


# Requirements:
The project uses Python 3.8 and matplotlib. See [requirements.txt](https://github.com/jcorvino/wows-ranked/blob/master/requirements.txt) for details.

# Credits:
Original version by player Terror_Tost from the EU server.

[example-regular]: https://github.com/jcorvino/wows-ranked/raw/master/example-regular-season/wows-ranked-regular-summary-15fr.png "Example summary plot for regular ranked season"
[example-histogram]: https://github.com/jcorvino/wows-ranked/raw/master/example-regular-season/wows-ranked-regular-simulation-50wr-15fr.png "Example histogram for regular ranked season"
[example-sprint]: https://github.com/jcorvino/wows-ranked/raw/master/example-sprint-season/wows-ranked-sprint-summary-15fr.png "Example summary plot for ranked sprint season"