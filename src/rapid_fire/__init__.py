# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showText, tooltip
import heapq
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


# for debugging
def printQueue(scheduler):
    for i in range(len(scheduler._lrnQueue)):
        print(str(i) + ": " + str(scheduler._lrnQueue[i]))


# algo for removing arbitrarily from a heap stolen from stackoverflow
def removeFromLrnQueue(scheduler, card):
    #print("Removing card: %d", card.id)
    #print("Before removal:")
    printQueue(scheduler)
    for i in range(len(scheduler._lrnQueue)):
        if scheduler._lrnQueue[i][1] == card.id:
            scheduler._lrnQueue[i] = scheduler._lrnQueue[-1]
            scheduler._lrnQueue.pop()
            heapq.heapify(scheduler._lrnQueue)
            break
    #print("After removal:")
    #printQueue(scheduler)
    


def revisedAnswerCard(self, card, ease):
    tolerance = 10 # number of times you are allowed to get it wrong
    oldAnswerCard(self, card, ease)
    entries = self.col.db.all(
            "select ease, type, ivl, lastIvl from revlog where cid = ?", card.id)
    misses = missCount(entries)
    # if 5, 10, 15, etc misses in a row
    # if the reset new card comes up again, and we miss it again, we are then at 6 in a row
    # we don't want to get reset immediately in that case, but rather wait til we miss it 10 times, etc
    if misses % tolerance == 0 and misses > 0:
        #tooltip("To the back of the bus! Miss #" + str(misses), period=1500)
        # reset the card
        self.forgetCards([card.id])
        # even though we have rescheduled the card, its id is still in
        # the learn queue which will cause it to be brought up before we want it
        removeFromLrnQueue(self, card) 
        # fix our queue counts
        self.newCount += 1
        self.lrnCount -= card.left // 1000 



# patch it
oldAnswerCard = sched.Scheduler.answerCard
sched.Scheduler.answerCard = revisedAnswerCard



