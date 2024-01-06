from io import TextIOWrapper
from instaloader import Instaloader, Profile
import logging


PROFILO_LOGIN = ''
PROFILO_ANALISI = ''


def salva(followers_set: set, followees_set: set) -> None:
    '''
    Metodo per salvare i followers ed i followees su due file, commentare la sua chiamata
    nella funzione main per non sovrascrivere i file
    '''
    with open('tempFile/'+PROFILO_ANALISI+'_followers.txt', 'w') as file:
        for followers in followers_set:
            file.write(followers.username + '\n')

    with open('tempFile/'+PROFILO_ANALISI+'_followees.txt', 'w') as file:
        for followees in followees_set:
            file.write(followees.username + '\n')

    logging.info('Salvataggio riuscito')


def confronta(followers_set: set, followees_set: set,
              file_followers: TextIOWrapper, file_followees: TextIOWrapper) -> None:
    '''
    Metodo per effettuare il confronto tra gli ultimi follower e followees, salvati
    nei rispettivi file, e quelli recuperati a runtime
    '''
    old_followers_set = set()
    old_followees_set = set()

    for line in file_followers:
        old_followers_set.add(line.strip('\n'))
    for line in file_followees:
        old_followees_set.add(line.strip('\n'))

    set_followers_username = set()
    set_followees_username = set()

    for follower in followers_set:
        set_followers_username.add(follower.username)

    for followee in followees_set:
        set_followees_username.add(followee.username)

    diff_nuovi_followers = set_followers_username.difference(old_followers_set)
    diff_nuovi_followees = set_followees_username.difference(old_followees_set)
    diff_persi_followers = old_followers_set.difference(set_followers_username)
    diff_persi_followees = old_followees_set.difference(set_followees_username)

    logging.info("Informazioni per account: " + PROFILO_ANALISI)

    logging.info("Followers guadagnati: " + str(diff_nuovi_followers))
    logging.info("Followers persi: " + str(diff_persi_followers))
    logging.info("Followees guadagnati: " + str(diff_nuovi_followees))
    logging.info("Followees persi: " + str(diff_persi_followees))

    logging.debug("confronto terminato con successo")


def main() -> None:
    '''
    Metodo principale richiamato durante l'esecuzione dello script
    '''
    logging.basicConfig(filename="tempFile/logger.log", filemode="a",
                        format="%(asctime)s - %(levelname)s : %(message)s", level=logging.INFO)
    logging.debug("ho inizializzato il logger")
    instaloader = Instaloader()
    # Recupero la sessione da un file creato in precedenza con l'esecuzione dello script fix_session.py
    instaloader.load_session_from_file('alessandro.scaccia_')
    # instaloader.login(user=PROFILO_LOGIN,passw='') # Deprecated: sconsigliato perche' rischio ban instagram
    logging.debug('*** LOGIN RIUSCITO con utente: ' +
                  instaloader.context.username)

    profile = Profile.from_username(instaloader.context, PROFILO_ANALISI)
    logging.debug('ho recuperato il profilo: ' + profile.username)

    followers_set = set(profile.get_followers())
    followees_set = set(profile.get_followees())

    try:
        file_followers = open(
            'tempFile/'+PROFILO_ANALISI+'_followers.txt', 'r')
        file_followees = open(
            'tempFile/'+PROFILO_ANALISI+'_followees.txt', 'r')

        confronta(followers_set, followees_set,
                  file_followers, file_followees)

        file_followers.close()
        file_followees.close()
    except FileNotFoundError:
        logging.error('Non ho trovato file con cui fare il confronto')
    except:
        logging.error(
            'Errore generico nel tentativo di confrontare con dati salvati')

    salva(followers_set, followees_set)


if __name__ == '__main__':
    main()
