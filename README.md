# The Internet Oracle RSS Builder

I've been a fan of the [Internet Oracle](https://internetoracle.org) for a long time. I even 
used to be a regular contributor... several decades ago. It's one of the early, _early_ bits of 
internet culture that somehow has still managed to survive to this day. It's also a unique 
experience that I can't describe, but poke around enough on the website and you'll find as much 
lore as you need.

Anyway, they've got a Web 0.7 website that still uses CGI scripts, for Pete's sake. There's a 
mailing list you can subscribe to if you want to receive updates that way, but some of us are 
stuck in the Web 1.5 days and we use RSS.  

## Installation

1. Install [pyenv](https://github.com/pyenv/pyenv), if you don't already have it, and run `pyenv 
install 3.12`. 
2. Install [pipenv](https://pipenv.pypa.io/en/latest/), if you don't already have it.
3. `cd internet-oracle-rss`
4. `pipenv install`
5. `pipenv run python3 script.py`

That should generate a file `internet-oracle.rss` in the current working directory.