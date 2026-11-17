#!/usr/bin/env python3
"""
Write the one-page summaries in other languages: fr/, de/, es/, it/, and ja/.

Each page is a short overview for people who search in their own language.
It leaves out versions and features on purpose, so a release never needs an
edit here. The Wacom messages are Wacom's own wording in that language.

The pages link to each other and to the English home page with hreflang,
and index.html's footer links to each of them.

Usage (from the repo root):
  tools/summary/build.py [--check]

--check changes nothing and exits 1 if a page is out of date.
"""

import argparse
import html
import json
import sys
from pathlib import Path

SITE = "https://mocktab.org"
DOWNLOAD = "https://github.com/Cyzor/tablet-driver/releases"
SOURCE = "https://github.com/Cyzor/tablet-driver"
FAMILIES = "Intuos, Intuos Pro, Cintiq, Bamboo"

PAGES = {
    "fr": {
        "name": "Français",
        "title": "MockTab : un pilote Mac gratuit pour les anciennes tablettes Wacom",
        "description": "MockTab est un pilote Mac gratuit pour les tablettes Wacom que le pilote de Wacom ne prend plus en charge.",
        "h1": "Votre tablette Wacom fonctionne encore",
        "intro": "Le pilote de Wacom abandonne peu à peu les anciennes tablettes. Votre tablette s’allume peut-être encore, mais si le pilote de Wacom affiche l’un de ces messages, MockTab peut la remettre en service :",
        "messages": ["« Votre périphérique Wacom n’est plus pris en charge »",
                     "« Le pilote de la tablette ne répond pas. »"],
        "what_h": "Ce que fait MockTab",
        "what": f"MockTab est une app Mac gratuite qui lit directement votre tablette. Elle prend en charge la pression, l’inclinaison et les boutons du stylet et de la tablette, sur les modèles USB et Bluetooth des gammes {FAMILIES} et Graphire, jusqu’à la première Intuos de 1998, ainsi que le pack Xencelabs Pen Display.",
        "clean": "Elle n’installe ni extension système ni service en arrière-plan. Pour la désinstaller, placez-la dans la corbeille.",
        "req_h": "Configuration requise",
        "req": "macOS 13 (Ventura) ou ultérieur, sur Mac à puce Apple ou Intel.",
        "start_h": "Pour commencer",
        "steps": ["Vérifiez que votre tablette figure dans la <a href=\"/hardware.html\">liste du matériel</a>.",
                  "Quittez ou désinstallez le pilote de Wacom.",
                  f"<a href=\"{DOWNLOAD}\">Téléchargez MockTab</a>, ouvrez l’app et accordez les autorisations demandées."],
        "language": "L’app est en français. Le <a href=\"/guide.html\">guide complet</a> et les pages de <a href=\"/troubleshooting.html\">dépannage</a> sont uniquement en anglais.",
        "download": "Télécharger pour Mac",
        "footer": "MockTab est un projet indépendant, sans lien avec Wacom.",
        "faq": [
            ("Qu’est-ce que MockTab ?", "Un pilote Mac gratuit pour les tablettes Wacom que le pilote de Wacom ne prend plus en charge."),
            ("Quelles tablettes sont prises en charge ?", f"Les modèles USB et Bluetooth des gammes {FAMILIES} et Graphire, jusqu’à la première Intuos de 1998, ainsi que le pack Xencelabs Pen Display."),
            ("Combien coûte MockTab ?", "Rien. L’app est gratuite et son code source est public."),
        ],
    },
    "de": {
        "name": "Deutsch",
        "title": "MockTab: kostenloser Mac-Treiber für ältere Wacom-Grafiktabletts",
        "description": "MockTab ist ein kostenloser Mac-Treiber für Wacom-Grafiktabletts, die der Wacom-Treiber nicht mehr unterstützt.",
        "h1": "Dein Wacom-Grafiktablett funktioniert noch",
        "intro": "Der Wacom-Treiber stellt die Unterstützung älterer Grafiktabletts nach und nach ein. Vielleicht leuchtet dein Grafiktablett noch, aber wenn der Wacom-Treiber eine dieser Meldungen zeigt, kann MockTab es wieder zum Laufen bringen:",
        "messages": ["„Ihr Wacom Gerät wird nicht mehr unterstützt“",
                     "„Der Tablett-Treiber reagiert nicht.“"],
        "what_h": "Was MockTab macht",
        "what": f"MockTab ist eine kostenlose Mac-App, die dein Grafiktablett direkt ausliest. Sie unterstützt Stiftdruck, Neigung und die Tasten an Stift und Grafiktablett, bei USB- und Bluetooth-Modellen der Serien {FAMILIES} und Graphire bis zurück zum ersten Intuos von 1998, außerdem das Xencelabs-Pen-Display-Bundle.",
        "clean": "MockTab installiert keine Systemerweiterungen und keine Hintergrunddienste. Zum Deinstallieren ziehst du die App in den Papierkorb.",
        "req_h": "Voraussetzungen",
        "req": "macOS 13 (Ventura) oder neuer, auf Apple Silicon oder Intel.",
        "start_h": "Erste Schritte",
        "steps": ["Prüfe, ob dein Grafiktablett in der <a href=\"/hardware.html\">Hardwareliste</a> steht.",
                  "Beende den Wacom-Treiber oder deinstalliere ihn.",
                  f"<a href=\"{DOWNLOAD}\">Lade MockTab herunter</a>, öffne die App und erteile die angefragten Berechtigungen."],
        "language": "Die App ist auf Deutsch. Die ausführliche <a href=\"/guide.html\">Anleitung</a> und die Seiten zur <a href=\"/troubleshooting.html\">Fehlerbehebung</a> gibt es nur auf Englisch.",
        "download": "Für Mac laden",
        "footer": "MockTab ist ein unabhängiges Projekt und gehört nicht zu Wacom.",
        "faq": [
            ("Was ist MockTab?", "Ein kostenloser Mac-Treiber für Wacom-Grafiktabletts, die der Wacom-Treiber nicht mehr unterstützt."),
            ("Welche Grafiktabletts unterstützt MockTab?", f"USB- und Bluetooth-Modelle der Serien {FAMILIES} und Graphire bis zurück zum ersten Intuos von 1998, außerdem das Xencelabs-Pen-Display-Bundle."),
            ("Was kostet MockTab?", "Nichts. MockTab ist kostenlos und quelloffen."),
        ],
    },
    "es": {
        "name": "Español",
        "title": "MockTab: controlador gratuito para Mac para tabletas Wacom antiguas",
        "description": "MockTab es un controlador gratuito para Mac para las tabletas Wacom que el controlador de Wacom ya no admite.",
        "h1": "Tu tableta Wacom todavía funciona",
        "intro": "El controlador de Wacom deja de admitir las tabletas antiguas con el tiempo. Puede que tu tableta aún se encienda, pero si el controlador de Wacom muestra uno de estos mensajes, MockTab puede devolverle la vida:",
        "messages": ["«Su dispositivo Wacom ya no es compatible»",
                     "«La tableta no responde.»"],
        "what_h": "Qué hace MockTab",
        "what": f"MockTab es una app gratuita para Mac que lee tu tableta directamente. Admite la presión y la inclinación del lápiz y los botones del lápiz y de la tableta, en modelos USB y Bluetooth de las familias {FAMILIES} y Graphire, hasta la Intuos original de 1998, además del paquete Xencelabs Pen Display.",
        "clean": "No instala extensiones del sistema ni servicios en segundo plano. Para desinstalarla, muévela a la papelera.",
        "req_h": "Requisitos",
        "req": "macOS 13 (Ventura) o posterior, en Mac con Apple Silicon o Intel.",
        "start_h": "Primeros pasos",
        "steps": ["Comprueba que tu tableta aparece en la <a href=\"/hardware.html\">lista de hardware</a>.",
                  "Sal del controlador de Wacom o desinstálalo.",
                  f"<a href=\"{DOWNLOAD}\">Descarga MockTab</a>, ábrela y concede los permisos que solicita."],
        "language": "La app está en español. La <a href=\"/guide.html\">guía completa</a> y las páginas de <a href=\"/troubleshooting.html\">solución de problemas</a> están en inglés.",
        "download": "Descargar para Mac",
        "footer": "MockTab es un proyecto independiente, sin relación con Wacom.",
        "faq": [
            ("¿Qué es MockTab?", "Un controlador gratuito para Mac para las tabletas Wacom que el controlador de Wacom ya no admite."),
            ("¿Qué tabletas admite MockTab?", f"Modelos USB y Bluetooth de las familias {FAMILIES} y Graphire, hasta la Intuos original de 1998, además del paquete Xencelabs Pen Display."),
            ("¿Cuánto cuesta MockTab?", "Nada. Es gratis y de código abierto."),
        ],
    },
    "it": {
        "name": "Italiano",
        "title": "MockTab: un driver Mac gratuito per le vecchie tavolette Wacom",
        "description": "MockTab è un driver Mac gratuito per le tavolette Wacom che il driver di Wacom non supporta più.",
        "h1": "La tua tavoletta Wacom funziona ancora",
        "intro": "Il driver di Wacom abbandona poco a poco le tavolette più vecchie. La tua tavoletta forse si accende ancora, ma se il driver di Wacom mostra uno di questi messaggi, MockTab può rimetterla in funzione:",
        "messages": ["«Il dispositivo Wacom non è più supportato»",
                     "«Il driver della tavoletta non risponde.»"],
        "what_h": "Cosa fa MockTab",
        "what": f"MockTab è un’app Mac gratuita che legge direttamente la tua tavoletta. Supporta pressione, inclinazione e pulsanti della penna e della tavoletta, sui modelli USB e Bluetooth delle serie {FAMILIES} e Graphire, fino alla prima Intuos del 1998, oltre al kit Xencelabs Pen Display.",
        "clean": "Non installa estensioni di sistema né servizi in background. Per disinstallarla, spostala nel Cestino.",
        "req_h": "Requisiti",
        "req": "macOS 13 (Ventura) o successivo, su Mac con chip Apple o Intel.",
        "start_h": "Per iniziare",
        "steps": ["Controlla che la tua tavoletta sia nell’<a href=\"/hardware.html\">elenco dell’hardware</a>.",
                  "Chiudi o disinstalla il driver di Wacom.",
                  f"<a href=\"{DOWNLOAD}\">Scarica MockTab</a>, apri l’app e concedi le autorizzazioni richieste."],
        "language": "L’app è in italiano. La <a href=\"/guide.html\">guida completa</a> e le pagine di <a href=\"/troubleshooting.html\">risoluzione dei problemi</a> sono solo in inglese.",
        "download": "Scarica per Mac",
        "footer": "MockTab è un progetto indipendente, non affiliato a Wacom.",
        "faq": [
            ("Cos’è MockTab?", "Un driver Mac gratuito per le tavolette Wacom che il driver di Wacom non supporta più."),
            ("Quali tavolette supporta MockTab?", f"I modelli USB e Bluetooth delle serie {FAMILIES} e Graphire, fino alla prima Intuos del 1998, oltre al kit Xencelabs Pen Display."),
            ("Quanto costa MockTab?", "Niente. L’app è gratuita e il suo codice sorgente è pubblico."),
        ],
    },
    "ja": {
        "name": "日本語",
        "title": "MockTab：古いワコムのペンタブレット向けの無料Macドライバ",
        "description": "MockTabは、ワコムのドライバでサポートが終了したワコムのペンタブレット向けの無料Macドライバです。",
        "h1": "そのワコムのペンタブレット、まだ使えます",
        "intro": "ワコムのドライバは、古いペンタブレットのサポートを順次終了しています。タブレットのランプが点灯していても、ワコムのドライバに次のメッセージが表示される場合は、MockTabで再び使えるようになるかもしれません。",
        "messages": ["「お使いのワコムデバイスは現在サポートされていません。」",
                     "「タブレットドライバが反応していません。」"],
        "what_h": "MockTabでできること",
        "what": "MockTabは、ペンタブレットから直接データを読み取る無料のMacアプリです。筆圧、傾き、ペンとタブレットのボタンに対応しています。対象は、Intuos、Intuos Pro、Cintiq、Bamboo、GraphireシリーズのUSBおよびBluetoothモデル（1998年の初代Intuosまで）と、Xencelabs Pen Displayバンドルです。",
        "clean": "システム拡張やバックグラウンドサービスはインストールしません。アンインストールは、アプリをゴミ箱に入れるだけです。",
        "req_h": "動作環境",
        "req": "macOS 13（Ventura）以降。Appleシリコン搭載MacとIntel搭載Macに対応しています。",
        "start_h": "使い方",
        "steps": ["お使いのタブレットが<a href=\"/hardware.html\">ハードウェア一覧</a>に載っているか確認します。",
                  "ワコムのドライバを終了するか、アンインストールします。",
                  f"<a href=\"{DOWNLOAD}\">MockTabをダウンロード</a>して開き、求められたアクセス許可を与えます。"],
        "language": "アプリは日本語に対応しています。詳しい<a href=\"/guide.html\">ガイド</a>と<a href=\"/troubleshooting.html\">トラブルシューティング</a>のページは英語のみです。",
        "download": "Mac版をダウンロード",
        "footer": "MockTabは独立したプロジェクトで、ワコムとは関係ありません。",
        "faq": [
            ("MockTabとは？", "ワコムのドライバでサポートが終了したワコムのペンタブレット向けの無料Macドライバです。"),
            ("対応しているタブレットは？", "Intuos、Intuos Pro、Cintiq、Bamboo、GraphireシリーズのUSBおよびBluetoothモデル（1998年の初代Intuosまで）と、Xencelabs Pen Displayバンドルです。"),
            ("料金は？", "無料です。ソースコードも公開されています。"),
        ],
    },
}


