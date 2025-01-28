import sys

class Debugger:
    """A utility class for debugging purposes.

    This class provides a simple interface for printing debug messages
    to standard error output.

    Attributes:
        None

    Methods:
        print(message): Prints a debug message to stderr.
    """
    def print(self, message):
        """
        Prints a message to the standard error stream.

        This method redirects the output to stderr instead of stdout, which is useful for
        debugging and error reporting purposes.

        Args:
            message: The message to be printed to stderr. Can be any object that can be
                    converted to a string.

        Examples:
            >>> debug = Debug()
            >>> debug.print("Error occurred")  # Prints to stderr
        """
        print(message, file=sys.stderr)
