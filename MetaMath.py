import subprocess
import threading
import queue

class MetaMath():
    """
    Class Representing the MetaMath program
    make sure metamath.exe is in path / current working directory
    Instantiating this class creates an process of metamath.exe
    >>> m = MetaMath()

    To send input use the send method 
    >>> m.send(str)
    To read the buffer see m.outq and m.errq
    They're Queue objects so see: https://docs.python.org/3/library/queue.html
    """
    def __init__(self):
        def output_reader(stream,outQueue):
            for char in iter(lambda: stream.read(1), b''):
                outQueue.put(char)
        self.outq = queue.Queue()
        self.errq = queue.Queue()
        self._proc = subprocess.Popen("metamath.exe",
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        t = threading.Thread(target=output_reader, args=(self._proc.stdout,self.outq,))
        terr = threading.Thread(target=output_reader, args=(self._proc.stderr,self.errq,))
        t.start()
        terr.start()

    def send(self,str):
        self._proc.stdin.write(str.encode())
        self._proc.stdin.write(b"\n")
        self._proc.stdin.flush()
# example how to use 
print(''.join((c.decode() for c in m.outq.queue)))