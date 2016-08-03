import re
def regexp(text):
    pattern = re.compile('[^a-zA-Z\s]')
    rezult = re.search(pattern, text)
    if rezult:
        return False
    else: return True
