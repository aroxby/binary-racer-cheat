#!/usr/bin/env python3
from pynput import keyboard
import keys


class StringListener(keyboard.Listener):
    def __init__(self, *args, **kwargs):
        # For some reason constructor assignments have different semantics than attribute assignments
        super().__init__(*args, **kwargs, on_press=self._on_key_down)
        self.on_release = self._on_key
        self.string = ""
        self.controller = keyboard.Controller()

    def _on_key_down(self, key) -> bool:
        vk = vk_from_key(key)
        if vk == ord("X"):
            print("Exiting...")
            return False
        return True

    def _on_key(self, key, injected) -> None:
        if injected:
            return
        vk = vk_from_key(key)

        if vk in range(keys.KP_0, keys.KP_9 + 1):
            i = vk - keys.KP_0
            self.string += str(i)
            print(f"Current string: {self.string}")
        elif vk == keys.ENTER:
            i = int(self.string) if self.string else 0
            self.string = ""
            game_input = to_tcg_string(i)
            print(f"Injecting: {game_input}")
            self.controller.type(game_input)
        elif vk == keys.BACKSPACE:
            self.string = ""
            print(f"Current string: {self.string}")


def vk_from_key(key) -> int:
    if hasattr(key, "vk"):
        return key.vk
    return key.value.vk


def to_tcg_string(i: int) -> str:
    i &= 0xFF
    bit_key = 8
    s = ""

    while i > 0:
        if i & 1:
            s += str(bit_key)
        i >>= 1
        bit_key -= 1

    return s + "\n"


def main():
    with StringListener() as listener:
        listener.join()


if __name__ == "__main__":
    main()
