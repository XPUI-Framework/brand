"""The pixel alphabet the mark is drawn in: X, P, U and I, in two weights."""

LIGHT = {
    "X": ["X...X", ".X.X.", "..X..", ".X.X.", "X...X"],
    "P": ["XXXX.", "X...X", "XXXX.", "X....", "X...."],
    "U": ["X...X", "X...X", "X...X", "X...X", ".XXX."],
    "I": ["XXXXX", "..X..", "..X..", "..X..", "XXXXX"],
}

BOLD = {
    "X": ["XX.......XX", "XXX.....XXX", ".XXX...XXX.", "..XXX.XXX..", "...XXXXX...",
          "....XXX....", "...XXXXX...", "..XXX.XXX..", ".XXX...XXX.", "XXX.....XXX",
          "XX.......XX"],
    "P": ["XXXXXXXXX..", "XXXXXXXXXX.", "XX......XXX", "XX.......XX", "XX......XXX",
          "XXXXXXXXXX.", "XXXXXXXXX..", "XX.........", "XX.........", "XX.........",
          "XX........."],
    "U": ["XX.......XX", "XX.......XX", "XX.......XX", "XX.......XX", "XX.......XX",
          "XX.......XX", "XX.......XX", "XX.......XX", "XXX.....XXX", ".XXXXXXXXX.",
          "..XXXXXXX.."],
    "I": ["XXXXXXXXXXX", "XXXXXXXXXXX", "....XXX....", "....XXX....", "....XXX....",
          "....XXX....", "....XXX....", "....XXX....", "....XXX....", "XXXXXXXXXXX",
          "XXXXXXXXXXX"],
}
