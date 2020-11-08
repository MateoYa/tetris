from pynput import keyboard


def on_press(key):
    if key == keyboard.Key.left:
        print(key)


listener = keyboard.Listener(on_press=on_press)
listener.start()
