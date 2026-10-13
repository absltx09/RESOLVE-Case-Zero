import textwrap

W = 72
def p(s=""):
    for ln in textwrap.wrap(s, W) or [""]: print(ln)
def say(who, s): p(f"{who:<6} {s}")
def rule(c="="): p(c * W)
def bar(n, size=10): return "#" * (n * size // 100) + "." * (size - n * size // 100)
def hud():
    p(f"[ RESONANCE {bar(res)} {res:03d}% BODY {bar(body*100//12, 6)} NERVE {bar(nerve)} FRAME {frame}]")
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
        if WARM[t]: p(); p(WARM[t])
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
 ("Upstairs, a door opens. Something is coming down to wait with you."), 4])

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
                "Allen. Go."]
        if gear: opts.append(f"PHIL: {GEAR[-gear]}")
        if frame: opts.append(f"BLACK FRAME ({frame})")
        a = opts[ask("", opts)]
        block = False
        if a.startswith("Strike"):
            hold -= 6 if primed else 2; primed = False
            p("You hit it where it seems human. It gives a little.")
        elif a.startswith("Read"):
            up(8); primed = block = True
            p("You see it coming, and you see the seam behind it: the place it is "
            "still forming, still a boy. You step out of the way.")
        elif a.startswith("Allen"):
            hold -= 4; up(6)
            say ("ALLEN", ALLEN_LINES[turn % len(ALLEN_LINES)])
            p("He moves at a speed where you can\'t tell what he does. But it works.")
        elif a.startswith("Phil"):
            gear -= 1; block = True
            say("PHIL", ['"Eyes shut, Adron. I mean it."', '"Built this with stolen tech, don\'t tell Royce."'])

