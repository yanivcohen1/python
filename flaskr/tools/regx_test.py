import re

# ה-Regex:
# (?s)     -> "same as re.DOTALL" שמאפשר ל- . להתאים גם לתווי שורה חדשה
# \[      -> סוגריים מרובעים פותחים (צריך escape כי זה תו שמור)
# cite    -> המילה cite
# .*?     -> כל תו (.), אפס פעמים או יותר (*), באופן "עצלן" (?) כדי לעצור בסגירה הראשונה
# \]      -> סוגריים מרובעים סוגרים
regex_pattern = r"(?s)\[cite.*?\]"

content = """Welcome to [cite: 1] and also
to [cite: 3]!"""

# to remove [cite: XX] from the content
clean_content = re.sub(regex_pattern, "", content)

print(clean_content)
# Welcome to  and also
# to !

# to find all [cite: XX] from the content
matches = re.findall(regex_pattern, content)

print(matches) # ['[cite: 1]', '[cite: 3]']

# in shellscript:
# yaniv@YanivAsusLaptop:~$ echo "hello [cite :1] from [cite :3] world" | grep -o '\[cite[^]]*\]'
# [cite :1]
# [cite :3]
# yaniv@YanivAsusLaptop:~$ echo "hello [cite :1] from [cite :3] world" | sed 's/\[cite[^]]*\]//g'
# hello  from  world
