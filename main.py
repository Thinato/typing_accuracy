import pygame as pg
import random

pg.init()

screen = pg.display.set_mode((400, 300))
pg.display.set_caption("Typing Accuracy Test")
clock = pg.time.Clock()

font_big = pg.font.Font("./font.ttf", 50)
font = pg.font.Font("./font.ttf", 36)

level = 1
mistakes = 0
correct = 0

letter_map = {
    "a": 0,
    "o": 1,
    "e": 2,
    "u": 3,
    "h": 4,
    "t": 5,
    "n": 6,
    "s": 7,
    "i": 8,
    "d": 9,
    "p": 10,
    "y": 11,
    "f": 12,
    "g": 13,
    "k": 14,
    "x": 15,
    "b": 16,
    "m": 17,
    "j": 18,
    "w": 19,
    "c": 20,
    "q": 21,
    "v": 22,
    "r": 23,
    "l": 24,
    "z": 25,
}


def generate_text(level, weights, last_letter=None):
    letters = "aoeuhtns"

    if level > 2:
        letters += "id"
    if level > 3:
        letters += "pyfg"
    if level > 4:
        letters += "kxbm"
    if level > 5:
        letters += "jwc"
    if level > 6:
        letters += "qvr"
    if level > 7:
        letters += "lz"

    res = random.choices(letters, weights[: len(letters)])[0]
    while res == last_letter:
        res = random.choices(letters, weights[: len(letters)])[0]
    return res


if __name__ == "__main__":
    running = True
    weight = [1 for i in range(len(letter_map))]
    text = generate_text(level, weight)
    is_correct = True
    lpm = 0
    while running:
        clock.tick(60)
        accuracy = correct / (correct + mistakes) * 100 if correct + mistakes > 0 else 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.unicode == text:
                    correct += 1
                    text = generate_text(level, weight, text)
                    is_correct = True
                    weight[letter_map[text]] *= 0.85
                    if (correct - level * 15) > 0 and accuracy > 90:
                        level += 1
                else:
                    mistakes += 1
                    is_correct = False
                    weight[letter_map[text]] *= 1.5
                    if accuracy < 90:
                        level = max(1, level - 1) if level < 7 else 7
                print(f"Correct: {correct}, Mistakes: {mistakes}")

        screen.fill((255, 255, 255))
        text_surface = font_big.render(
            text.upper(), True, (0, 0, 0) if is_correct else (255, 0, 0)
        )
        screen.blit(text_surface, (100, 10))

        lpm = correct / (pg.time.get_ticks() / 60000)

        lpm_surface = font.render(f"LPM: {lpm:.2f}", True, (0, 0, 0))
        screen.blit(lpm_surface, (10, 150))

        accuracy_surface = font.render(f"Accuracy: {accuracy:.2f}%", True, (0, 0, 0))
        screen.blit(accuracy_surface, (10, 200))

        level_surface = font.render(f"Level: {level}", True, (0, 0, 0))
        screen.blit(level_surface, (10, 250))

        pg.display.flip()
