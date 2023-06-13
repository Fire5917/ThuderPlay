import discord
from discord.ext import commands
import asyncio
import random
import requests
import instaloader
from googlesearch import search
import os, csv
import difflib



client = commands.Bot(command_prefix="?", intents=discord.Intents.all())


message = ""
nbr_de_site_trouve = 0

def check_url(debut_url, pseudo, fin_url, nom):
    global message
    global nbr_de_site_trouve
    url = f"{debut_url}{pseudo}{fin_url}"
    response = requests.get(url)
    if response.status_code == 200:
        message = message +  f"\n[+] {nom}"
        nbr_de_site_trouve += 1
        print(f"[+] {nom}")
    else:
        print(f"[-] {nom}")


def search_internet(query, number_of_result):
    results = []
    
    # Effectuer la recherche
    for result in search(query, number_of_result):
        results.append(result)
    
    return results






url_liste = [["https://tiktok.com/@", "", "TikTok"], 
             ["https://www.snapchat.com/add/", "", "Snapchat"], 
             ["https://api.mojang.com/users/profiles/minecraft/", "", "Minecraft"],
             ["https://pornhub.com/users/", "", "Pornhub [NSFW]"],
             ["https://xhamster.com/creators/", "", "Xhamster [NSFW]"],
             ["https://youporn.com/uservids/", "", "YouPorn [NSFW]"],
             ["https://about.me/", "", "About.ME"],
             ["https://community.brave.com/u/", "", "Brave Community"],
             ["https://github.com/", "", "Github"],
             ["https://www.xvideos.com/amateur-channels/", "", "Xvideos Amateur [NSFW]"],
             ["https://www.xvideos.com/channels/", "", "Xvideos Channel [NSFW]"]]








bluff_players = []  # Liste des joueurs participant au jeu de bluff
bluff_impostor = None  # Joueur qui est l'imposteur
words = ["abricot", "abeille", "acrobate", "aéroport", "alchimiste", "alligator", "amiral", "ananas", "araignée", "arc-en-ciel", "astronaute", "autruche", "aventurier", "baguette", "banane", "barbecue", "biscuit", "bouteille", "bulle", "caméléon", "canard", "capitaine", "cascade", "chameau", "champignon", "chanteur", "chat", "château", "chaussure", "chocolat", "chouette", "clown", "cochon", "coiffeur", "comédien", "compas", "cordonnier", "corbeau", "couronne", "crayon", "crocodile", "cycliste", "danseur", "diamant", "dindon", "dompteur", "dragon", "éléphant", "épée", "escargot", "explorateur", "fakir", "feuille", "flamant", "fleur", "fusée", "girafe", "gondolier", "gorille", "guitare", "hélicoptère", "hippopotame", "horloge", "île", "jongleur", "kangourou", "ketchup", "labyrinthe", "lait", "lampe", "lion", "loup", "magicien", "maison", "marteau", "méduse", "mélodie", "métro", "miroir", "montagne", "narval", "navire", "nuage", "oiseau", "or", "orchidée", "ours", "palmier", "papillon", "parapluie", "pêche", "penguin", "piano", "pilote", "pingouin", "pirate", "poisson", "pomme", "pont", "princesse", "pyramide", "raton-laveur", "renard", "requin", "rhinocéros", "robot", "rocher", "rouge-gorge", "ruban", "singe", "sirène", "sorcière", "soleil", "souris", "stade", "super-héros", "tambour", "tigre", "tortue", "train", "trésor", "tricycle", "trompette", "uniforme", "vache", "vampire", "violon", "volcan", "zèbre", "zombie", "Antarctique", "Arctique", "Australie", "Brésil", "Canada", "Chine", "Egypte", "France", "Groenland", "Hollywood", "Inde", "Irlande", "Italie", "Japon", "Kenya", "Liban", "Londres", "Madagascar", "Mexique", "Moscou", "Nouvelle-Zélande", "Paris", "Pôle Nord", "Pôle Sud", "Rio de Janeiro", "Rome", "Sahara", "Sibérie", "Sydney", "Tokyo", "Amazonie", "Everest", "Grand Canyon", "Mont Fuji", "Niagara", "Taj Mahal", "Tour Eiffel", "Victoria Falls", "Wall Street", "bureau", "café", "cinéma", "école", "église", "forêt", "hôpital", "île", "magasin", "parc", "piscine", "plage", "restaurant", "route", "supermarché", "théâtre", "train", "université", "zoo", "Barack Obama", "Beyoncé", "Bruce Lee", "Cristiano Ronaldo", "Donald Trump", "Elon Musk", "Emma Watson", "Freddie Mercury", "Gandhi", "Harry Potter", "Iron Man", "Jack Sparrow", "James Bond", "John Lennon", "Lionel Messi", "Marilyn Monroe", "Michael Jackson", "Mickey Mouse", "Napoleon Bonaparte", "Naruto", "Pikachu", "Sherlock Holmes", "Spider-Man", "Superman", "Voldemort", "Wonder Woman", "Yoda", "Aladdin", "Alice (Alice au pays des merveilles)", "Batman", "Buzz l'Éclair", "Captain America", "Darth Vader", "Dora l'exploratrice", "Flash McQueen", "Goku", "Hulk", "Iron Fist", "Joker", "Lara Croft", "Luke Skywalker", "Mario", "Minnie Mouse", "Mulder (X-Files)", "Nemo", "Obi-Wan Kenobi", "Pocahontas", "Ratatouille", "Robocop", "Sailor Moon", "Sonic", "Spartacus", "SpongeBob", "Tintin", "Thor", "Totoro", "Winnie l'ourson", "Yoda", "Zorro", "Avatar", "Avengers", "Breaking Bad", "Friends", "Game of Thrones", "Harry Potter", "Indiana Jones", "La Reine des neiges", "Le Seigneur des anneaux", "Matrix", "Pirates des Caraïbes", "Star Wars", "The Big Bang Theory", "The Walking Dead", "Titanic", "Toy Story", "Twilight", "X-Men"]
@client.event
async def on_ready():
    print('Le bot est prêt')
    await client.change_presence(activity=discord.Game(name="?osint | ?ask | ?pendu - Just Better - Une envie de faire une bonne action? --> ?bonnes_actions"))

