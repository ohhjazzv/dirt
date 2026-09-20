dirt

dirt is a farming game that runs in your terminal. you plant stuff, wait for it to grow, harvest it before the weather kills it, and use the money to buy better stuff. built in a week for third space by two people who are both worse at python than they'd like to be.

running it

you need python 3 and nothing else — no dependencies. python main.py for the terminal version, python gui.py for the window version. same game underneath, two ways of looking at it.

how it plays

you start with 10 coins and six empty plots. each plot shows a letter for the crop and a number for days left, so w1 is wheat with one day to go. capital letter with a ! means ready. hit 4 and a day passes — everything ages and the weather rerolls.

three crops: wheat (3 coins, sells 8, 3 days, 5% storm risk), chili (8, 22, 5 days, 10%) and melon (20, 65, 8 days, 15%). melons pay by far the best but sit in the ground nearly three times longer, so the weather gets way more chances at them. that tradeoff is basically the only real decision the game asks you to make, but it's a decent one. on storm days every growing crop rolls against its own risk and can just die. nothing you can do once it's planted.

how it's built

two files, and the split between them is the actual point. farm_1.py holds the rules and never prints anything — it doesn't know an interface exists. main.py is the terminal side and holds zero game rules; it asks questions and prints what the rules file hands back. gui.py is the same thing as a window.

the halves only talk through four functions: plant(plot, seed), harvest(plot), advance_day() and get_state(). we wrote that contract down before writing any actual code, which is the only reason two people could work at once without breaking each other's stuff. it also meant the gui got bolted on later without touching the rules file once. wasn't planned, but nice when it happened.

krish built farm_1.py and gui.py. jaz built main.py.

not done

no achievements or stats, no watering or anything that lets you affect your own odds, only three crops, and no real reason to keep playing once you can afford melons.
