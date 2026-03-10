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


text = """hello: 'game :["a 1"]' from 'cite2 :{b: 3}'
world 'cite3 :c99'"""

# This pattern looks for:
# '      - an opening single quote
# (      - start of a capture group
#  [^']+ - one or more characters that are NOT a single quote
# )      - end of capture group
# '      - a closing single quote
results = re.findall(r"'([^']+)'", text)
print(results)
# Output: ['game :["a 1"]', 'cite2 :{b: 3}', 'cite3 :c99']

# ---------- without regx ------------

# Split the text by the single quote
parts = text.split("'")
# Extract every second element (odd indices)
# [start:stop:step] -> [1::2] starts at index 1 and takes every 2nd item
results = parts[1::2]
print(results)
# Output: ['game :["a 1"]', 'cite2 :{b: 3}', 'cite3 :c99']


# ----------- in shellscript ------------------:
# Regex:
# (cite[^)]*) -> (cite followed by any characters that are not ) (using [^)]*), until the closing )
# echo "hello (cite :1) from (cite :3) world" | grep -o '(cite[^)]*)'
# (cite :1)
# (cite :3)
# replace (cite: XX) with empty string in shellscript:
# echo "hello (cite :1) from (cite :3) world" | sed 's/(cite[^)]*)//g'
# hello  from  world

# Regex:
# \[cite[^]]*\] -> \[cite followed by any characters that are not ] (using [^]]*), until the closing \]
# yaniv@YanivAsusLaptop:~$ echo "hello [cite :1] from [cite :3] world" | grep -o '\[cite[^]]*\]'
# [cite :1]
# [cite :3]
# sed replace [cite: XX] with empty string (using //):
# yaniv@YanivAsusLaptop:~$ echo "hello [cite :1] from [cite :3] world" | sed 's/\[cite[^]]*\]//g'
# hello  from  world

# to extract only the number or text after [cite: and before ]
# -P (Perl-Compatible Regular Expressions): This flag tells grep to use the Perl engine instead of the basic or extended POSIX engines.
#    This is essential because standard grep does not support advanced features like Lookarounds (Lookbehind/Lookahead).
# -o (Only matching): By default, grep prints the entire line containing a match.
#    This flag forces it to output only the specific part of the text that matched your pattern.
#    If there are multiple matches in one line, it will print each one on a new line.
# -a, you force grep to ignore those non-text characters and search through the content anyway.
# (?<=\[cite :) (Positive Lookbehind): This is a non-consuming assertion.
#    It tells the engine: "Look for a position that is preceded by the literal text
#    [cite :, but do not include that prefix in the final match result."
#     It effectively sets the "starting line" for the output right after the colon.
# [^]]* (Negated Character Class): As we discussed, this means "match any character that is not a closing bracket (]), zero or more times." This allows the command to capture any value (numbers, letters, or symbols) and ensures it stops exactly before the closing bracket.
#
# yaniv@YanivAsusLaptop:~$ echo "hello [cite :1] from [cite :a3] world" | grep -Pao '(?<=\[cite :)[^]]*'
# 1
# a3
