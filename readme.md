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

Run `python wows-ranked.py -h` for the full help menu.

# Example Output:
![Example histogram][example]


# Requirements:
The project uses Python 3.8 and matplotlib. See [requirements.txt](https://github.com/jcorvino/wows-ranked/blob/master/requirements.txt) for details.

# Credits:
Original version by player Terror_Tost from the EU server.


[example]: https://github.com/jcorvino/wows-ranked/raw/master/images/example.png "Example histogram"