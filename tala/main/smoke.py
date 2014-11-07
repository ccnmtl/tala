from smoketest import SmokeTest
from .models import Room
import zmq
from django.conf import settings
import json

zmq_context = zmq.Context()


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = Room.objects.all().count()
        self.assertTrue(cnt > 0)


class BrokerConnectivity(SmokeTest):
    def test_connect(self):
        """ a simple check to see if we can open up a socket
        to the zmq broker.

        We send a message and wait three seconds for a response.

        Send the message to room "0", which should never
        conflict with an actual chat room.
        """
        socket = zmq_context.socket(zmq.REQ)
        socket.setsockopt(zmq.LINGER, 0)
        socket.connect(settings.WINDSOCK_BROKER_URL)

        try:
            # the message we are broadcasting
            md = dict(room_id=0,
                      username="smoketest",
                      message_text="smoketest")
            # an envelope that contains that message serialized
            # and the address that we are publishing to
            e = dict(address="%s.room_0" % (settings.ZMQ_APPNAME),
                     content=json.dumps(md))
            # send it off to the broker
            socket.send(json.dumps(e))
            # wait for a response from the broker to be sure it was sent

            poller = zmq.Poller()
            poller.register(socket, zmq.POLLIN)
            if poller.poll(3 * 1000):  # 3s timeout in milliseconds
                socket.recv()
            else:
                raise IOError("Timeout connecting to broker")
            self.assertTrue(True)
        except:
            self.assertTrue(False)
        finally:
            socket.close()
