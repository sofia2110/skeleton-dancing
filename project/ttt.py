from ursina import *

app = Ursina()

camera.orthographic = True
camera.fov = 10
camera.position = (0, 0, -10)

window.title = 'Mini prj'
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True
window.color = color.black
game_state = 'explore'
current_dialogue = None
selected_option = 0

player = Entity(
    model='quad',
    texture='player.png',
    scale=1,
    position=(0, 0)
)

player_speed = 4

def move_player():
    player.x += (held_keys['d'] - held_keys['a']) * time.dt * player_speed
    player.y += (held_keys['w'] - held_keys['s']) * time.dt * player_speed

def update():
    if game_state == 'explore':
        move_player()

npc = Animation(
    'frame_',
    fps=8,
    loop=True,
    scale=3,
    position=(3, 0)
)

def player_near_npc():
    return distance(player.position, npc.position) < 1.2

dialogue_box = Button(
    parent=camera.ui,
    text='',
    color=color.black,
    text_color=color.white,
    scale=(0.9, 0.25),
    position=(0, -0.4),
    visible=False,
    highlight_color=color.black,
    pressed_color=color.black
)

npc_dialogue = {
    "text": "A wild skeleton blocks your path… suddenly, it starts dancing.",
    "options": [
        ("talk","talk"),
        ("fight","fight"),
        ("flee","flee")
    ]
}

def start_dialogue(dialogue):
    global game_state, current_dialogue, selected_option
    game_state = 'dialogue'
    current_dialogue = dialogue
    selected_option = 0

    dialogue_box.visible = True
    update_dialogue_text()

def update_dialogue_text():
    text = current_dialogue["text"] + "\n\n"
    for i, option in enumerate(current_dialogue["options"]):
        prefix = "> " if i == selected_option else "  "
        text += prefix + option[0] + "\n"

    dialogue_box.text = text

def handle_choice(choice):
    global game_state

    if choice == "talk":
        current_dialogue["text"] = "'Nice moves, bro.'\nskeleton keeps flossing like nothing happened."
        current_dialogue["options"] = [("Epic", "end")]

    elif choice == "fight":
        current_dialogue["text"] = "You try to attack… skeleton does a perfect moonwalk and dodges.\nBruh."
        current_dialogue["options"] = [("WTF?", "end")]

    elif choice == "flee":
        current_dialogue["text"] = "You run away safely, but the skeleton's dance moves haunt your dreams."
        current_dialogue["options"] = [("GG", "end")]

    elif choice == "end":
        dialogue_box.visible = False
        game_state = 'explore'
        return

    selected_option = 0
    update_dialogue_text()

def input(key):
    global selected_option, game_state

    if game_state == 'explore':
        if key == 'e' and player_near_npc():
            start_dialogue(npc_dialogue)

    elif game_state == 'dialogue':
        if key == 'w':
            selected_option = (selected_option - 1) % len(current_dialogue["options"])
            update_dialogue_text()

        elif key == 's':
            selected_option = (selected_option + 1) % len(current_dialogue["options"])
            update_dialogue_text()

        elif key == 'enter':
            choice = current_dialogue["options"][selected_option][1]
            handle_choice(choice)

    if key == 'escape':
        application.quit()
app.run()