@client.event
async def on_message(message):
    print(f"[{message.author}] (#{message.channel.name if message.guild is not None else 'MP'}) >>>  {message.content}\n")
    await client.process_commands(message)

@client.command()
async def bluff(ctx):
    # 1) envoyer un message avec une réaction que le bot a mis dessus (dans le message le bot dit de réagir au message avec la meme réaction que lui pour participer au jeu).
    emoji = "👍" # choisir l'emoji que vous voulez
    message = await ctx.send(f"Réagissez avec {emoji} pour participer au jeu du bluff ! Vous avez 15 secondes.")
    await message.add_reaction(emoji)

    # 2) 60 secondes plus tard le bot envoie la liste des joueurs dans le même salon textuel.
    await asyncio.sleep(15)
    message = await ctx.channel.fetch_message(message.id)
    players = []
    for reaction in message.reactions:
        if reaction.emoji == emoji:
            async for user in reaction.users():
                if user != client.user:
                    players.append(user)
    if len(players) < 2:
        await ctx.send("Il n'y a pas assez de joueurs pour commencer le jeu.")
        return
    else:
        await ctx.send(f"Les joueurs sont : {', '.join([player.mention for player in players])}")

    # 3) Ensuite le bot explique le jeu (en gros le jeu c'est que le bot envoie en MP aux personnes (sauf à une ou 2 personnes en fonction du nombre de joueur) un mot. Touts les joueurs doivent dire en MP au bot un mot pour décrire le mot envoyé par le bot. (Les joueurs n'ayant pas le mot recevront les mots répondus par les autres et diront alors un mot au bot (ils doivent bluffés). Ensuite les joueurs voteront pour un joueur qu'il pensent être l'imposteur.
    await ctx.send("Le jeu du bluff commence ! Le but est de trouver l'imposteur parmi les joueurs. Le bot va envoyer un mot en MP à tous les joueurs sauf à un ou deux qui seront les imposteurs. Les joueurs devront alors envoyer un mot au bot pour décrire le mot reçu. Les imposteurs recevront ensuite les mots des autres joueurs et devront envoyer un mot au bot pour essayer de bluffer. Ensuite, les joueurs voteront pour celui qu'ils pensent être l'imposteur. Si l'imposteur est découvert, les non-imposteurs gagnent, sinon l'imposteur gagne.")

    # 4) Ensuite tu envoie aux joueurs le mot (aléatoire) sauf à un joueur auquel tu envoie ("Tu es l'imposteur)

    word = random.choice(words)
    impostors = random.sample(players, k=max(1, len(players)//5)) # choisir le nombre d'imposteurs
    for player in players:
        if player in impostors:
            await player.send("Tu es l'imposteur !")
        else:
            await player.send(f"Le mot est : {word}; envoyer un mot qui peut faire penser à ce mot, mais attention, il ne faut pas que l'imposteur arrive à trouver le mot d'origine!")

    # 5) Les joueurs ont 30 secondes pour répondre au bot en MP
    await ctx.send("Vous avez 20 secondes pour envoyer un mot au bot en MP.")
    await asyncio.sleep(20)

    # 6) Ensuite tu envoie les mots récupérer à l'imposteur.
    clues = {}
    for player in players:
        if player not in impostors:
            dm = await player.create_dm()
            message = await discord.utils.get(dm.history(limit=1))
            if message.author == player:
                clues[player] = message.content
    for impostor in impostors:
        await impostor.send(f"Les mots des autres joueurs sont : {', '.join(clues.values())}")

    # 7) Après 30 secondes tu envoie dans le salon textuel ou le jeu a été lancé les mots de chaques joueur (pas en anonyme).
    await ctx.send("Vous avez 20 secondes pour envoyer un mot au bot en MP.")
    await asyncio.sleep(20)
    for impostor in impostors:
        dm = await impostor.create_dm()
        message = await discord.utils.get(dm.history(limit=1))
        if message.author == impostor:
            clues[impostor] = message.content
    await ctx.send(f"Les mots de chaque joueur sont : {', '.join([f'{player.mention} : {clue}' for player, clue in clues.items()])}")

    # 8) Ensuite tu enverra un message avec la liste des joueurs à coté de leurs numéros.
    numbers = {}
    for i, player in enumerate(players, start=1):
        numbers[i] = player
    await ctx.send(f"Les numéros de chaque joueur sont : {', '.join([f'{i} : {player.mention}' for i, player in numbers.items()])}")

    # 9) TU demandera au joueur le numéro de la personne pour qui ils votent
    await ctx.send("Vous avez 60 secondes pour voter pour le numéro de la personne que vous pensez être l'imposteur. Envoyez votre vote au bot en MP. Vous pouvez débattre dans ce salon pendant ce temps...")
    await asyncio.sleep(60)

    # 10) Tu dira quel joueur a été choisi (le plus voté)
    votes = {}
    for player in players:
        dm = await player.create_dm()
        message = await discord.utils.get(dm.history(limit=1))
        if message.author == player:
            try:
                vote = int(message.content)
                if vote in numbers:
                    votes[player] = numbers[vote]
            except ValueError:
                pass
    counts = {}
    for vote in votes.values():
        counts[vote] = counts.get(vote, 0) + 1
    if counts:
        chosen = max(counts, key=counts.get)
        await ctx.send(f"Le joueur le plus voté est : {chosen.mention} avec {counts[chosen]} votes.")
    else:
        await ctx.send("Aucun vote n'a été enregistré.")

    # 11) Ensuite tu dit si les non imposteurs ont gagnés ou perdu (si l'imposteur est la personne la plus voté alors ils ont gagnés sinon ils ont perdu)
    if chosen in impostors:
        await ctx.send("Bravo ! Vous avez trouvé l'imposteur ! Les non-imposteurs ont gagné !")
    else:
        await ctx.send("Dommage ! Vous vous êtes trompés ! L'imposteur a gagné !")
    await ctx.send(f"Les imposteurs étaient : {', '.join([impostor.mention for impostor in impostors])}")

    
@client.command()
async def loto(ctx):
    # Le bot envoie un message permettant de participé au jeu
    bot_message = await ctx.send("Cliquez sur la même réaction que moi pour participer au loto !")
    emoji = "🍀" # Choisir l'émoji trèfle à quatre feuilles
    await bot_message.add_reaction(emoji) # Ajouter la réaction au message du bot


    # Le bot récupère les participants après 15 secondes
    await asyncio.sleep(15) # Attendre 15 secondes
    participants = [] # Créer une liste vide pour stocker les participants
    cache_msg = discord.utils.get(client.cached_messages, id=bot_message.id) # Récupérer le message du bot depuis le cache
    for reaction in cache_msg.reactions: # Parcourir les réactions du message
        if reaction.emoji == emoji: # Si la réaction est la même que celle du bot
            async for user in reaction.users(): # Parcourir les utilisateurs qui ont réagi
                if user != client.user and user not in participants: # Si l'utilisateur n'est pas le bot ni déjà dans la liste des participants
                    participants.append(user) # Ajouter l'utilisateur à la liste des participants

    # Le bot demande alors en mp aux joueurs les numéros qu'ils ont choisis
    for user in participants: # Parcourir les participants
        await user.send(f"Bonjour {user.name}, vous avez participé au loto ! Veuillez me donner vos numéros sous cette forme : chiffre1, chiffre2, chiffre3, chiffre4, chiffre5 , nombre_chance") # Envoyer un message privé à chaque participant

    # Le bot récupère les numéros de tout les participants après 45 secondes
    await asyncio.sleep(45) # Attendre 45 secondes
    numeros = {} # Créer un dictionnaire vide pour stocker les numéros de chaque participant
    for user in participants: # Parcourir les participants
        async for message in user.history(limit=1): # Récupérer le dernier message privé de chaque participant
            try:
                choix = [int(x) for x in message.content.split(",")] # Convertir le message en une liste d'entiers
                assert len(choix) == 6 # Vérifier que la liste contient 6 éléments
                assert all(1 <= x <= 49 for x in choix[:5]) # Vérifier que les 5 premiers éléments sont entre 1 et 49
                assert 1 <= choix[5] <= 9 # Vérifier que le dernier élément est entre 1 et 9
                numeros[user] = choix # Ajouter le choix au dictionnaire avec l'utilisateur comme clé
            except:
                await user.send("Désolé, votre réponse n'est pas valide. Vous ne pouvez pas participer au tirage.") # Envoyer un message d'erreur si le choix n'est pas valide

    # Le bot simule un tirage dans le salon où a été envoyé la commande
    tirage = random.sample(range(1,50), 5) + [random.randint(1,9)] # Générer une liste de 6 nombres aléatoires
    await ctx.send(f"Le tirage est : {', '.join(str(x) for x in tirage)}") # Envoyer le tirage dans le salon

    # Le bot fait alors un classement des joueurs ayant le plus de numéros en commun
    classement = [] # Créer une liste vide pour stocker le classement
    for user, choix in numeros.items(): # Parcourir le dictionnaire des numéros
        communs = len(set(choix) & set(tirage)) # Calculer le nombre de numéros en commun
        if communs == 6: # Si 6 numéros en commun
            gain = 1000000 # Le gain est de 1 million d'euros
        elif communs == 5: # Si 5 numéros en commun
            gain = 1000 # Le gain est de 1000 euros
        elif communs == 4: # Si 4 numéros en commun
            gain = 100 # Le gain est de 100 euros
        elif communs == 3: # Si 3 numéros en commun
            gain = 10.5 # Le gain est de 10.5 euros
        elif communs == 2: # Si 2 numéros en commun
            gain = 5.2 # Le gain est de 5.2 euros
        elif communs == 1: # Si 1 numéro en commun
            gain = 0 # Le gain est de 0 euro
        else: # Si aucun numéro en commun
            gain = -2.2 # Le gain est de -2.2 euros
        classement.append((user, choix, communs, gain)) # Ajouter un tuple avec l'utilisateur, son choix, le nombre de numéros en commun et le gain à la liste du classement

    classement.sort(key=lambda x: x[3], reverse=True) # Trier la liste du classement par ordre décroissant de gain

    # Le bot met dans le classement le résultat de tout le monde en argent
    resultat = "" # Créer une chaîne vide pour stocker le résultat
    for user, choix, communs, gain in classement: # Parcourir la liste du classement
        resultat += f"{user.name} a choisi {', '.join(str(x) for x in choix)} et a {communs} numéro(s) en commun. Il gagne {gain} euros.\n" # Ajouter une ligne au résultat avec le nom, le choix, le nombre de numéros en commun et le gain de chaque participant

    # Le bot envoie le résultat de chaque joueur au joueur même à la fin du tirage
    for user in participants: # Parcourir les participants
        await user.send(resultat) # Envoyer le résultat en message privé à chaque participant
    
@client.command()
async def pendu(ctx, essais: int = 6):
    if essais <= 0:
        await ctx.send("Le nombre d'essais doit être supérieur à zéro.")
        return

    mot_choisi = random.choice(words).lower()
    lettres_trouvees = []

    mot_masque = ""
    for char in mot_choisi:
        if char == " ":
            mot_masque += " "
            lettres_trouvees.append(" ")  # Marquer les espaces comme déjà trouvés
        else:
            mot_masque += "_"

    message = await ctx.send(f"Le mot à deviner contient {len(mot_choisi)} lettres : `{mot_masque}`\n\nLettres déjà essayées : `{', '.join(lettres_trouvees)}`\nEssais restants : `{essais}`")

    while essais > 0:
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        try:
            response = await client.wait_for("message", check=check, timeout=60)  # Attend la réponse de l'utilisateur pendant 60 secondes
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé, la partie est terminée.")
            return

        lettre = response.content.lower()

        await response.delete()  # Supprime le message de l'utilisateur

        if lettre in lettres_trouvees:
            await ctx.send("Cette lettre a déjà été essayée.")
            continue

        lettres_trouvees.append(lettre)

        mot_masque_temp = ""
        for i, char in enumerate(mot_choisi):
            if char in lettres_trouvees or (char in ["e", "é", "è", "ê"] and lettre == "e") or (char in ["u", "ù", "û"] and lettre == "u") or (char in ["o", "ô"] and lettre == "o"):
                mot_masque_temp += char
            else:
                mot_masque_temp += "_"

        if mot_masque_temp == mot_masque:
            essais -= 1
        else:
            mot_masque = mot_masque_temp

        await message.edit(content=f"```\n{mot_masque}\n\nLettres déjà essayées : {', '.join(lettres_trouvees)}\nEssais restants : {essais}\n```")

        if "_" not in mot_masque:
            await ctx.send("Félicitations, vous avez trouvé le mot !")
            return

    await ctx.send(f"Dommage, vous avez épuisé tous vos essais. Le mot était : {mot_choisi}")
    
    






@client.command()
async def osint(ctx, pseudo):
    global message
    global nbr_de_site_trouve
    message = ""
    nbr_de_site_trouve = 0
    await ctx.send(f":timer: Recherche commencée pour {pseudo}. Ne devrais pas prendre plus de 2mins :timer:")
    for infos in url_liste:
        check_url(infos[0], pseudo, infos[1], infos[2])
    if message != "":
        await ctx.send(f"```{message}```")
    await ctx.send(f"**{pseudo}** est inscrit sur {nbr_de_site_trouve}/{len(url_liste)} sites")
    results = search_internet(pseudo, 5)
    message = "Résultats de la recherche pour '{}':\n".format(pseudo)
    for index, result in enumerate(results):
        message += "{}. {}\n".format(index+1, result)
    await ctx.send(f"```{message}```")




@client.command()
async def get_insta(ctx, pseudo):
    await ctx.send("> Commmande actuellement en mise à jour")




@client.command()
async def make_search(ctx, number_of_result, search_to_do):
    number_of_result = int(number_of_result)
    results = search_internet(search_to_do, number_of_result)
    message = "Résultats de la recherche pour '{}':\n".format(search_to_do)
    for index, result in enumerate(results):
        message += "{}. {}\n".format(index+1, result)
    await ctx.send(f"```{message}```")

    
    
def load_responses(filename):
    responses = {}
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            question = row[0]
            answers = row[1:]
            responses[question] = answers
    return responses

# Fonction pour sauvegarder les réponses dans le fichier CSV
def save_responses(filename, responses):
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        for question, answers in responses.items():
            row = [question] + answers
            writer.writerow(row)

# Fonction pour trouver la question la plus proche
def get_closest_question(question, responses):
    closest_question = None
    closest_similarity = 0
    for stored_question in responses.keys():
        similarity = difflib.SequenceMatcher(None, question, stored_question).ratio()
        if similarity > closest_similarity:
            closest_question = stored_question
            closest_similarity = similarity
    return closest_question



@client.command()
async def ask(ctx):
    filename = "ressources.csv"
    responses = load_responses(filename)
    await ctx.send("Posez votre question :")
    try:
        question = await client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
        closest_question = get_closest_question(question.content, responses)
        if closest_question is not None:
            confirm = await ctx.send(f"Est-ce que cette question correspond à votre demande : '{closest_question}' ? (y/n) ")
            try:
                answer = await client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
                if answer.content.lower() == 'y':
                    if closest_question in responses:
                        answer_list = responses[closest_question]
                        response = random.choice(answer_list)
                        await ctx.send(response)
                        await ctx.send("Est-ce que cela répond à votre question ? (y/n) ")
                        try:
                            vote = await client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
                            if vote.content.lower() == 'n':
                                await ctx.send("Qu'aurait dû être la réponse à votre question ? ")
                                try:
                                    new_answer = await client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
                                    answer_list.append(str(new_answer.content).replace(",", " "))
                                    save_responses(filename, responses)
                                    await ctx.send("Réponse ajoutée avec succès !")
                                except asyncio.TimeoutError:
                                    await ctx.send("Temps écoulé, veuillez réessayer.")
                            else:
                                await ctx.send("Cool !")
                        except asyncio.TimeoutError:
                            await ctx.send("Temps écoulé, veuillez réessayer.")
                    else:
                        await ctx.send("Je ne trouve pas de réponse appropriée à votre question. Qu'aurait dû être la réponse ?")
                        try:
                            new_answer = await client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
                            responses[closest_question] = [str(new_answer.content).replace(",", " ")]
                            save_responses(filename, responses)
                            await ctx.send("Question et réponse ajoutées avec succès !")
                        except asyncio.TimeoutError:
                            await ctx.send("Temps écoulé, veuillez réessayer.")
                elif answer.content.lower() == 'n':
                    await ctx.send("Qu'aurait dû être la réponse à votre question ? ")
                    try:
                        new_answer = await client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
                        responses[question.content] = [str(new_answer.content).replace(",", " ")]
                        save_responses(filename, responses)
                        await ctx.send("Question et réponse ajoutées avec succès !")
                    except asyncio.TimeoutError:
                        await ctx.send("Temps écoulé, veuillez réessayer.")
            except asyncio.TimeoutError:
                await ctx.send("Temps écoulé, veuillez réessayer.")
        elif closest_question is None:
            await ctx.send("Je ne trouve pas de réponse appropriée à votre question. Qu'aurait dû être la réponse ?")
            try:
                new_answer = await client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
                responses[question.content] = [str(new_answer.content).replace(",", " ")]
                save_responses(filename, responses)
                await ctx.send("Question et réponse ajoutées avec succès !")
            except asyncio.TimeoutError:
                await ctx.send("Temps écoulé, veuillez réessayer.")
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé, veuillez réessayer.")

@client.command()
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=1112754567864668160&permissions=8&scope=bot")

    
@client.command()
async def bonnes_actions(ctx):
    message = """
Bonjour/Bonsoir à tous ! 👋

📣 - Je vais vous présenter le serveur : **Cleanwalk.org !** 

(**clean walk**: vient de l'anglais marche propre)

🚮 - Ce serveur a pour but de **sensibiliser un maximum de personnes qui sont sur discord d'arrêter de jeter leurs déchets dans la nature** et **d'organiser et/ou de participer à des ramassages de déchets** dans chaque région de France, les pays francophones et les régions d'Outre-mer tout au long de l'année afin de nettoyer nos villes, forêts, plages...
Les inscriptions aux ramassages se font sur le __site internet officiel__ : 

➡ - __Cleanwalk.org__ :  https://www.cleanwalk.org

🎉 - **Animations régulières** (conférences, défis, débats...) en lien avec le thème du serveur.

📮 - **Recrutement en permanence pour rejoindre une équipe du staff** (modération, technique, animation, graphisme et rédaction).

👤 - Ouvert aux **échanges de pubs et aux partenariats avec des serveurs sur le même thème (écologie, biodiversité).**

- > Alors, qu'attendez vous ?
Rejoignez notre serveur dès maintenant ! ⤵

https://cdn.discordapp.com/attachments/723633922507800588/796303228521938964/Sans_titre-1-Recupere.png

- __Lien d'invitation__ 🎟️ : https://discord.gg/XZNHvvd
    
    
    
    """
    await ctx.send(message)
    
