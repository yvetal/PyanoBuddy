import mido, random

from time import sleep, time

from scales import scales

keys = {
    'C': 60,
    'C#': 61,
    'D': 62,
    'D#': 63,
    'E': 64,
    'F': 65,
    'F#': 66,
    'G': 67,
    'G#': 68,
    'A': 69,
    'A#': 70,
    'B': 71
}
    

class Looper():
    def __init__(self):
        self._out_port = mido.open_output(mido.get_output_names()[0])
        self._in_port = mido.open_input(mido.get_input_names()[0])
        self._notes = [60]
        self._note_count = 12
        self._timer = 5
        self._max_note_count = 2
    
    def _play_note(self):
        for note in self._notes:
            self._out_port.send(mido.Message('note_on', note=note, velocity=100))
            sleep(0.2)
            self._out_port.send(mido.Message('note_off', note=note))

    def _listen_for_note(self):
        start_time = time()
        
        matched = set()

        while time() - start_time < self._timer:  
            for msg in self._in_port.iter_pending():
                if msg.type == 'note_on' and msg.velocity > 0:
                    if msg.note in self._notes:
                        if msg.note not in matched:
                            matched.add(msg.note)
                            print(f"✅ Correct ({len(matched)}/{self._note_count})")
                    else:
                        print("❌ Wrong note, listen again!\n")
                        matched.clear()  # reset if any wrong

            if len(matched) == len(set(self._notes)):
                return True
            
        return False
    
    def run_loop(self):
        while True:
            self._note_count = random.choice(range(1,self._max_note_count))

            self._notes = random.choices([keys['A']+i for i in scales['HARMONIC_MINOR']], k=self._note_count)

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