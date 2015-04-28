import threading
import time
import socket

class ThreadingServer(object):


    """ Threading example class

    The run() method will be started and it will run in the background
    until the application exits.
    """


    def __init__(self, interval=1):
        """ Constructor

        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()
        
    def run(self):
		TCP_IP = socket.gethostbyname(socket.gethostname())
		print "Local IP = " + TCP_IP
		TCP_PORT = 5005
		BUFFER_SIZE = 20  #rmally 1024, but we want fast response

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((TCP_IP, TCP_PORT))
		s.listen(1)
	 
		conn, addr = s.accept()
		print 'Connection address:', addr

		while 1:
			data = conn.recv(BUFFER_SIZE)
			if not data:
				break
			print "received data:", data
			conn.send(data)  # echo
		conn.close()

		



