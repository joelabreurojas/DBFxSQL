import logging
import os
import signal
import subprocess

from watchfiles import run

logger: logging.Logger = logging.getLogger("watchfiles.main")


class SignalSafeCombinedProcess(run.CombinedProcess):
    """
    A subclass of CombinedProcess that handles process termination with SIGINT
    and SIGKILL, providing more robust and informative logging.
    """

    def stop(self, sigint_timeout: int = 5, sigkill_timeout: int = 1) -> None:
        """
        Stops the managed process, attempting graceful termination with SIGINT
        followed by SIGKILL if necessary.
        """
        os.environ.pop("WATCHFILES_CHANGES", None)

        if not self.is_alive():
            logger.warning("Process already terminated, exit code: %s", self.exitcode)
            return

        logger.debug("Stopping process...")

        try:
            self.join(sigint_timeout)
        except subprocess.TimeoutExpired:
            logger.warning(f"SIGINT timed out after {sigint_timeout} seconds.")
            self._force_kill(sigkill_timeout)
        else:
            logger.debug("Process stopped gracefully.")

    def _force_kill(self, sigkill_timeout: int) -> None:
        """
        Sends SIGKILL to the process and waits for it to terminate.
        """
        if self.exitcode is None:
            logger.warning("Process did not terminate after SIGINT, sending SIGKILL.")
            self.send_signal(signal.SIGKILL)
            try:
                self.join(sigkill_timeout)
            except subprocess.TimeoutExpired:
                logger.error(
                    f"SIGKILL timed out after {sigkill_timeout} seconds. "
                    "Process may be hung."
                )
            else:
                logger.debug("Process terminated after SIGKILL.")
        else:
            logger.debug("Process stopped after SIGINT timeout, but before SIGKILL.")
