from dbconfig import DB

def translate(key, guild_id, balance=None, feedback=None, tries=None, number=None, winnings=None, giver=None,
              amount=None, receiver=None, color=None, time=None,
              bet=None, total=None, cards=None):
    translations = {
        "en": {
            "language_text": "English",
            "language_message": "You can choose your language!",
            "user_permissions_error": "You don't have the permissions to do that.",
            "daily_success": "Enjoy your free 500 coins!",
            "daily_error": "There was an error!",
            "daily_cooldown": f"This command is on cooldown. Please try again in {time}.",
            "balance": f"Your balance is {balance} coins.",
            "leaderboard_title": "Leaderboard",
            "place_positive_bet": "Please place a positive bet!",
            "guess_intro": f"Number Guessing Game\n\nI've chosen a number between 1 and 100. You have {tries} attempts to guess it.",
            "guess_correct": f"Congratulations! You guessed the number {number} correctly. You win {winnings} coins!",
            "insufficient_balance": "Insufficient balance!",
            "guess_wrong": f"{feedback} You have {tries} attempts remaining.",
            "guess_timeout": "Timeout! You took too long to respond. Game over!",
            "guess_game_over": f"Game Over. The number was {number}. Better luck next time!",
            "guess_feedback_too_low": "Too low!",
            "blackjack_intro": f"Welcome to Blackjack! Your bet is `{bet}` coins. Your balance is `{balance}` coins. Let's play!",
            "blackjack_your_hand": "Your hand: {cards} (Total: {total})",
            "blackjack_dealer_hand": "Dealer's hand: {cards} (Total: {total})",
            "blackjack_win": f"Congratulations! You win {winnings} coins with a total of {total}.",
            "blackjack_lose": f"You lose! The dealer's total was {total}. Better luck next time.",
            "blackjack_push": "It's a tie! Both you and the dealer have the same total.",
            "blackjack_busted": f"Busted! Your total of {total} exceeds 21. Game over.",
            "blackjack_dealer_busted": f"The dealer busted with a total of {total}! You win {winnings} coins.",
            "blackjack_hit_or_stand": "Would you like to **hit** (draw a card) or **stand** (keep your current hand)?",
            "blackjack_after_doubling": "After doubling down, your hand is: {cards} (Total: {total}).",
            "blackjack_dealer_now_playing": "The dealer is now playing their turn...",
            "blackjack_you_win": f"You win {winnings} coins! Great job!",
            "blackjack_congratulations": "Well played! You're on a winning streak!",
            "free_success": "You can have 250 free coins!",
            "free_rich": "You are rich, bro!",
            "slot_intro": '''You place a bet and spin a 3x3 grid filled with different symbols. Each symbol has a payout value, and some symbols are more likely to appear than others.

    If you get three matching symbols in a row, column, or diagonal, you win a payout based on the symbol's value. There's also a special symbol that can give a huge jackpot if it appears!

    **Those are the symbols with their multipliers:**''',
            "weekly_success": "Enjoy your free 50,000 coins!",
            "gift_success": f"{giver} gave {amount} to {receiver}!",
            "website": 'Visit our website: ',
            "gift_self_error": "You can't gift yourself!",
            "gift_bot_error": "Oops, don't give me money!",
            "gift_insufficient": "You don't have enough money.",
            "about": "Casino Bot brings virtual casino fun to your server with games, leaderboards, and bonuses!",
            "coinflip_win": f"Congratulations! You win {winnings} coins!",
            "coinflip_lose": "Almost! Try again?",
            "coinflip_invalid_prediction": "You should choose either 'heads' or 'tails'.",
            "roulette_win": f"You win! The number was {number} ({color}). You won {winnings} coins!",
            "roulette_lose": f"You lose! The number was {number} ({color}).",
            "roulette_invalid": "Please choose valid numbers for red/black.",
            "footer": "Casino by The Cantina | Claim your reward daily!",
            "command_list": """
    Casino Bot Command List:

    - **/daily**: Get free coins daily.\n\n
    - **/balance**: Check your balance.\n\n
    - **/leaderboard**: View the top players.\n\n
    - **/guess**: Play a number guessing game.\n\n
    - **/blackjack**: Play a game of Blackjack.\n\n
    - **/free**: Get 250 coins if your balance is zero.\n\n
    - **/slot**: Try your luck with the slot machine.\n\n
    - **/weekly**: Get 50,000 coins weekly.\n\n
    - **/gift**: Gift coins to another user.\n\n
    - **/about**: Learn about the bot.\n\n
    - **/coinflip**: Flip a coin to win coins.\n\n
    - **/roulette**: Bet on a color or number in roulette.\n\n
    - **/setlanguage**: Set your sever language\n\n
    """,
            "not_your_game": "This is not your game!",
            "vote_message": 'Click here to vote:\nhttps://discordbotlist.com/bots/crescendo\n\nGet 5000 coins for free daily!'
        },
        "es": {
            "language_text": "Espanol",
            "language_message": "¡Puedes elegir tu idioma!",
            "user_permissions_error": "No tienes los permisos para hacer eso.",
            "daily_success": "¡Disfruta de tus 500 monedas gratis!",
            "daily_error": "¡Hubo un error!",
            "daily_cooldown": f"Este comando está en enfriamiento. Por favor, inténtalo de nuevo en {time}.",
            "balance": f"Tu saldo es de {balance} monedas.",
            "leaderboard_title": "Tabla de clasificación",
            "place_positive_bet": "¡Por favor, haga una apuesta mayor a 0!",
            "guess_intro": f"Juego de adivinanza de números\n\nHe elegido un número entre 1 y 100. Tienes {tries} intentos para adivinarlo.",
            "guess_correct": f"¡Felicidades! Adivinaste el número {number} correctamente. ¡Ganas {winnings} monedas!",
            "guess_wrong": f"{feedback} Te quedan {tries} intentos.",
            "guess_timeout": "¡Tiempo agotado! Te tardaste demasiado en responder. ¡Juego terminado!",
            "guess_game_over": f"Juego terminado. El número era {number}. ¡Mejor suerte la próxima vez!",
            "guess_feedback_too_low": "¡Demasiado bajo!",
            "guess_feedback_too_high": "¡Demasiado alto!",
            "blackjack_intro": f"¡Bienvenido a Blackjack! Tu apuesta es de `{bet}` monedas. Tu saldo es de `{balance}` monedas. ¡Juguemos!",
            "blackjack_your_hand": "Tu mano: {cards} (Total: {total})",
            "blackjack_dealer_hand": "Mano del crupier: {cards} (Total: {total})",
            "blackjack_win": f"¡Felicidades! Ganaste {winnings} monedas con un total de {total}.",
            "blackjack_lose": f"Perdiste. El total del crupier fue {total}. Mejor suerte la próxima vez.",
            "blackjack_push": "¡Es un empate! Tanto tú como el crupier tienen el mismo total.",
            "blackjack_busted": f"Te pasaste. Tu total de {total} supera 21. Fin del juego.",
            "blackjack_dealer_busted": f"El crupier se pasó con un total de {total}. ¡Ganaste {winnings} monedas!",
            "blackjack_hit_or_stand": "¿Quieres **pedir** (tomar otra carta) o **plantarte** (quedarte con tu mano actual)?",
            "blackjack_after_doubling": "Después de doblar tu apuesta, tu mano es: {cards} (Total: {total}).",
            "blackjack_dealer_now_playing": "El crupier está jugando su turno...",
            "blackjack_you_win": f"¡Ganaste {winnings} monedas! ¡Buen trabajo!",
            "blackjack_congratulations": "¡Bien jugado! ¡Estás en racha!",
            "free_success": "¡Puedes tener 250 monedas gratis!",
            "free_rich": "¡Eres rico, amigo!",
            "slot_intro": '''Colocas una apuesta y giras una cuadrícula 3x3 llena de diferentes símbolos. Cada símbolo tiene un valor de pago, y algunos símbolos tienen más probabilidades de aparecer que otros.

    Si consigues tres símbolos coincidentes en una fila, columna o diagonal, ganarás un pago basado en el valor del símbolo. ¡También hay un símbolo especial que puede darte un gran bote si aparece!

    **Estos son los símbolos con sus multiplicadores:**''',
            "weekly_success": "¡Disfruta de tus 50,000 monedas gratis!",
            "gift_success": f"¡{giver} le dio {amount} a {receiver}!",
            "website": "Visite nuestro sitio web: ",
            "gift_self_error": "¡No puedes regalarte monedas a ti mismo!",
            "gift_bot_error": "¡Ups, no me des dinero!",
            "gift_insufficient": "No tienes suficiente dinero.",
            "about": "¡Casino Bot trae diversión de casino virtual a tu servidor con juegos, tablas de clasificación y bonificaciones!",
            "coinflip_win": f"¡Felicidades! Ganaste {winnings} monedas.",
            "coinflip_lose": "¡Casi! ¿Intentar otra vez?",
            "coinflip_invalid_prediction": "Debes elegir 'heads' o 'tails'.",
            "roulette_win": f"¡Ganaste! El número era {number} ({color}). Ganaste {winnings} monedas.",
            "roulette_lose": f"Perdiste. El número era {number} ({color}).",
            "roulette_invalid": "Por favor elige números válidos para red/black.",
            "footer": "Casino by The Cantina | ¡Reclama tu recompensa diariamente!",
            "command_list": """
    Lista de comandos de Casino Bot:

    - **/daily**: Obtén monedas gratis diariamente.\n\n
    - **/balance**: Revisa tu saldo.\n\n
    - **/leaderboard**: Ver los mejores jugadores.\n\n
    - **/guess**: Juega un juego de adivinanza de números.\n\n
    - **/blackjack**: Juega Blackjack.\n\n
    - **/free**: Obtén 250 monedas si tu saldo es cero.\n\n
    - **/slot**: Prueba suerte con las tragamonedas.\n\n
    - **/weekly**: Obtén 50,000 monedas semanalmente.\n\n
    - **/gift**: Regala monedas a otro usuario.\n\n
    - **/about**: Aprende sobre el bot.\n\n
    - **/coinflip**: Lanza una moneda para ganar monedas.\n\n
    - **/roulette**: Apuesta en un color o número en la ruleta.\n\n
    - **/set language**: Establezca el idioma de su servidor/l\n\n
    """,
            "not_your_game": "¡Este no es tu juego!",
            "vote_message": 'Haz clic aquí para votar:\nhttps://discordbotlist.com/bots/crescendo\n\n¡Obtén 5000 monedas gratis diariamente!'
        },
        "de": {
            "language_text": "Deutsch",
            "language_message": "Du kannst deine Sprache wählen!",
            "user_permissions_error": "Sie haben nicht die Berechtigung, das zu tun.",
            "daily_success": "Genieße deine 500 kostenlosen Münzen!",
            "daily_error": "Es gab einen Fehler!",
            "daily_cooldown": f"Dieser Befehl hat eine Abklingzeit. Bitte versuche es in {time} erneut.",
            "balance": f"Dein Kontostand beträgt {balance} Münzen.",
            "leaderboard_title": "Bestenliste",
            "place_positive_bet": "Möchte das Spiel über 0 hinauszögern!",
            "guess_intro": f"Zahlenraten-Spiel\n\nIch habe eine Zahl zwischen 1 und 100 gewählt. Du hast {tries} Versuche, sie zu erraten.",
            "guess_correct": f"Herzlichen Glückwunsch! Du hast die Zahl {number} richtig erraten. Du gewinnst {winnings} Münzen!",
            "guess_wrong": f"{feedback} Du hast noch {tries} Versuche übrig.",
            "guess_timeout": "Zeit abgelaufen! Du hast zu lange gebraucht, um zu antworten. Spiel vorbei!",
            "guess_game_over": f"Spiel beendet. Die Zahl war {number}. Viel Glück beim nächsten Mal!",
            "guess_feedback_too_low": "Zu niedrig!",
            "guess_feedback_too_high": "Zu hoch!",
            "blackjack_intro": f"Willkommen bei Blackjack! Dein Einsatz beträgt `{bet}` Münzen. Dein Guthaben ist `{balance}` Münzen. Viel Glück!",
            "blackjack_your_hand": "Deine Hand: {cards} (Gesamt: {total})",
            "blackjack_dealer_hand": "Hand des Dealers: {cards} (Gesamt: {total})",
            "blackjack_win": f"Herzlichen Glückwunsch! Du gewinnst {winnings} Münzen mit einem Gesamtwert von {total}.",
            "blackjack_lose": f"Du verlierst. Der Gesamtwert des Dealers war {total}. Viel Glück beim nächsten Mal.",
            "blackjack_push": "Es ist ein Unentschieden! Sowohl du als auch der Dealer haben den gleichen Gesamtwert.",
            "blackjack_busted": f"Überkauft! Dein Gesamtwert von {total} übersteigt 21. Spiel vorbei.",
            "blackjack_dealer_busted": f"Der Dealer hat sich überkauft mit einem Gesamtwert von {total}. Du gewinnst {winnings} Münzen!",
            "blackjack_hit_or_stand": "Möchtest du **ziehen** (eine weitere Karte) oder **stehen bleiben** (mit deiner aktuellen Hand weitermachen)?",
            "blackjack_after_doubling": "Nach dem Verdoppeln beträgt deine Hand: {cards} (Gesamt: {total}).",
            "blackjack_dealer_now_playing": "Der Dealer spielt jetzt seine Runde...",
            "blackjack_you_win": f"Du gewinnst {winnings} Münzen! Herzlichen Glückwunsch!",
            "blackjack_congratulations": "Gut gespielt! Du bist auf einer Gewinnsträhne!",
            "free_success": "Du kannst 250 kostenlose Münzen erhalten!",
            "free_rich": "Du bist reich, mein Freund!",
            "slot_intro": '''Du platzierst eine Wette und drehst ein 3x3 Raster mit verschiedenen Symbolen. Jedes Symbol hat einen Auszahlungspreis, und einige Symbole erscheinen häufiger als andere.

    Wenn du drei übereinstimmende Symbole in einer Reihe, Spalte oder Diagonale erhältst, gewinnst du einen Auszahlungspreis basierend auf dem Wert des Symbols. Es gibt auch ein spezielles Symbol, das dir einen riesigen Jackpot einbringen kann, wenn es erscheint!

    **Dies sind die Symbole mit ihren Multiplikatoren:**''',
            "weekly_success": "Genieße deine 50.000 kostenlosen Münzen!",
            "gift_success": f"{giver} gab {amount} an {receiver}!",
            "website": 'Besuchen Sie unsere Website: ',
            "gift_self_error": "Du kannst dir selbst keine Münzen schenken!",
            "gift_bot_error": "Ups, gib mir kein Geld!",
            "gift_insufficient": "Du hast nicht genug Geld.",
            "about": "Casino Bot bringt virtuelles Casino-Spaß auf deinen Server mit Spielen, Bestenlisten und Boni!",
            "coinflip_win": f"Herzlichen Glückwunsch! Du gewinnst {winnings} Münzen!",
            "coinflip_lose": "Fast! Versuch es nochmal?",
            "coinflip_invalid_prediction": "Du solltest entweder 'heads' oder 'tails' wählen.",
            "roulette_win": f"Du gewinnst! Die Zahl war {number} ({color}). Du hast {winnings} Münzen gewonnen!",
            "roulette_lose": f"Du verlierst! Die Zahl war {number} ({color}).",
            "roulette_invalid": "Bitte wähle gültige Zahlen für red/black.",
            "footer": "Casino von The Cantina | Fordere dein tägliches Geschenk ein!",
            "command_list": """
    Casino Bot Command List:

    - **/daily**: Tägliche Münzen erhalten.\n\n
    - **/balance**: Deinen Kontostand überprüfen.\n\n
    - **/leaderboard**: Zeige die besten Spieler.\n\n
    - **/guess**: Spiele ein Zahlenraten-Spiel.\n\n
    - **/blackjack**: Spiele Blackjack.\n\n
    - **/free**: Bekomme 250 Münzen, wenn dein Kontostand 0 ist.\n\n
    - **/slot**: Versuche dein Glück bei den Spielautomaten.\n\n
    - **/weekly**: Bekomme wöchentliche 50.000 Münzen.\n\n
    - **/gift**: Verschenke Münzen an einen anderen Benutzer.\n\n
    - **/about**: Lerne den Bot kennen.\n\n
    - **/coinflip**: Wirf eine Münze, um Münzen zu gewinnen.\n\n
    - **/roulette**: Wette auf eine Farbe oder Zahl in der Roulette.\n\n
    - **/set language**: Stelle deine Serversprache einund\n\n
    """,
            "not_your_game": "Das ist nicht dein Spiel!",
            "vote_message": 'Klicken Sie hier, um abzustimmen:\nhttps://discordbotlist.com/bots/crescendo\n\nErhalten Sie täglich 5000 Münzen kostenlos!'
        },
        "bg": {
            "language_text" : "Български",
            "language_message": "Можете да изберете вашия език!",
            "user_permissions_error": "Нямате нужните правомощия за да използвате тази команда!",
            "daily_success": "Наслаждавайте се на вашите 500 безплатни монети!",
            "daily_error": "Имаше грешка!",
            "daily_cooldown": f"Тази команда е в режим на охлаждане. Моля, опитайте отново след {time}.",
            "balance": f"Балансът ви е {balance} монети.",
            "leaderboard_title": "Таблица с резултати",
            "place_positive_bet": "Моля, поставете положителна залог!",
            "guess_intro": f"Игра за отгатване на числа\n\nИзбрал съм число между 1 и 100. Имате {tries} опита да го познаете.",
            "guess_correct": f"Поздравления! Познахте числото {number} правилно. Печелите {winnings} монети!",
            "guess_wrong": f"{feedback} Остават ви {tries} опита.",
            "guess_timeout": "Изтече времето! Задержали сте твърде дълго за отговор. Играта е приключила!",
            "guess_game_over": f"Играта приключи. Числото беше {number}. Повече късмет следващия път!",
            "guess_feedback_too_low": "Твърде ниско!",
            "guess_feedback_too_high": "Твърде високо!",
            "blackjack_intro": f"Добре дошли в Блекджек! Вашият залог е `{bet}` монети. Вашият баланс е `{balance}` монети. Успех!",
            "blackjack_your_hand": "Вашата ръка: {cards} (Общо: {total})",
            "blackjack_dealer_hand": "Ръката на дилъра: {cards} (Общо: {total})",
            "blackjack_win": f"Поздравления! Печелите {winnings} монети с обща стойност от {total}.",
            "blackjack_lose": f"Губите. Общата стойност на дилъра беше {total}. Успех следващия път.",
            "blackjack_push": "Равенство! И вие, и дилърът имате една и съща обща стойност.",
            "blackjack_busted": f"Прехвърлихте 21! Вашата обща стойност от {total} надвишава 21. Играта приключи.",
            "blackjack_dealer_busted": f"Дилърът прехвърли 21 с обща стойност от {total}. Печелите {winnings} монети!",
            "blackjack_hit_or_stand": "Искате ли **още една карта** (да теглите) или **да останете** (да продължите с настоящата си ръка)?",
            "blackjack_after_doubling": "След удвояване вашата ръка е: {cards} (Общо: {total}).",
            "blackjack_you_win": f"Печелите {winnings} монети! Поздравления!",
            "blackjack_congratulations": "Добре изиграно! Вие сте в серия от победи!",
            "free_success": "Можете да получите 250 безплатни монети!",
            "free_rich": "Богат сте, приятелю!",
            "slot_intro": '''Залагате и въртите 3x3 мрежа, пълна с различни символи. Всеки символ има стойност на изплащане, а някои символи се появяват по-често от други.

    Ако получите три съвпадащи символа в ред, колона или диагонал, ще спечелите изплащане въз основа на стойността на символа. Има и специален символ, който може да ви донесе огромен джакпот, ако се появи!

    **Ето символите със техните множители:**''',
            "weekly_success": "Наслаждавайте се на вашите 50 000 безплатни монети!",
            "gift_success": f"{giver} даде {amount} на {receiver}!",
            "website": 'Посетете нашия уебсайт: ',
            "gift_self_error": "Не можете да подарите себе си!",
            "gift_bot_error": "Ооо, не ми давайте пари!",
            "gift_insufficient": "Нямате достатъчно пари.",
            "about": "Casino Bot носи виртуално казино забавление на вашия сървър с игри, таблици с резултати и бонуси!",
            "coinflip_win": f"Поздравления! Печелите {winnings} монети!",
            "coinflip_lose": "Точно така! Опитайте отново?",
            "coinflip_invalid_prediction": "Трябва да изберете 'heads' или 'tails'.",
            "roulette_win": f"Печелите! Числото беше {number} ({color}). Спечелихте {winnings} монети!",
            "roulette_lose": f"Загубихте! Числото беше {number} ({color}).",
            "roulette_invalid": "Моля, изберете валидни числа за red/black.",
            "footer": "Casino от The Cantina | Вземете своята награда всеки ден!",
            "command_list": """
    Списък на командите на Casino Bot:

    - **/daily**: Получете безплатни монети ежедневно.\n\n
    - **/balance**: Проверете вашия баланс.\n\n
    - **/leaderboard**: Прегледайте най-добрите играчи.\n\n
    - **/guess**: Играйте игра за отгатване на число.\n\n
    - **/blackjack**: Играйте Blackjack.\n\n
    - **/free**: Получете 250 монети ако балансът ви е нула.\n\n
    - **/slot**: Опитайте вашето късметче със слот машината.\n\n
    - **/weekly**: Получете 50 000 монети ежеседмично.\n\n
    - **/gift**: Подарете монети на друг потребител.\n\n
    - **/about**: Научете повече за бота.\n\n
    - **/coinflip**: Хвърлете монета, за да спечелите монети.\n\n
    - **/roulette**: Залагайте на цвят или число в рулетка.\n\n
    - **/setlanguage**: Задайте езика на сървъра си!\n\n

    """,
            "not_your_game": "Това не е твоята игра!",
            "blackjack_dealer_now_playing": "Дилърът сега играе своята ръка.",
            "vote_message": 'Натисни тук за да гласуваш:\nhttps://discordbotlist.com/bots/crescendo\n\n5000 монети ежедневно!'
        }
    }

    if key == 'get_all':
        return translations
    db = DB()

    language = db.get_current_guild_language(guild_id)
    language_translations = translations.get(language, translations['en'])

    try:
        translation = language_translations[key]
    except KeyError:
        return f'Translation not found for {key}!'

    if isinstance(translation,
                  str) and '{' in translation:
        translation = translation.format(
            balance=balance,
            time=time,
            tries=tries,
            number=number,
            winnings=winnings,
            giver=giver,
            amount=amount,
            receiver=receiver,
            color=color,
            bet=bet,
            feedback=feedback,
            total=total,
            cards=cards
        )

    return translation
