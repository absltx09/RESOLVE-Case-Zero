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

res, body, nerve, frame, gear = 0, 12, 0, 2, 2
read, seen, fired = set(), -1, set()
def up(n):
    global res; res = max(0, min(100, res + n))

OBJ = {
    "coat": ("The coat on the hanger by the door", 
    "A wool coat, brushed often. It has not been worn in "
    "nineteen years. It is the cleanest thing in the house.",
    ("PHIL", '"That\'s a lot of care put into one coat. Whoever it belongs to must have been gone for a while."')),
    "table": ("The dinner table", "Five seats. Only four people live here. The fifth is in the middle, where "
    "the life of the party would be. The plate is warm.", 
    ("ALLEN", '"Man, I could go for some dinner."'),
    ("PHIL", '"We just ate."')),
    "calendar": ("The calendars in the kitchen", 
    "Nineteen on one nail, every year turned to the same month. Someone ")
}