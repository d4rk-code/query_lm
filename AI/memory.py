history = []

LIMIT = 6 # largest context of 4 chats

if len(history) > LIMIT:
    history.pop(0)
