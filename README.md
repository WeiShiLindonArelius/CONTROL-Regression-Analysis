How do I play CONTROL?
- Open the Codespace miniature zebra
- Open the file **control_main_true.py**
- Click the three lines in the top left
- Click run without debugging
- Watch it unfold in front of you!
- Useful documents to look at for stats and more: history, region_mvp, best_stats, my_teams, and playerstats.

What is CONTROL?
- CONTROL is a game fundamentally based on random number generation (RNG). Teams have 6 players, each with the following statistics: Power, Attack Damage, Attack Speed, Critical Chance, Critical Multiplier, Max Health, and Spawn Time.
- Individual games are played between lineups of 4 players. Each team has 8 main lineups, the 8 best unique 4-man lineups from their roster, plus a 9th for tiebreaker situtations.
- The process of an individual game is invisible, but here is roughly how it goes.
  - Each team is randomly assigned "+" or "-" which determines their impact on the TESSERACT.
  - Games take 104 "ticks", each tick goes through every living player and does a number of things
  - The TESSERACT, the value around which the result of the game is determined, is adjusted by the player's Power. Positive for the + team, Negative for the - team.
  - If the tick is a multiple of the player's attack speed, they attack a random enemy player, decreasing their health by an amount equal to their attack damage. There is also a chance, based on their critical chance, for a critical hit.
  - If the player dies, an amount equal to 3x the excess damage is applied to the TESSERACT. This is called "Overkill" and is tracked in stats.
  - All players which are not alive have their countdown incremented by one; once it hits a value equal to their "Spawn Time" statistic, they respawn.
- In the regular season, matches consist of only the first 8 of a team's lineup playing one another, and if it ends 4-4, it's a draw. Regular season standings are based on the number of **games** you win, not the number of **matches** you win.
- In the playoffs, if it is 4-4 after the first 8 games, a tiebreaker is played with the same lineup as the first game, meaning both teams' best players. Playoff series go up to a certain number of **matches** with a certain margin of victory. (This margin can decrease for absurdly long series)
