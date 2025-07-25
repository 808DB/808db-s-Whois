import subprocess
import requests
import os
from colorama import init
import getpass
import socket
import sys

init()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Palette violet/bleu clair pour le dégradé
colors = [129, 135, 141, 147, 111, 117, 123, 159]

def color_print(text, index):
    color_code = colors[index % len(colors)]
    print(f"\033[38;5;{color_code}m{text}\033[0m")

def print_gradient_menu():
    menu_lines = [
        "   ██████╗  ██╗██████╗ ",
        "   ╚════██╗███║╚════██╗",
        "    █████╔╝╚██║ █████╔╝",
        "   ██╔═══╝  ██║██╔═══╝ ",
        "   ███████╗ ██║███████╗",
        "   ╚══════╝ ╚═╝╚══════╝",
        "",
        "       OSINT Tool by .808db.",
        "╔════════════════════════════════════════════╗",
        "║ [1] IP Lookup (WHOIS + GeoIP + liens OSINT)║",
        "║ [2] Database Lookup (fichier local)        ║",
        "║ [3] Ping                                   ║",
        "║ [4] Traceroute                             ║",
        "║ [5] Nmap Scan (si installé)                ║",
        "║ [6] SQLMap (si installé)                   ║",
        "║ [7] Quitter                                ║",
        "╚════════════════════════════════════════════╝"
    ]
    for i, line in enumerate(menu_lines):
        color_print(line, i)

def colored_input(prompt_text, index):
    color_code = colors[index % len(colors)]
    return input(f"\033[38;5;{color_code}m{prompt_text}\033[0m")

def print_subprocess_output(proc):
    # Récupérer la sortie ligne par ligne et afficher avec dégradé
    i = 0
    for line in proc.stdout:
        line = line.decode(errors='ignore').rstrip()
        if line:
            color_print(line, i)
            i += 1

def ip_lookup():
    clear_screen()
    target = colored_input("Entrez une IP ou un domaine : ", 0).strip()

    print()
    # WHOIS (python-whois)
    color_print("== WHOIS ==", 1)
    try:
        import whois
        w = whois.whois(target)
        for i, line in enumerate(str(w).splitlines()):
            color_print(line, (2 + i) % len(colors))
    except Exception as e:
        color_print(f"Erreur WHOIS : {e}", 3)

    print()
    # GEOIP via ip-api.com
    color_print("== GEOIP via ip-api.com ==", 1)
    try:
        r = requests.get(f"http://ip-api.com/json/{target}", timeout=5)
        data = r.json()
        if data.get('status') == 'success':
            for i, k in enumerate(['query', 'country', 'regionName', 'city', 'lat', 'lon', 'timezone', 'isp', 'org', 'as']):
                color_print(f"{k}: {data.get(k)}", (2 + i) % len(colors))
        else:
            color_print(f"Erreur géoloc : {data.get('message')}", 3)
    except Exception as e:
        color_print(f"Erreur requête géoloc : {e}", 3)

    print()
    # Liens OSINT
    color_print("== Liens OSINT ==", 1)
    links = {
        "Shodan": f"https://www.shodan.io/search?query={target}",
        "Censys": f"https://search.censys.io/hosts?q={target}",
        "CriminalIP": f"https://criminalip.io/en/asset/ip/{target}",
        "VirusTotal": f"https://www.virustotal.com/gui/ip-address/{target}/detection",
        "AbuseIPDB": f"https://www.abuseipdb.com/check/{target}"
    }
    for i, (name, url) in enumerate(links.items()):
        color_print(f"{name} : {url}", (2 + i) % len(colors))

    colored_input("\nAppuie sur Entrée pour revenir au menu...", 6)

def database_lookup():
    clear_screen()
    path = colored_input("Chemin du fichier local (.txt, .csv, etc) : ", 0).strip()
    if not os.path.exists(path):
        color_print("Fichier introuvable.", 3)
        colored_input("\nAppuie sur Entrée pour revenir au menu...", 6)
        return

    keyword = colored_input("Mot ou IP à rechercher dans la base : ", 1).strip()
    color_print(f"\nRecherche de \"{keyword}\" dans {path}...\n", 2)
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            found = False
            for i, line in enumerate(f):
                if keyword in line:
                    color_print(f"[Ligne {i+1}] {line.strip()}", (3 + i) % len(colors))
                    found = True
        if not found:
            color_print("Aucun résultat trouvé.", 3)
    except Exception as e:
        color_print(f"Erreur lecture : {e}", 3)

    colored_input("\nAppuie sur Entrée pour revenir au menu...", 6)

def ping_target():
    clear_screen()
    target = colored_input("IP ou domaine à ping : ", 0).strip()
    try:
        # Lance la commande ping et récupère la sortie
        proc = subprocess.Popen(
            ["ping", "-n", "4", target] if os.name == "nt" else ["ping", "-c", "4", target],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        print_subprocess_output(proc)
        proc.wait()
    except Exception as e:
        color_print(f"Erreur ping : {e}", 3)
    colored_input("\nAppuie sur Entrée pour revenir au menu...", 6)

def traceroute_target():
    clear_screen()
    target = colored_input("IP ou domaine à traceroute : ", 0).strip()
    try:
        proc = subprocess.Popen(
            ["tracert", target] if os.name == "nt" else ["traceroute", target],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        print_subprocess_output(proc)
        proc.wait()
    except Exception as e:
        color_print(f"Erreur traceroute : {e}", 3)
    colored_input("\nAppuie sur Entrée pour revenir au menu...", 6)

def nmap_scan():
    clear_screen()
    target = colored_input("Cible pour Nmap : ", 0).strip()
    try:
        proc = subprocess.Popen(
            ["nmap", "-sV", target],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        print_subprocess_output(proc)
        proc.wait()
    except Exception as e:
        color_print(f"Erreur Nmap (installé ?) : {e}", 3)
    colored_input("\nAppuie sur Entrée pour revenir au menu...", 6)

def sqlmap_run():
    clear_screen()
    target = colored_input("URL vulnérable SQL à tester (ex: http://site.com/index.php?id=1) : ", 0).strip()
    try:
        proc = subprocess.Popen(
            ["sqlmap", "-u", target, "--batch", "--banner"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        print_subprocess_output(proc)
        proc.wait()
    except Exception as e:
        color_print(f"Erreur SQLMap (installé ?) : {e}", 3)
    colored_input("\nAppuie sur Entrée pour revenir au menu...", 6)

def menu():
    hostname = socket.gethostname().upper()  # Nom PC en majuscules
    user = getpass.getuser()
    while True:
        clear_screen()
        print_gradient_menu()
        # Affichage du prompt personnalisé avec le nom PC @ panel et couleurs dégradées caractère par caractère
        prompt_base = f"┌──({hostname}@808panel)─[~/Windows/Panel]\n└─$ "
        colored_prompt = "".join(
            f"\033[38;5;{colors[i % len(colors)]}m{c}\033[0m" for i, c in enumerate(prompt_base)
        )
        choix = input(colored_prompt).strip()

        if choix == "1":
            ip_lookup()
        elif choix == "2":
            database_lookup()
        elif choix == "3":
            ping_target()
        elif choix == "4":
            traceroute_target()
        elif choix == "5":
            nmap_scan()
        elif choix == "6":
            sqlmap_run()
        elif choix == "7":
            color_print("Bye.", 2)
            break
        else:
            color_print("Choix invalide.", 3)
            colored_input("\nAppuie sur Entrée pour continuer...", 6)

if __name__ == "__main__":
    menu()
