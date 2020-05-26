# Description:
This project estimates the number of battles needed to get to rank 1 in World of Warships.

# Example Usage:
python wows-ranked.py -w 0.5 -f 0.15 -m 1000 -s 5000

This will run the program with a player win rate of 0.5 (50% chance of winning a battle), 
a first place rate of 0.15 (15% chance of getting first place in a battle),
a maximum of 1,000 battles per simulation (to prevent infinite loops),
and 5,000 simulation runs.

# Example Output:
![Example histogram][example]


# Credits:
Original version by player Terror_Tost from the EU server.


[example]: https://github.com/jcorvino/wows-ranked/raw/master/images/example.png "Example histogram"