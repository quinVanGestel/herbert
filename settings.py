import json

#region global settings
with open('settingsGlobal.json', 'r') as file:
    settingsGlobal = json.load(file)
    OWNERID: int = settingsGlobal['ownerID']
#endregion

#region guild settings
with open('settingsGuild.json', 'r') as file:
    settingsGuild = json.load(file)

commandPrefix:list[str] = settingsGuild['commandPrefix']
stripAfterPrefix:list[str] = settingsGuild['stripAfterPrefix']

equippableRoles:list[str] = settingsGuild['equippableRoles']

humanGreetings:list[str] = settingsGuild['humanGreetings']
botGreetings:list[str] = settingsGuild['botGreetings']
botPunctuations:list[str] = settingsGuild['botPunctuations']
#endregion
