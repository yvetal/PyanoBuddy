import mido, random

from time import sleep, time
WHITE_NOTES = [60, 62, 64, 65, 67, 69, 71, 72]

class Looper():
    def __init__(self):
        self._out_port = mido.open_output(mido.get_output_names()[0])
        self._in_port = mido.open_input(mido.get_input_names()[0])
        self._notes = [60]
        self._note_count = 3
        self._timer = 3
    
    def _play_note(self):
        for note in self._notes:
            self._out_port.send(mido.Message('note_on', note=note, velocity=100))
        sleep(1)
        
        for note in self._notes:
            self._out_port.send(mido.Message('note_off', note=note))

    def _listen_for_note(self):
        start_time = time()
        
        matched = set()

        while time() - start_time < self._timer:  # wait up to 5 seconds
            for msg in self._in_port.iter_pending():
                if msg.type == 'note_on' and msg.velocity > 0:
                    if msg.note in self._notes:
                        if msg.note not in matched:
                            matched.add(msg.note)
                            print(f"✅ Correct ({len(matched)}/{self._note_count})")
                    else:
                        print("❌ Wrong note, listen again!\n")
                        matched.clear()  # reset if any wrong

            if len(matched) == self._note_count:
                return True
            
            sleep(0.05)

            if len(matched) < self._note_count:
                sleep(1)
        return False
        if len(matched) == self._note_count:
            return True
        else:
            return False
    def run_loop(self):
        while True:
            self._notes = random.sample(WHITE_NOTES, self._note_count)

            matched = False
            while not matched:
                self._play_note()
                matched = self._listen_for_note()
                # wait for input
                
            sleep (0.5)
def main():
        

    looper = Looper()
    looper.run_loop()
    

if __name__=='__main__':
    main()