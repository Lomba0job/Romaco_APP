import logging
from colorlog import ColoredFormatter

# Define a new logging level for SUCCESS
SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)

logging.Logger.success = success

# Define custom filters
class CodiceFilter(logging.Filter):
    def __init__(self, codici):
        super().__init__()
        self.codici = codici

    def filter(self, record):
        return getattr(record, 'codice', None) in self.codici

# Logger configuration for two log files
def setup_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)  # Set the minimum logger level

    # Colored formatter configuration for console output
    color_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'white',
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
            'SUCCESS': 'green'  # Color for SUCCESS level
        }
    )

    # Handler for app.log with a specific filter
    app_handler = logging.FileHandler('app.log')
    app_handler.setLevel(logging.DEBUG)
    app_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    app_handler.setFormatter(app_formatter)
    app_handler.addFilter(CodiceFilter(set(range(0, 1000))))  # Codici da 0 a 999 inclusi

    # Handler for thread.log with a specific filter
    thread_handler = logging.FileHandler('thread.log')
    thread_handler.setLevel(logging.DEBUG)
    thread_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    thread_handler.setFormatter(thread_formatter)
    thread_handler.addFilter(CodiceFilter(set(range(1000, 1501))))

    # Console handler for colored output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(color_formatter)

    # Add handlers to the logger
    logger.addHandler(app_handler)
    logger.addHandler(thread_handler)
    logger.addHandler(console_handler)

    return logger

# Dictionary mapping codes to log levels and messages
log_messages = {
    0: ('SUCCESS', 'Applicazione avviata.'),
    1: ('SUCCESS', 'Configurazione termianta: '),
    2: ('SUCCESS', 'Richiesta Peso termianta: '),
    3: ('SUCCESS', 'Bilancia singola peso terminato: '),
    4: ('SUCCESS', 'Tara totale termianta'),
    5: ('SUCCESS', 'Tara singola termianta'),
    6: ('SUCCESS', 'Calibrazione singola termianta'),
    7: ('SUCCESS', 'Salvataggio peso termianto'),
    
    101: ('INFO', 'Configurazione Richiesta'),
    102: ('INFO', 'Richiesta Peso '),
    103: ('INFO', 'Bilancia singola peso richiesta'),
    104: ('INFO', 'Tara totale richiesta'),
    105: ('INFO', 'Tara singola richiesta'),
    106: ('INFO', 'Calibrazione singola richiesta'),
    107: ('INFO', 'Salvataggio peso richiesto'),
    
    404: ('WARNING', 'Errore sconosciuto'),
    401: ('WARNING', 'Errore di Configurazione no ID'),
    402: ('WARNING', 'Errore di Configurazione errore risposta'),
    403: ('WARNING', 'Bilancia singola peso in errore interno: '),
    405: ('WARNING', 'Tara totale in Errore'),
    406: ('WARNING', 'Tara singola in Errore'),
    407: ('WARNING', 'Calibrazione singola in Errore'),
    408: ('WARNING', 'Salvataggio peso in Errore'),
    
    700: ('CRITICAL', 'Bilancie Scollegate'),
    701: ('CRITICAL', 'Deriva Eccessiva'),  #not implement
    
    1000: ('INFO', 'thread: '),
}

# Function to log messages based on code and optional suffix
def log_file(codice, suffix=None):
    logger = logging.getLogger('my_logger')
    if codice in log_messages:
        livello, messaggio = log_messages[codice]
        if suffix:
            messaggio = f"{messaggio} {suffix}"  # Append the suffix to the message
        extra = {'codice': codice}  # Add the code as an extra attribute
        if livello == 'DEBUG':
            logger.debug(messaggio, extra=extra)
        elif livello == 'INFO':
            logger.info(messaggio, extra=extra)
        elif livello == 'WARNING':
            logger.warning(messaggio, extra=extra)
        elif livello == 'SUCCESS':
            logger.success(messaggio, extra=extra)
        elif livello == 'CRITICAL':
            logger.critical(messaggio, extra=extra)
        else:
            logger.error(f'Livello non riconosciuto per il codice {codice}', extra=extra)
    else:
        logger.warning(f'Codice {codice} non riconosciuto.', extra={'codice': codice})
