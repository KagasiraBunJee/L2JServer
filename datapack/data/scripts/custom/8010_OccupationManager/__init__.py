import sys
from com.l2jfrozen.gameserver.model.actor.instance import L2PcInstance
from com.l2jfrozen.gameserver.model.actor.instance import L2NpcInstance
from java.util import Iterator
from com.l2jfrozen.util.database import L2DatabaseFactory
from com.l2jfrozen.gameserver.model.quest import State
from com.l2jfrozen.gameserver.model.quest import QuestState
from com.l2jfrozen.gameserver.model.quest.jython import QuestJython as JQuest
from com.l2jfrozen.gameserver.model.base import Race

qn = "6667_OccupationManager"

NPC=70000
NPC_NAME="Kain"
QuestId     = 6667
QuestName   = "OccupationManager"
QuestDesc   = "custom"

REQUEST_ITEM_ID = 57 #adena
REQUEST_ITEM_NAME = "Adena"
OCCUPATIONS_PRICE = {
    1: 100000,
    2: 1000000,
    3: 20000000
}
OCCUPATIONS_LVL_REQ = {
    1: 20,
    2: 40,
    3: 76
}

RACE_NAMES = {
    Race.human: "human",
    Race.elf: "elf",
    Race.darkelf: "dark elf",
    Race.dwarf: "dwarf",
    Race.orc: "orc"
}

CLASS_NAMES = {
    0: "Human Fighter",
    1: "Human Warrior",
    2: "Gladiator",
    3: "Warlord",
    4: "Human Knight",
    5: "Paladin",
    6: "Dark Avenger",
    7: "Rogue",
    8: "Treasure Hunter",
    9: "Hawkeye",
    10: "Human Mage",
    11: "Human Wizard",
    12: "Sorcerer",
    13: "Necromancer",
    14: "Warlock",
    15: "Cleric",
    16: "Bishop",
    17: "Prophet",
    88: "Duelist",
    89: "Dread Nought",
    90: "Phoenix Knight",
    91: "Hell Knight",
    92: "Sagittarius",
    93: "Adventurer",
    94: "Archmage",
    95: "Soul Taker",
    96: "Arcane Lord",
    97: "Cardinal",
    98: "Hierophant",
    18: "Elven Fighter",
    19: "Elven Knight",
    20: "Temple Knight",
    21: "Swordsinger",
    22: "Elven Scout",
    23: "Plainswalker",
    24: "Silver Ranger",
    25: "Elven Mage",
    26: "Elven Wizard",
    27: "Spellsinger",
    28: "Elemental Summoner",
    29: "Elven Oracle",
    30: "Elven Elder",
    99: "Evas Templar",
    100: "Sword Muse",
    101: "Wind Rider",
    102: "Moonlight Sentinel",
    103: "Mystic Muse",
    104: "Elemental Master",
    105: "Evas Saint",
    31: "Dark Elven Fighter",
    32: "Pallus Knight",
    33: "Shillien Knight",
    34: "Bladedancer",
    35: "Assasin",
    36: "Abyss Walker",
    37: "Phantom Ranger",
    38: "Dark Elven Mage",
    39: "Dark Wizard",
    40: "Spellhowler",
    41: "Phantom Summoner",
    42: "Shillien Oracle",
    43: "Shillien Elder",
    106: "Shillien Templar",
    107: "Spectral Dancer",
    108: "Ghost Hunter",
    109: "Ghost Sentinel",
    110: "Storm Screamer",
    111: "Spectral Master",
    112: "Shillien Saint",
    44: "Orc Fighter",
    45: "Orc Raider",
    46: "Destroyer",
    47: "Monk",
    48: "Tyrant",
    49: "Orc Mage",
    50: "Orc Shaman",
    51: "Overlord",
    52: "Warcryer",
    113: "Titan",
    114: "Grand Khauatari",
    115: "Dominator",
    116: "Doomcryer",
    53: "Dwarven Fighter",
    54: "Scavenger",
    55: "Bounty Hunter",
    56: "Artisan",
    57: "Warsmith",
    117: "Fortune Seeker",
    118: "Maestro"
}

