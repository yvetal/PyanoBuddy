import mido, random

from time import sleep

out_port = mido.open_output(mido.get_output_names()[0])

in_port = mido.open_input(mido.get_input_names()[0])
    
print(f"Using output: {out_port}")
print(f"Using input: {in_port}")
WHITE_NOTES = [60, 62, 64, 65, 67, 69, 71, 72]

sleep(0.2)
while True:
    note = random.choice(WHITE_NOTES)
    print(f"Play this note: {note}")

    matched = False
    while not matched:
        # play note
        out_port.send(mido.Message('note_on', note=note, velocity=100))
        sleep(1)
        out_port.send(mido.Message('note_off', note=note))

        # wait for input
        for msg in in_port:
            if msg.type == 'note_on':
                print(f"You played: {msg.note}")
                if msg.note == note:
                    print("Matched! Moving to next note.\n")
                    matched = True
                    break
                else:
                    print("Wrong note, listen again!\n")
                    break  # replay same note
    sleep (0.5)

