# Monday 23 November 2026 — The World in One Image

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/fckkrel/news-image-23nov-fckkrel/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/fckkrel/news-image-23nov-fckkrel/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up the world's news of [Monday 23 November 2026](https://make.fun/bounty/news-image-20261123), for make.fun's "Sum up 23 November's world news in one image" bounty.

The front page carries 34 stories across 7 regions, every one dated to that single day. The lead is Ukraine saying its sea drones sank the Russian corvette Merkury off Libya. Under it sit seven colour-coded sections: Europe, Middle East, Asia-Pacific, Africa, North America, Latin America, and a markets, science and sport column — from NATO's emergency meeting on the Russian missiles that fell in Poland and the COP31 blame game, to the Cikande factory fire toll in Indonesia, drones killing five children in Khartoum, the Democrats' 258-seat House majority, and Marc Márquez winning his eighth MotoGP title.

`build_entry.py` draws the page with Pillow (1024×1024, bold headlines sized to stay readable when the image is shrunk) and saves it as `entry.png`. `main.ts` checks that file is a PNG within the bounty's limits and writes it to `/output/entry.png`. No network, no clock, no randomness: Node 22 standard library only, and both runs write the same bytes.
