import re
def clean_response(line):
    line = re.sub(r"(?i)^(you should )?(say|respond|reply|answer)( with)? ", "", line).strip()
    return line

print(clean_response("you should say hello back"))
print(clean_response("say hi"))
print(clean_response("respond with how are you"))
print(clean_response("I am fine"))
