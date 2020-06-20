# Description:
This project estimates the number of battles needed to get to rank 1 in World of Warships.

# Example Usage:
```bash
python wows-ranked.py -w 0.55 -f 0.20 -m 3000 -s 20000 -o example.png
```

This will run the program with the following settings:
* a player win rate of 0.55 (55% chance of winning a battle), 
* a first place rate of 0.20 (20% chance of getting first place in a battle),
* a maximum of 3,000 battles per simulation (to prevent infinite loops),
* and 10,000 simulation runs.
* The plot will be saved as a file called "example.png"

Adding a `--sprint` flag will simulate a ranked sprint season instead of the regular ranked season.

Run `python wows-ranked.py -h` for the full help menu.

# Example Output:
```bash
python wows-ranked.py -w 0.55 -f 0.20 -m 3000 -s 20000 -o .\images\example-regular.png
```
![Example histogram][example-regular]

```bash
python wows-ranked.py -w 0.55 -f 0.20 -m 3000 -s 20000 --sprint -o .\images\example-sprint.png
```
![Example histogram][example-sprint]


# Requirements:
The project uses Python 3.8 and matplotlib. See [requirements.txt](https://github.com/jcorvino/wows-ranked/blob/master/requirements.txt) for details.

# Credits:
Original version by player Terror_Tost from the EU server.


[example-regular]: https://github.com/jcorvino/wows-ranked/raw/master/images/example-regular.png "Example histogram for regular ranked season"
[example-sprint]: https://github.com/jcorvino/wows-ranked/raw/master/images/example-sprint.png "Example histogram for ranked sprint season"