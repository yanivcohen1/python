import re

# ה-Regex:
# (?s)     -> "same as re.DOTALL" שמאפשר ל- . להתאים גם לתווי שורה חדשה
# \[      -> סוגריים מרובעים פותחים (צריך escape כי זה תו שמור)
# cite    -> המילה cite
# .*?     -> כל תו (.), אפס פעמים או יותר (*), באופן "עצלן" (?) כדי לעצור בסגירה הראשונה
# \]      -> סוגריים מרובעים סוגרים
regex_pattern = r"(?s)\[cite.*?\]"

content = """Welcome to [cite: 1] and also
to [cite: 2]!"""

clean_content = re.sub(regex_pattern, "", content)

print(clean_content)
# פלט:
# Welcome to  and also
# to !
