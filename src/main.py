from io import TextIOWrapper
from instaloader import Instaloader, Profile, NodeIterator


PROFILO_LOGIN = ''
PROFILO_ANALISI = ''


def salva(followers_iterator: NodeIterator[Profile], followees_iterator: NodeIterator[Profile]) -> None:
    '''
    Metodo per salvare i followers ed i followees su due file, commentare la sua chiamata
    nella funzione main per non sovrascrivere i file
    '''
    with open('tempFile/'+PROFILO_ANALISI+'_followers.txt', 'w') as file:
        for followers in followers_iterator:
            file.write(followers.username + '\n')

    with open('tempFile/'+PROFILO_ANALISI+'_followees.txt', 'w') as file:
        for followees in followees_iterator:
            file.write(followees.username + '\n')

    print('Salvataggio riuscito')


def confronta(followers_iterator: NodeIterator[Profile], followees_iterator: NodeIterator[Profile],
              file_followers: TextIOWrapper, file_followees: TextIOWrapper) -> None:
    '''
    Metodo per effettuare il confronto tra gli ultimi follower e followees, salvati
    nei rispettivi file, e quelli recuperati a runtime
    '''
    old_followers_set = set()
    old_followees_set = set()
    set_followers = set()
    set_followees = set()
    for follower in followers_iterator:
        set_followers.add(follower.username)
    for followee in followees_iterator:
        set_followers.add(followee.username)

    for line in file_followers:
        old_followers_set.add(line)
    for line in file_followees:
        old_followees_set.add(line)

    diff_nuovi_followers = set_followers.difference(old_followers_set)
    diff_nuovi_followees = set_followees.difference(old_followees_set)
    diff_persi_followers = old_followers_set.difference(set_followers)
    diff_persi_followees = old_followees_set.difference(set_followees)

    print('Followers guadagnati: ')
    print(diff_nuovi_followers)
    print('Followers persi: ')
    print(diff_persi_followers)
    print('Followees guadagnati: ')
    print(diff_nuovi_followees)
    print('Followees persi: ')
    print(diff_nuovi_followees)
    print('Confronto effettuato')


def main() -> None:
    '''
    Metodo principale richiamato durante l'esecuzione dello script
    '''
    instaloader = Instaloader()
    # Recupero la sessione da un file creato in precedenza con l'esecuzione dello script fix_session.py
    instaloader.load_session_from_file('alessandro.scaccia_')
    # instaloader.login(user=PROFILO_LOGIN,passw='') # Deprecated: sconsigliato perche' rischio ban instagram
    print('*** LOGIN RIUSCITO con utente: ' + PROFILO_LOGIN)

    profile = Profile.from_username(instaloader.context, PROFILO_ANALISI)

    print('Recuperato profilo da analizzare: ' + profile.username)

    followers_iterator = profile.get_followers()
    followees_iterator = profile.get_followees()

    try:
        file_followers = open(
            'tempFile/'+PROFILO_ANALISI+'_followers.txt', 'r')
        file_followees = open(
            'tempFile/'+PROFILO_ANALISI+'_followees.txt', 'r')

        confronta(followers_iterator, followees_iterator,
                  file_followers, file_followees)

        file_followers.close()
        file_followees.close()
    except FileNotFoundError:
        print('Non ho trovato file con cui fare il confronto')
    except:
        print('Errore generico nel tentativo di confrontare con dati salvati')

    salva(followers_iterator, followees_iterator)


if __name__ == '__main__':
    main()
