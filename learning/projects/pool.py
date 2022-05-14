favorite_languages = {"jen": "python", "sarah": "c", "edward": "ruby", "phil": "python"}

friends = ["phil", "sarah"]

for k, y in favorite_languages.items():
    if k not in friends:
        print(f"{k} you should take you pool ")
    else:
        print(f"{k} Thank you for taking our pool ")
        print(f"I see your fav language is {y}")
