# Anki Rapid Fire

Add-on for Anki 2.1

** This is NOT working currently! **

The goal of this project is the help you learn unordered flashcards faster.

Imagine you have a deck of 500 vocabulary words. Some of them will be easier than
others to memorize. Let's say your minimum interval is 1 minute. You will end up
cycling through 1 minute worth of your hardest words as you learn the easy ones, leaving
only hard words in your learning queue. To
fix this problem, this addon moves "learning" cards to the bottom
of the new card queue if you miss them 5 times in a row. That way you will blaze
through all the easy cards and you won't be looking at hard cards for the entire
study period.

Currently, this also does not
change the experimental scheduler. 

**Warning: This will  reset the data on your _lapsed_ cards as well
if you keep missing them, which you may not want.**

## TODO

- Make this a per-deck option
- Make the number of misses required to trigger a reset customizable.
- Add option to disable tooltip.

