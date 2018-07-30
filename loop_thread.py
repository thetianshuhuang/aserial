
"""Loop-based thread manager"""

import threading
import logging


class LoopThreading(threading.Thread):
    """Loop-based thread manager"""

    def __init__(self):
        threading.Thread.__init__(self)

    def loop(self, exit_request):
        """Main loop to run.

        This method should be overwritten.

        Raises
        ------
        Exception
            This method should NEVER be allowed to run. An ``Exception`` is
            always raised.

        Returns
        -------
        bool
            ``True`` if the loop should continue running; ``False`` otherwise.
            This placeholder function always returns ``False``.
        """

        logging.warning(
            "threaded_device instance created without a main loop.")
        raise Exception(
            "threaded_device instance created without a main loop " +
            "(a thread has been created that does nothing)")

        return False

    def main_alive(self):
        """Checks if python's main thread is alive.

        Returns
        -------
        bool
            ``True`` if the main thread can be located and is alive; ``False``
            otherwise
        """
        for thread in threading.enumerate():
            if thread.name == "MainThread":
                return(thread.is_alive())

        return False

    def run(self):
        """Run the main loop.

        The main loop (``self.loop``) will be run until one of the following
        occurs:
        - ``self.loop`` returns ``False``
        - The main thread can no longer be found or has been terminated
        - ``self.exit_request`` has been set to ``True``
        """

        while self.loop() and self.main_alive() and not self.exit_request:
            pass

        self.done = True
