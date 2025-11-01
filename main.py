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
        self._note_count = 4
        self._timer = 5
        self._max_note_count = 1
        self._context = True
        
    
    def _play_note(self):
        for note in self._notes:
            self._out_port.send(mido.Message('note_on', note=note, velocity=100))
            sleep(0.2)
            self._out_port.send(mido.Message('note_off', note=note))

    def _listen_for_note(self):
        start_time = time()
        
        matched = []
        while time() - start_time < self._timer:  
            for msg in self._in_port.iter_pending():
                if msg.type == 'note_on' and msg.velocity > 0:
                    matched.append(msg.note)
                    if len(matched) == self._note_count:
                        break
            if matched == self._notes:
                return True
        print('Time up')
        return False
    
    def run_loop(self):
        self._streak = 0
        while True:
            if(self._streak > 20):
                self._streak = 0
                self._max_note_count +=1
                print(f'Streak reached! Max count is now {self._max_note_count}')

            root = keys['C']
            scale = scales['MAJOR_CHORD']
            self._note_count = random.choice(range(1,self._max_note_count+1))
            self._notes = random.choices([root+i for i in scale], k=self._note_count)
            if self._context:
                self._note_count +=1
                self._notes = [root]+self._notes
            match = False
            while not match:
                self._play_note()
                match = self._listen_for_note()
                if match:
                    print(f"✅ Correct")
                    self._streak += 1
                else:
                    print("❌ Wrong note, listen again!\n")
                    self._streak = 0
                print(f'Streak: {self._streak}')
                
                sleep(0.5)
def main():
        

    looper = Looper()
    looper.run_loop()
    

if __name__=='__main__':
    main()