CLASSES = {
    # Humans
    # First
    0: [1, 4, 7], # Fighter
    10: [11, 15], # Mage

    # Second
    #Fighter
    1: [2, 3],
    4: [5, 6],
    7: [8, 9],
    #Mage
    11: [12, 13, 14],
    15: [16, 17],

    # Third
    #Fighter
    2: [88],
    3: [89],
    5: [90],
    6: [91],
    8: [93],
    9: [92],
    #Mage
    12: [94],
    13: [95],
    14: [96],
    16: [97],
    17: [98],
    #------------------------

    # First elves
    18: [19, 22], # Fighter
    25: [26, 29], # Mage

    #Second
    #Fighter
    19: [20, 21],
    22: [23, 24],
    #Mage
    26: [27, 28],
    29: [30],

    # Third
    #Fighter
    20: [99],
    21: [100],
    23: [101],
    24: [102],
    #Mage
    27: [103],
    28: [104],
    30: [105],
    #------------------------

    # First dark elves
    31: [32, 35], # Fighter
    38: [39, 42], # Mage'
    #------------------------

    # First orcs
    44: [45, 47], # Fighter
    49: [50], # Mage
    #------------------------

    # First dwarves
    53: [54, 56]
}

print "INFO  OccupationManager ("+str(NPC)+") Enabled..."

def invalid_request():
    return "You are not ready"

def valid_player(player):
    reason = ""
    # Level requirement
    curr_lvl = player.getLevel()
    occ_lvl = player.getClassId().level() + 1
    req_lvl = OCCUPATIONS_LVL_REQ.get(occ_lvl)
    valid_lvl = curr_lvl >= req_lvl

    #items
    itemCount = player.getQuestState(qn).getQuestItemsCount(REQUEST_ITEM_ID)
    valid_items = itemCount >= OCCUPATIONS_PRICE.get(occ_lvl)
    if not valid_lvl:
        reason = "You must have "+str(req_lvl)+" level or higher"
    elif not valid_items:
        reason = "You must have more than "+str(OCCUPATIONS_PRICE[occ_lvl])+" "+REQUEST_ITEM_NAME
    elif occ_lvl >= 3:
        reason = "You have finished your training"
    valid = valid_lvl and valid_items and occ_lvl < 3
    return [valid, reason]


def main_dialog(player):
    race = player.getRace()
    player_class = player.getClassId()
    class_id = player_class.getId()
    race_name = RACE_NAMES.get(race)
    html = "<html><body>"
    html += "<center>Adventurer's Guide</center>"
    available_classes = CLASSES[class_id]
    isValidPlayer, reason = valid_player(player)

    html += "<br>Hello "+race_name+" traveler, I am "+NPC_NAME+", i will be your guide through your training and ascending<br>"

    if len(available_classes) > 0:
        if isValidPlayer:
            html += "<font color=00FF00>Now, you can become:</font><br>"
        elif not isValidPlayer:
            html += "<font color=FF0000>You cannot ascend your occupation. Reason: "+reason+"</font><br>"
            html += "<font color=FFFF00>But when you will be ready, you can become:</font><br>"
        for i in available_classes:
            class_name = CLASS_NAMES.get(i, "None")
            if class_name != "None":
                if isValidPlayer:
                    action = "bypass -h Quest "+qn+" "+str(i)+""
                    html += "<font><a action=\""+action+"\">"+ class_name +"</a></font>"
                else:
                    html += "<font>["+ class_name +"]</font>"
                html += "<br>"
    else:
        html += invalid_request()
    html += "</body></html>"
    return html

class Quest (JQuest) :

    def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

    def onAdvEvent (self,event,npc,player):
        isValidPlayer, reason = valid_player(player)
        if not isValidPlayer:
            return "<html><body>Cool down son. You are not ready.<br>"+reason+"</body></html>"
        st = player.getQuestState(qn)
        occ_lvl = player.getClassId().level() + 1
        st.takeItems(REQUEST_ITEM_ID, OCCUPATIONS_PRICE.get(occ_lvl))
        st.playSound("ItemSound.quest_fanfare_2")

        player.setClassId(int(event))
        player.setBaseClass(int(event))
        player.broadcastUserInfo()

    def onFirstTalk (self,npc,player):
        st = player.getQuestState(qn)
        if not st : st = self.newQuestState(player)
        return main_dialog(player)

QUEST = Quest(-1,qn,"custom")
CREATED     = State('Start', QUEST)
STARTED     = State('Started', QUEST)

QUEST.setInitialState(CREATED)
QUEST.addStartNpc(NPC)
QUEST.addFirstTalkId(NPC)
QUEST.addTalkId(NPC)