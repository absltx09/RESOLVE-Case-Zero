import textwrap

W = 72
def p(s=""):
    for ln in textwrap.wrap(s, W) or [""]: print(ln)
def say(who, s): p(f"{who:<6} {s}")
def rule(c="="): p(c * W)
def bar(n, size=10): return "#" * (n * size // 100) + "." * (size - n * size // 100)
def hud():
    p(f"[ RESONANCE {bar(res)} {res:03d}% BODY {bar(body*100//12, 6)} NERVE {bar((10-nerve)*100//10, 5)} FRAME {frame}]")
def ask(q, opts):
    p(); q and p(q)
    for i, o in enumerate(opts, 1): p(f"  {i}. {o}")
    while True:
        try: n = int(input("> "))
        except ValueError: continue
        if 1 <= n <= len(opts): return n - 1
def wait(): input("[enter]")

# state
res, body, nerve, frame, gear = 0, 12, 0, 2, 2
read, seen, fired = set(), -1, set()
def up(n):
    global res; res = max(0, min(100, res + n))

BURN = ["", "Fingertips hot.", 
        "Static on your tongue.", 
        "A burning smell. Coming from you.", 
        "You can't feel what you're touching.", 
        "", "Hand shakes.", 
        "Left hand won't answer.", 
        "Ringing. Something says your name. You don't know what.", "", ""]

def burn(n):
    global nerve
    nerve = max(0, min(10, nerve + n))
    if BURN[nerve]: p("  > " + BURN[nerve])
    if nerve >= 10: raise SystemExit(lost())

# the house
OBJ = {
    "coat": ("The coat on the hanger by the door", 
    "A wool coat, brushed often. It has not been worn in "
    "nineteen years. It is the cleanest thing in the house.",
    ("PHIL", '"That\'s a lot of care put into one coat. Whoever it belongs to must have been gone for a while."')),
    "table": ("The dinner table", "Five seats. Only four people live here. The fifth is in the middle, where "
    "the life of the party would be. The plate is warm.", 
    ("ALLEN", '"Man, I could go for some dinner." \nYou just ate.')),
    "calendar": ("The calendars in the kitchen", 
    "Nineteen on one nail, every year turned to the same month. Someone "
    "circled the same date each time and wrote nothing next to it.",
    ("PHIL", '"Nineteen times. Leo and the file said recent.')),
    "hall": ("The hallway floor",
    "The boards are worn in a track to the front door and back. Thousands "
    "of times. Like someone was expecting something.",
    ("", "Allen is digging through kitchen drawers. Phil is trying to stop him.")),
    "photo": ("The framed photo on the stairs",
    "Four people and a gap, the way you leave a seat for someone. The "
    "print has been redone. The gap is wider than it was.",
    ("", "Allen looks at the photo a long time and says nothing. That\'s new.")),
}
COST, NEED, GATES = 18, 3, (50, 80)

WARM = ["",
 "The house is not cold. You\'d expected it to be cold.",
 "Someone has left the good lamp on for you. You start to think "
 "that staying wouldn\'t be too bad.",
 "We are doing well. The house is very good and there is no reason to "
 "go. In the window over the sink, you see the room behind you and a "
 "man in an old suit, smiling. You turn. The house is very good."]

def beat():
    global seen
    t = min(3, (res + 5) // 25)
    if t > seen:
        seen = t
        if WARM[t]: 
            if nerve >= 4: 
                p(); p("WARM: ???")
            else: p(); p(WARM[t])
        if t == 3: say("ALLEN", '"Adron. Who are you smiling at."')       

# combat
# enemies are (name, hold, moves). Each move: (tell, damage)
CLOCKS = ("THE MINUTE", 6, [
 ("Every clock in the house turns its face toward you.", 2),
 ("The minute repeats. You are standing where you were.", 1),
 ("A cuckoo comes out of the wall and won\'t stop.", 3)])
WAITING = ("THE WAITING", 14, [
 ("The hallway lengthens. The door is getting further away.", 1),
 ("The coat comes off the hook and grabs you.", 3),
 ("Five chairs scrape across the floor at once.", 2),
 ("The good lamp turns to face you. You\'re almost blinded.", 2),
 ("Upstairs, a door opens. Something is coming down to wait with you.", 4)])

GEAR = ["the strobe (blinds it for a beat)", "the jammer (static. it flinches)"]

def fight(foe):
    global body, nerve, frame, gear
    name, hold, moves = foe
    turn, primed = 0, False
    rule("-"); p(f"{name} · HOLD {hold}")
    while hold > 0:
        txt, dmg = moves[turn % len(moves)]
        p(); p(f"> {txt}"); hud(); p(f"  {name} HOLD {bar(hold*100//foe[1], 8)}")
        opts = ["Strike." + (" (you know where)" if primed else ""),
                "Read it. Find the seam.",
                "Allen. Go.", "Stillness. Take the hit and recover energy."]
        if gear: opts.append(f"Phil: {GEAR[-gear]}")
        if frame: opts.append(f"BLACK FRAME ({frame})")
        a = opts[ask("", opts)]
        block = False
        if a.startswith("Strike"):
            hold -= 6 if primed else 2; primed = False
            p("You hit it where it seems human. It gives a little.")
        elif a.startswith("Read"):
            up(8); burn(1); primed = block = True
            p("You see it coming, and you see the seam behind it: the place it is "
            "still forming, still a boy. You step out of the way.")
        elif a.startswith("Allen"):
            hold -= 4; up(6)
            say ("ALLEN", ALLEN_LINES[turn % len(ALLEN_LINES)])
            p("He moves at a speed where you can\'t tell what he does. But it works.")
        elif a.startswith("Phil"):
            gear -= 1; block = True
            say("PHIL", ['"Eyes shut, Adron. I mean it."', '"Built this with stolen tech, don\'t tell Royce."'][gear])
        elif a.startswith("Stillness"):
            burn(-2)
            p("You take the hit head on. The impact is heavy, but something inside "
              "you is calming, stabilizing.")
        else:
            frame -= 1; block = True; up(-8)
            p("BLACK FRAME. The room loses any meaning, including the "
            "part that was part that was about to hurt you.")
        if hold > 0 and not block:
            body -= dmg; p(f"It lands. BODY -{dmg}")
            say(*HIT[(turn + len(read)) % len(HIT)])
        if body <= 0 or res >= 100: return False
        turn += 1
    p(f"{name} lets go."); rule("-")
    return True

HIT = [("ALLEN", '"Walk it off. Or don\'t, I don\'t care."'),
       ("PHIL", '"Adron! Talk to me!"'),
       ("ALLEN", '"Oh, that looked like it hurt. Did it? Tell me."'),
       ("PHIL", '"Allen, cover him, I swear to God--"')]
ALLEN_LINES = ['"Finally, something in this house to hit. Phil, '
               'you\'re next."',
               '"Hold still. Not you, Adron. It."',
               '"I\'m having a great time. Is that allowed? Does it matter?"']

# scenes
def drive():
    p("ROYCE TECHNOLOGIES · INFERNO · FIELD OPERATION 000") 
    p("HEAD INVESTIGATOR: ADRON ETERE") 
    p("SUPPORTING INVESTIGATOR(S): PHIL FESTUS, ALLEN MAHAAN") 
    p("SUPERVISOR(S): LEO ROYCE V"); p()
    p("The old city, the hour where the light starts fading. Phil "
      "drives, headphones around his neck. Allen is in the back, racing "
      "jacket, feet on your seat, chewing something as he toys with a "
      "metal bracelet. You are Adron, sitting next to Phil "
      "in the front, and this is - fortunately or unfortunately "
      "your team for this case.")
    say("ALLEN", '"I\'m just saying, I think I should be the one driving. '
        'Phil\'s too slow."')
    say("PHIL", "Last time you had the wheel, you drove us off a cliff.")
    say("ALLEN", '"But we still got there faster."')
    say("YOU", '"In Allen\'s defense, I think anyone would choose to drive "' 
    'of a cliff than deal with you two bickering."')
    say("PHIL", '"Real funny, Adron."')
    p("A voice crackles through the homemade walkie-talkie on the dashboard. "
      "Your boss, Leo.")
    say("LEO", '"Standard containment. A residence. I\'ll walk you through "' 
    'the mechanics on site."')
    p(); p("You place a hand on your locket. Phil understands. Allen doesn't." 
    " You don't bother explaining.")
    wait()

def house():
    rule(); p("THE HOUSE"); rule()
    p("The door is unlocked. It smells like a meal is about to be served."
      " Not cooking. Served. The house is devoid of life.")
    say("LEO", '"What you feel is Resonance. Attention leaves residue and ' 
    'some people can read it. Every read raises the field. If you' 
    ' need to push through, we call the technique SECOND ANSWER."')
    say("PHIL", '"Who\'s we?"')
    say("ALLEN", '"The feds and the aliens, Phil."')
    say("PHIL", '"...what?"')
    say("ALLEN", '"Joking."')
    while True:
        beat(); p(); hud()
        left = [k for k in OBJ if k not in read]
        if not left: break
        n = ask("What do you inspect?", 
            [OBJ[k][0] for k in left] + ["Stop. You have enough."])
        if n == len(left):
            if len(read) >= NEED: break
            say("PHIL", f'"{NEED}, minimum. I\'m not filing less."'); continue
        k = left[n]; read.add(k); up(COST)
        p(); p(OBJ[k][1])
        who, line = OBJ[k][2] 
        say(who, line) if who else p(line)
        if res >= 100: return False
        if len(read) == 4: 
            say("PHIL", '"Adron, that\'s enough. It\'s eating it."')
            p("The object has started to melt into the foundation of the house.")
        for g in GATES:
            if res >= g and g not in fired:
                fired.add(g)
                if g == GATES[0]:
                    p(); p("On the stairs, a black feather. You blink. "
                     "Third time since the accident. You haven't told anyone.")
                    say("PHIL", '"Take as long as you want in here. Honestly."')
                    p("Phil does not say things like that.")
                if not fight(CLOCKS): return False
    return True

def deduce():
    rule(); p("THE ATTENDING"); rule()
    p("Upstairs, a woman is awake with the light on. She has been awake "
      "with the light on for nineteen years. She is not surprised by you.")
    say("PHIL", '"Okay. Say it. Who and what.')
    while True:
        a = ask("Who died?", ["The son. He went out one night.",
                              "The father. He's downstairs, so no.",
                              "A lodger. Someone outside the family."])
        b = ask("What did they want most, at the end?", 
                ["To be forgiven.", "To be waited for.", "To come home."])
        if (a, b) == (0, 1):
            p(); p("Not to come home. Coming home is something *you* do. "
             "He wanted the waiting: coat brushed, place set, door watched. " 
             "He has had it every night for nineteen years, long enough " 
             "that it remembers him.")
            p(); p('From the foot of the stairs, once, in a voice that has ' 
            'not aged at all: "Mom?"')
            p("There's something different in Allen's expression. He hides " 
            "it before you can ask. But the case is done.")
            return True
        p(); p("The house doesn't change. Being wrong out loud is still "
         "attention."); up(10); hud()
        if res >= 100: return False
        say("ALLEN", '"Bold. Dramatic. But wrong. Go again."')

def leave():
    rule(); p("BREAK OUT"); rule()
    p("You turn for the door and the house stands up. It is not angry. It " 
     "is a boy who wanted to be waited for, and you are leaving, and " 
     "leaving is the only thing it remembers being afraid of.")
    say("PHIL", '"Civilian upstairs. Nothing gets past this hallway."')
    say("ALLEN", '"Ooh, team building."')
    global body
    p("Allen pulls his bracelet over his knuckles. Phil tapes your " 
    "own before you can do it yourself. BODY +4."); body = min(12, body + 4)
    if not fight(WAITING): return False
    n = ask("It's open. One clean shot.",
            ["SECOND ANSWER.", "Let Allen end it."])
    if n:
        p("Allen grins like you've handed him a present. Then he sees your " 
        "face, and steps back, and says\"fine,\" like it costs him. It " 
        "doesn't. He wanted to see if you'd let him.")
    p("You say the name Leo gave it an hour ago, out loud, and it works, " 
    "which you will think about later. You don't let these things go.")
    p(); p('    "SECOND ANSWER."'); p()
    p("The hallway is a hallway again. The door is four steps away, then " 
    "none.")
    wait(); return True

def lost():
    rule()
    p("You're elsewhere. You sit at the table because it would be " 
     "strange not to. He is well dressed and smiling, and he " 
     "says we, and you find you agree.")
    p("Phil and Allen are shouting. It doesn't reach.")
    p(); p("FIELD OPERATION 000 · CONDITION: UNHELD") # UNHELD means you lost

def telling():
    rule(); p("THE TELLING"); rule()
    p("There is no equipment for this part. Royce never built any.")
    p("You go back upstairs and tell the woman her son is dead, and keep " 
     "telling her until she has heard it. Nothing is exorcised. Somebody " 
     "is told the truth and stops waiting, and the thing made of waiting " 
     "has nothing left to be made of.")
    rule(); p("ROUTING"); rule()
    p("An ambulance should come. A van comes, white, Royce. The men are " 
    "kind and very fast.")
    say("LEO", '"Royce processing. They\'ll be looked after."')
    p("True. You ask where. He tells you something else that is true. " 
    "Leo's security consultant leans on the van and looks at you half "
    "second longer than the job needs.")
    say("ALLEN", '"Diner? Diner. Adron\'s paying, he got to say the cool thing"')
    p("You write it down first. Phil sees and doesn't ask.")
    rule()
    p("ROYCE FILING ............ RELEASED")
    p("FIELD NOTEBOOK ............ 1 ENTRY")
    p("FIELD OPERATION 000 · CONDITION: CONTESTED") # a bittersweet ending :( most are
    p(f"READ {len(read)}/5 · BODY {body}/12 · FRAME {frame} · RES {res:03d}%")
    p(f"NERVE CONDUCTION: {100 - nerve*10}%")
    if nerve >= 7: p("SCARRING: L HAND")
    p("ZONE RESHAPING: PERMANENT. NOT SCHEDULED FOR REVIEW.")
    p(); p("RESOLVE")
    p(); input("[ press enter to close ]")


def main():
    drive()
    for scene in (house, deduce, leave):
        if not scene(): return lost()
    telling()

if __name__ == "__main__":
    try: main()
    except (KeyboardInterrupt, EOFError): print("\n[ transmission ends ]")








