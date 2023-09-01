import argparse
import configparser

"""
parte per i comandi da shell
parte per leggere e scrivere la configurazione del client
"""


def parser_command_definizione():
    """
    Funzione che definisce i comandi da terminale
    """
    parser = argparse.ArgumentParser(
        description='client mqtt: legge da csv e pubblica su mqtt una stringa in formato json')
    parser.add_argument("-file",
                        type=str,
                        dest='csv_file',
                        help='file sorgente csv')
    parser.add_argument("-int",
                        "-intervallo",
                        type=int,
                        dest='secondi',
                        help='intervallo di tempo IN SECONDI tra ogni invio')
    parser.add_argument("-inizio",
                        type=int,
                        dest='inizio',
                        help="numero di elementi da scartare all'inizio")
    parser.add_argument("-host",
                        type=str,
                        dest='host',
                        help='IP o dns del server mqtt')
    parser.add_argument("-topic",
                        type=str,
                        dest='topic',
                        help='nome del topic su mqtt')
    return parser


def config_crea(file: str):
    """
    Funzione per creare il file con i valori di default
    :param file: file in cui scrivere
    :return:
    """
    configurazione = configparser.ConfigParser()
    configurazione.add_section('Default')
    configurazione['Default']['csv_file'] = 'Input.csv'
    configurazione['Default']['attesa_secondi'] = '900'
    configurazione['Default']['inizio'] = '0'
    configurazione['Default']['log_file'] = 'log.json'
    configurazione['Default']['host'] = 'localhost'
    configurazione['Default']['porta'] = '1883'
    configurazione['Default']['login'] = 'False'
    configurazione['Default']['username'] = ''
    configurazione['Default']['password'] = ''
    configurazione['Default']['topic'] = 'sensori'
    configurazione['Default']['cert_tls'] = ''
    with open(file, 'w') as configfile:
        configurazione.write(configfile)


class ParserConfig:
    def __init__(self, file: str):
        self.dizionario = {"csv_file": "",
                           "attesa_secondi": "",
                           "inizio": "",
                           "log_file": "",
                           "host": "",
                           "porta": "",
                           "login": "",
                           "username": "",
                           "password": "",
                           "topic": "",
                           "cert_tls": ""
                           }
        self.file = file

    def config_leggi(self):
        """
        Funzione lettura del file di configurazione
        """
        config = configparser.ConfigParser()
        config.read(self.file)
        self.dizionario.update({"csv_file": config['Default']['csv_file']})
        self.dizionario.update({"attesa_secondi": config['Default']['attesa_secondi']})
        self.dizionario.update({"inizio": config['Default']['inizio']})
        self.dizionario.update({"log_file": config['Default']['log_file']})
        self.dizionario.update({"host": config['Default']['host']})
        self.dizionario.update({"porta": config['Default']['porta']})
        self.dizionario.update({"login": config['Default']['login']})
        self.dizionario.update({"username": config['Default']['username']})
        self.dizionario.update({"password": config['Default']['password']})
        self.dizionario.update({"topic": config['Default']['topic']})
        self.dizionario.update({"cert_tls": config['Default']['cert_tls']})

    def config_terminale(self, args):
        """
        Funzione lettura comandi da terminale
        :param args: linea di comando
        :return:
        """
        '''
        print('file= {}\nintervallo= {} secondi\nhost= {}\ntopic= {}'.format(
                ARGS.csv_file,ARGS.secondi,ARGS.host,ARGS.topic)
            )
        '''
        # file sorgente in csv
        if args.csv_file is not None:
            self.dizionario.update({"csv_file": args.csv_file})
        # tempo di intervallo per ogni invio
        # SEMPRE IN SECONDI
        if args.secondi is not None:
            self.dizionario.update({"attesa_secondi": args.secondi})
        # messaggio da cui partire
        # UN NUMERO INTERO
        if args.inizio is not None:
            self.dizionario.update({"numero_messaggio": args.inizio})
        # indirizzo a qui inviare
        if args.host is not None:
            self.dizionario.update({"host": args.host})
        # nome del topic
        if args.topic is not None:
            self.dizionario.update({"topic": args.topic})

    def get_csv_file(self):
        return self.dizionario.get('csv_file')

    def get_secondi(self):
        return int(self.dizionario.get('attesa_secondi'))

    def get_inizio(self):
        return int(self.dizionario.get('inizio'))

    def get_log_file(self):
        return self.dizionario.get('log_file')

    def get_host(self):
        return self.dizionario.get('host')

    def get_porta(self):
        return int(self.dizionario.get('porta'))

    def get_login(self):
        return bool(self.dizionario.get('login'))

    def get_username(self):
        return self.dizionario.get('username')

    def get_password(self):
        return self.dizionario.get('password')

    def get_topic(self):
        return self.dizionario.get('topic')

    def get_cert_tls(self):
        return self.dizionario.get('cert_tls')
