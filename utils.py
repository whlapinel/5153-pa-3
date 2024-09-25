
import domain


def translate(position: domain.Position, direction: domain.Direction)->domain.Position:
    return domain.Position(position.x_coord + direction[0], position.y_coord + direction[1])



def int_input_with_limits(min: int, max: int, prompt: str)->int:
    valid_input = False
    entry = 0
    while not valid_input:
        entry = int(input(prompt))
        valid_input = min <= entry <= max
        if not valid_input:
            print(f'Invalid input! Must be integer between {min} and {max}.')
    return entry
