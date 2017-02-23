"""Contains all the classes and functions related to the commands handling of the
   telemetry package.
"""


import queue
import threading

from .selectors import Selector


class CommandHandler:
    """Handle accesses to the commands queues."""

    def __init__(self,
                 selector: Selector,
                 consumed: queue.Queue,
                 produced: queue.Queue):
        """Initialize the `TaskHandler`.

        :param selector: The selector that will be used to fetch/send the
                         packets to the other connected host
        :type selector: :mod:`design.telemetry.selectors.Selector`
        :param consumed: The commands to be sent over the network
        :type consumed: :mod:`queue.Queue`
        :param produced: The commands to be handled by the AI
        :type produced: :mod:`queue.Queue`
        """
        self._consumed = consumed
        self._produced = produced

        self._selector = selector
        self._selector_thread = threading.Thread(target=self._selector.run,
                                                 daemon=True)
        self._selector_thread.start()

    def put_command(self, packet):
        """Add a command to be sent.

        :param packet: The packet to be sent
        :type packet: :mod:`design.telemetry.packets.Packet`
        """
        try:
            self._consumed.put_nowait(packet)
        except queue.Full:
            pass

    def fetch_command(self):
        """Fetch a command from the received ones.

        :returns: A packet that was received from the network. If there is no
                  data in the queue, returns `None`.
        :rtype: :mod:`design.telemetry.packets.Packet`
        """
        command = None
        try:
            command = self._produced.get_nowait()
        except queue.Empty:
            pass

        return command