def alternates():
    links = [f'<link rel="alternate" hreflang="en" href="{SITE}/" />',
             f'<link rel="alternate" hreflang="x-default" href="{SITE}/" />']
    links += [f'<link rel="alternate" hreflang="{l}" href="{SITE}/{l}/" />' for l in PAGES]
    return "\n        ".join(links)


def language_row(current):
    items = ['<a href="/" hreflang="en" lang="en">English</a>']
    for l, p in PAGES.items():
        if l == current:
            items.append(f'<span aria-current="page">{p["name"]}</span>')
        else:
            items.append(f'<a href="/{l}/" hreflang="{l}" lang="{l}">{p["name"]}</a>')
    return " &middot; ".join(items)


def page(lang, p):
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": lang,
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]],
    }
    e = html.escape
    messages = "\n".join(f"                <li><strong>{e(m)}</strong></li>" for m in p["messages"])
    steps = "\n".join(f"                <li>{s}</li>" for s in p["steps"])
    return f"""<!doctype html>
<html lang="{lang}">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{e(p["title"])}</title>
        <meta name="description" content="{e(p["description"])}" />
        <link rel="stylesheet" href="/css/style.css" />
        <link rel="canonical" href="{SITE}/{lang}/" />
        {alternates()}
        <meta property="og:title" content="{e(p["title"])}" />
        <meta property="og:description" content="{e(p["description"])}" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{SITE}/{lang}/" />
        <link rel="icon" type="image/svg+xml" href="/images/favicon/favicon-light.svg" media="(prefers-color-scheme: light)" />
        <link rel="icon" type="image/svg+xml" href="/images/favicon/favicon-dark.svg" media="(prefers-color-scheme: dark)" />
        <link rel="mask-icon" href="/images/favicon/safari-pinned-tab.svg" color="#00696f" />
        <script type="application/ld+json">
{json.dumps(faq, ensure_ascii=False, indent=4)}
        </script>
    </head>
    <body>
        <header class="site">
            <div class="wrap">
                <a href="/" class="brand">MockTab</a>
                <nav aria-label="Languages">{language_row(lang)}</nav>
            </div>
        </header>
        <main id="main" class="wrap">
            <h1>{e(p["h1"])}</h1>
            <p>{e(p["intro"])}</p>
            <ul class="bullets">
{messages}
            </ul>
            <h2>{e(p["what_h"])}</h2>
            <p>{e(p["what"])}</p>
            <p>{e(p["clean"])}</p>
            <h2>{e(p["req_h"])}</h2>
            <p>{e(p["req"])}</p>
            <h2>{e(p["start_h"])}</h2>
            <ol>
{steps}
            </ol>
            <p>{p["language"]}</p>
            <p><a class="cta" href="{DOWNLOAD}">{e(p["download"])}</a></p>
        </main>
        <footer class="site">
            <div class="wrap">
                <p>{e(p["footer"])} &middot; <a href="{SOURCE}">GitHub</a></p>
            </div>
        </footer>
    </body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    stale = []
    for lang, p in PAGES.items():
        path = root / lang / "index.html"
        text = page(lang, p)
        if path.exists() and path.read_text(encoding="utf-8") == text:
            continue
        stale.append(path.relative_to(root))
        if not args.check:
            path.parent.mkdir(exist_ok=True)
            path.write_text(text, encoding="utf-8")
    for s in stale:
        print(("out of date: " if args.check else "wrote ") + str(s))
    sys.exit(1 if args.check and stale else 0)


if __name__ == "__main__":
    main()
