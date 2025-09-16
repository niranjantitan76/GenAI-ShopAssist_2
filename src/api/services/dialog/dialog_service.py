from lib.dialog_manager import dialogue
async def dialog(user_input: str,state):
    return await dialogue(user_input, state)

