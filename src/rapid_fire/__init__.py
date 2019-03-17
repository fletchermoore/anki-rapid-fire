# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showText, tooltip

import anki.sched as sched

# takes a card revlog containing only [(ease,), ...]
# returns number of times ease 1 was selected in a row
# ie, number of consecutive times you said you didn't know the answer
def missCount(log):
    missCount = 0
    index = len(log) - 1
    while index > -1:
        ease = log[index][0]
        if ease == 1:
            missCount += 1
        else:
            break
        index = index - 1
    return missCount



oldAnswerCard = sched.Scheduler.answerCard

def revisedAnswerCard(self, card, ease):
    oldAnswerCard(self, card, ease)
    entries = self.col.db.all(
            "select ease from revlog where cid = ?", card.id)
    misses = missCount(entries)
    if misses > 5:
        tooltip("To the back of the bus!")
        self.forgetCards([card.id])
        self.sortCards([card.id]) # set due to 1 (back of the bus!)
        self.newCount += 1
    #showText(str(entries) + " " + str(misses))

sched.Scheduler.answerCard = revisedAnswerCard



