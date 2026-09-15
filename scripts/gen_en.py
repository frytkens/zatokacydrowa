#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates the /en/ English mirror of the site from the Polish source files.
Run once from the repo root: python3 scripts/gen_en.py
Not part of the deployed site (scripts/ is not linked from any page).
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = [
    "index.html",
    "kontakt.html",
    "dla-dzieci.html",
    "mieszkania-letnie.html",
    "polityka-prywatnosci.html",
    "apartamenty/apartament-1.html",
    "apartamenty/apartament-2.html",
    "apartamenty/apartament-3.html",
    "apartamenty/apartament-4.html",
    "apartamenty-letnie/apartament-letni-1.html",
    "apartamenty-letnie/apartament-letni-2.html",
    "apartamenty-letnie/apartament-letni-3.html",
    "apartamenty-letnie/apartament-letni-4.html",
]

# Ordered PL -> EN dictionary. Longest strings first avoids partial-overlap
# clobbering (applied in this order, top to bottom).
DICT = [
    # ---- Meta / titles ----
    ("Zatoka Cydrowa Stegna — Apartamenty klimatyzowane 1500 m od plaży", "Zatoka Cydrowa Stegna — Air-conditioned apartments 1500 m from the beach"),
    ("Zatoka Cydrowa — apartamenty i domki w Stegnie, 1500 m od piaszczystej plaży. Klimatyzacja, wellness (komora hiperbaryczna, sauna, solarium), plac zabaw. Zadzwoń: 797 315 001.", "Zatoka Cydrowa — apartments and cottages in Stegna, 1500 m from the sandy beach. Air conditioning, wellness (hyperbaric chamber, sauna, solarium), playground. Call: +48 797 315 001."),
    ("Apartamenty i domki letniskowe w Stegnie, w otoczeniu sosnowego lasu, 1500 m od Bałtyku. Wellness, plac zabaw, monitorowany parking.", "Apartments and holiday cottages in Stegna, surrounded by pine forest, 1500 m from the Baltic Sea. Wellness zone, playground, monitored parking."),
    ("Kontakt — Zatoka Cydrowa, Stegna", "Contact — Zatoka Cydrowa, Stegna"),
    ("Skontaktuj się z Zatoką Cydrową w Stegnie: telefon 797 315 001, Messenger na Facebooku, adres ul. Grunwaldzka 12, 82-103 Stegna.", "Get in touch with Zatoka Cydrowa in Stegna: phone +48 797 315 001, Messenger on Facebook, address Grunwaldzka 12, 82-103 Stegna, Poland."),
    ("Dla dzieci — sala zabaw „Zatoczka Cydrowa” — Zatoka Cydrowa, Stegna", "For kids — the “Zatoczka Cydrowa” playroom — Zatoka Cydrowa, Stegna"),
    ("Sala zabaw „Zatoczka Cydrowa” i plac zabaw w ogrodzie — atrakcje dla najmłodszych gości Zatoki Cydrowej w Stegnie, niezależnie od pogody.", "The “Zatoczka Cydrowa” playroom and garden playground — attractions for our youngest guests at Zatoka Cydrowa in Stegna, whatever the weather."),
    ("Mieszkania letnie – pokoje z łazienkami — Zatoka Cydrowa", "Summer rooms with private bathrooms — Zatoka Cydrowa"),
    ("Mieszkania letnie w Zatoce Cydrowej, Stegna: pokoje letnie z łazienkami, dostępne w sezonie wakacyjnym. Zapytaj o dostępność: 797 315 001.", "Summer rooms at Zatoka Cydrowa, Stegna: rooms with private bathrooms, available during the summer season. Ask about availability: +48 797 315 001."),
    ("Polityka prywatności — Zatoka Cydrowa", "Privacy Policy — Zatoka Cydrowa"),
    ("Polityka prywatności serwisu zatokacydrowa.pl — zasady przetwarzania danych osobowych.", "Privacy Policy for zatokacydrowa.pl — rules for the processing of personal data."),
    ("Apartament 1 – 65 m² z tarasem i 2 łazienkami (do 8 osób) — Zatoka Cydrowa", "Apartment 1 – 65 m² with a terrace and 2 bathrooms (up to 8 guests) — Zatoka Cydrowa"),
    ("Apartament 1 w Zatoce Cydrowej, Stegna: do 8 osób, 65 m², 3 pokoje, 2 niezależne łazienki, taras z wyjściem do ogrodu. Rezerwacja bezpośrednia: 797 315 001.", "Apartment 1 at Zatoka Cydrowa, Stegna: up to 8 guests, 65 m², 3 rooms, 2 independent bathrooms, terrace opening onto the garden. Book directly: +48 797 315 001."),
    ("Apartament 2 – 35 m² na piętrze (do 5 osób) — Zatoka Cydrowa", "Apartment 2 – 35 m² on the upper floor (up to 5 guests) — Zatoka Cydrowa"),
    ("Apartament 2 w Zatoce Cydrowej, Stegna: do 5 osób, 35 m², 2 pokoje, piętro 2, w pełni wyposażony aneks kuchenny. Rezerwacja bezpośrednia: 797 315 001.", "Apartment 2 at Zatoka Cydrowa, Stegna: up to 5 guests, 35 m², 2 rooms, 2nd floor, fully equipped kitchenette. Book directly: +48 797 315 001."),
    ("Apartament 3 – 65 m² z 2 łazienkami (do 7 osób) — Zatoka Cydrowa", "Apartment 3 – 65 m² with 2 bathrooms (up to 7 guests) — Zatoka Cydrowa"),
    ("Apartament 3 w Zatoce Cydrowej, Stegna: do 7 osób, 65 m², 2 pokoje, piętro 1, 2 niezależne łazienki. Rezerwacja bezpośrednia: 797 315 001.", "Apartment 3 at Zatoka Cydrowa, Stegna: up to 7 guests, 65 m², 2 rooms, 1st floor, 2 independent bathrooms. Book directly: +48 797 315 001."),
    ("Apartament 4 – 35 m² na piętrze (do 4 osób) — Zatoka Cydrowa", "Apartment 4 – 35 m² on the upper floor (up to 4 guests) — Zatoka Cydrowa"),
    ("Apartament 4 w Zatoce Cydrowej, Stegna: do 4 osób, 35 m², 2 pokoje, piętro 2, osobna sypialnia i aneks kuchenny. Rezerwacja bezpośrednia: 797 315 001.", "Apartment 4 at Zatoka Cydrowa, Stegna: up to 4 guests, 35 m², 2 rooms, 2nd floor, separate bedroom and kitchenette. Book directly: +48 797 315 001."),
    ("Apartament letni 1 – dwupokojowy lokal wakacyjny — Zatoka Cydrowa", "Summer Apartment 1 – two-room holiday unit — Zatoka Cydrowa"),
    ("Apartament letni 1 w Zatoce Cydrowej, Stegna: dwa pokoje, jadalnia i aneks kuchenny — dobry wybór na letni wypoczynek rodzinny. Rezerwacja: 797 315 001.", "Summer Apartment 1 at Zatoka Cydrowa, Stegna: two rooms, dining area and kitchenette — a great choice for a family summer holiday. Booking: +48 797 315 001."),
    ("Apartament letni 2 – lokal dla pary — Zatoka Cydrowa", "Summer Apartment 2 – a unit for couples — Zatoka Cydrowa"),
    ("Apartament letni 2 w Zatoce Cydrowej, Stegna: przytulny lokal dla pary z prywatną łazienką. Rezerwacja: 797 315 001.", "Summer Apartment 2 at Zatoka Cydrowa, Stegna: a cosy unit for couples with a private bathroom. Booking: +48 797 315 001."),
    ("Apartament letni 3 – stylowa, czarno-biała aranżacja — Zatoka Cydrowa", "Summer Apartment 3 – stylish black-and-white interior — Zatoka Cydrowa"),
    ("Apartament letni 3 w Zatoce Cydrowej, Stegna: stylowa, czarno-biała aranżacja z dwiema sypialniami, aneksem kuchennym i łazienką. Rezerwacja: 797 315 001.", "Summer Apartment 3 at Zatoka Cydrowa, Stegna: a stylish black-and-white interior with two bedrooms, a kitchenette and a bathroom. Booking: +48 797 315 001."),
    ("Apartament letni 4 – dla rodziny 2+2 — Zatoka Cydrowa", "Summer Apartment 4 – for a family of 4 — Zatoka Cydrowa"),
    ("Apartament letni 4 w Zatoce Cydrowej, Stegna: osobna sypialnia i pełne wyposażenie dla rodziny 2+2. Rezerwacja: 797 315 001.", "Summer Apartment 4 at Zatoka Cydrowa, Stegna: separate bedroom and full facilities for a family of 4. Booking: +48 797 315 001."),

    # ---- JSON-LD (LodgingBusiness / reviews / FAQ / amenities) ----
    ("Klimatyzacja", "Air conditioning"),
    ("Komora hiperbaryczna", "Hyperbaric chamber"),
    ("Sauna", "Sauna"),
    ("Solarium", "Solarium"),
    ("Plac zabaw", "Playground"),
    ("Monitorowany parking", "Monitored parking"),
    ("Zwierzęta dozwolone", "Pets allowed"),
    ("Pobyt w Zatoce Cydrowej był wspaniały. Obiekt jest super, położony w spokojnym miejscu, idealnym na odpoczynek. Gospodarze są fantastyczni — bardzo serdeczni i pomocni.", "Our stay at Zatoka Cydrowa was wonderful. The place is great, in a quiet spot perfect for relaxing. The hosts are fantastic — very warm and helpful."),
    ("Do tego opalenizna z solarium, gorący powiew z sauny — człowiek od razu zapomina, że nad Bałtykiem właśnie pada. Dzieci mają tutaj swój raj — bilard, kino i plac zabaw.", "A tan from the solarium, a hot blast from the sauna — you instantly forget it's raining by the Baltic. Kids have their own paradise here — pool table, cinema and a playground."),
    ("Jeśli szukacie idealnego miejsca na odpoczynek nad morzem, to Zatoka Cydrowa jest strzałem w dziesiątkę. Pokoje lśnią czystością, są urządzone ze smakiem i bardzo przytulne.", "If you're looking for the perfect place to relax by the sea, Zatoka Cydrowa is a bullseye. The rooms are spotless, tastefully furnished and very cosy."),
    ("Jak daleko jest do plaży od Zatoki Cydrowej?", "How far is the beach from Zatoka Cydrowa?"),
    ("Ok. 1500 m pieszo od piaszczystej plaży w Stegnie.", "About 1500 m on foot from the sandy beach in Stegna."),
    ("Czy w Zatoce Cydrowej można zostać ze zwierzęciem?", "Can I stay at Zatoka Cydrowa with a pet?"),
    ("Tak, zwierzęta domowe są mile widziane we wszystkich apartamentach.", "Yes, pets are welcome in all of our apartments."),
    ("Czy jest parking na miejscu?", "Is there parking on site?"),
    ("Tak, na terenie obiektu jest duży, monitorowany i bezpieczny parking.", "Yes, there is a large, monitored and secure car park on site."),
    ("Czy strefa wellness (sauna, komora hiperbaryczna, solarium) działa poza sezonem letnim?", "Is the wellness zone (sauna, hyperbaric chamber, solarium) open outside the summer season?"),
    ("Tak, komora hiperbaryczna, sauna i solarium są dostępne dla gości przez cały rok.", "Yes, the hyperbaric chamber, sauna and solarium are available to guests all year round."),
    ("Czy apartamenty są klimatyzowane?", "Are the apartments air-conditioned?"),
    ("Tak, wszystkie cztery apartamenty całoroczne są klimatyzowane.", "Yes, all four year-round apartments are air-conditioned."),
    ("Klimatyzowany apartament na 1. piętrze: 65 m², 3 pokoje (salon + 2 sypialnie), 2 niezależne łazienki, taras z wyjściem do ogrodu. Do 8 osób.", "Air-conditioned 1st-floor apartment: 65 m², 3 rooms (living room + 2 bedrooms), 2 independent bathrooms, terrace opening onto the garden. Up to 8 guests."),
    ("Klimatyzowany apartament na 2. piętrze: 35 m², 2 pokoje (salon + sypialnia), 1 łazienka, w pełni wyposażony aneks kuchenny. Do 5 osób.", "Air-conditioned 2nd-floor apartment: 35 m², 2 rooms (living room + bedroom), 1 bathroom, fully equipped kitchenette. Up to 5 guests."),
    ("Klimatyzowany apartament na 1. piętrze: 65 m², 2 pokoje (salon + sypialnia), 2 niezależne łazienki. Do 7 osób.", "Air-conditioned 1st-floor apartment: 65 m², 2 rooms (living room + bedroom), 2 independent bathrooms. Up to 7 guests."),
    ("Klimatyzowany apartament na 2. piętrze: 35 m², 2 pokoje (salon + osobna sypialnia), 1 łazienka, aneks kuchenny. Do 4 osób.", "Air-conditioned 2nd-floor apartment: 35 m², 2 rooms (living room + separate bedroom), 1 bathroom, kitchenette. Up to 4 guests."),
    ("Sezonowy lokal wakacyjny (dostępność czerwiec–wrzesień): 2 pokoje (jadalnia + sypialnia), w pełni wyposażony aneks kuchenny.", "Seasonal holiday unit (available June–September): 2 rooms (dining area + bedroom), fully equipped kitchenette."),
    ("Sezonowy lokal wakacyjny (dostępność czerwiec–wrzesień) dla pary, z prywatną łazienką.", "Seasonal holiday unit (available June–September) for couples, with a private bathroom."),
    ("Sezonowy lokal wakacyjny (dostępność czerwiec–wrzesień): 2 sypialnie, 1 łazienka, stylowa czarno-biała aranżacja.", "Seasonal holiday unit (available June–September): 2 bedrooms, 1 bathroom, stylish black-and-white interior."),
    ("Sezonowy lokal wakacyjny (dostępność czerwiec–wrzesień) dla rodziny 2+2, z osobną sypialnią.", "Seasonal holiday unit (available June–September) for a family of 4, with a separate bedroom."),

    # ---- Breadcrumb / nav labels ----
    ("Strona główna", "Home"),
    ("Menu główne", "Main menu"),
    ("Menu mobilne", "Mobile menu"),
    ("Otwórz menu", "Open menu"),
    ("Apartamenty całoroczne", "Year-round apartments"),
    ("Apartamenty letnie", "Summer apartments"),
    ("Apartamenty", "Apartments"),
    ("Atrakcje", "Attractions"),
    ("Wellness", "Wellness"),
    ("Opinie", "Reviews"),
    ("Okolica", "Area"),
    ("Kontakt", "Contact"),
    ("Sprawdź dostępność", "Check availability"),
    ("Dla dzieci", "For kids"),
    ("Mieszkania letnie", "Summer rooms"),
    ("Polityka prywatności", "Privacy Policy"),

    # ---- Hero ----
    ("Stegna · Sosnowy las", "Stegna · Pine forest"),
    ("Twój spokojny kawałek Bałtyku", "Your quiet corner of the Baltic"),
    ("Apartamenty w Stegnie, wśród sosnowego lasu. 1500 m od plaży.", "Apartments in Stegna, nestled in a pine forest. 1500 m from the beach."),
    ("Sprawdź apartamenty", "See our apartments"),
    ("Zadzwoń i zapytaj o termin", "Call to ask about dates"),
    ("do plaży", "to the beach"),
    ("Sosnowy las", "Pine forest"),
    ("cisza i spokój", "peace and quiet"),
    ("Dla rodzin", "For families"),
    ("plac zabaw i ogród", "playground and garden"),
    ("sauna, komora, solarium", "sauna, chamber, solarium"),

    # ---- Intro ----
    ("Wypoczynek, który zaczyna się już po przekroczeniu bramy", "A holiday that begins the moment you walk through the gate"),
    ("Zatoka Cydrowa to spokojne miejsce wśród sosnowego lasu, stworzone z myślą o rodzinnym wypoczynku nad Bałtykiem. Plaża, natura, własny taras i przestrzeń, w której można naprawdę zwolnić.", "Zatoka Cydrowa is a quiet spot in a pine forest, built for a family holiday by the Baltic. The beach, nature, your own terrace, and space to really slow down."),

    # ---- Apartments section head ----
    ("Przestronne apartamenty w sercu leśnej Stegny", "Spacious apartments in the heart of forested Stegna"),
    ("Cztery klimatyzowane apartamenty z własnym tarasem, aneksem kuchennym i dwiema niezależnymi łazienkami w większych lokalach.", "Four air-conditioned apartments with their own terrace, a kitchenette, and two independent bathrooms in the larger units."),
    ("Do 8 osób", "Up to 8 guests"),
    ("Do 5 osób", "Up to 5 guests"),
    ("Do 7 osób", "Up to 7 guests"),
    ("Do 4 osób", "Up to 4 guests"),
    ("65 m² · 3 pokoje · piętro 1 · 2 niezależne łazienki", "65 m² · 3 rooms · 1st floor · 2 independent bathrooms"),
    ("35 m² · 2 pokoje · piętro 2", "35 m² · 2 rooms · 2nd floor"),
    ("65 m² · 2 pokoje · piętro 1 · 2 niezależne łazienki", "65 m² · 2 rooms · 1st floor · 2 independent bathrooms"),
    ("Apartament 1", "Apartment 1"),
    ("Apartament 2", "Apartment 2"),
    ("Apartament 3", "Apartment 3"),
    ("Apartament 4", "Apartment 4"),
    ("Zobacz szczegóły →", "See details →"),

    # ---- Summer apartments section ----
    ("Oferta sezonowa", "Seasonal offer"),
    ("Apartamenty letnie", "Summer apartments"),
    ("Kameralne lokale dostępne w sezonie letnim — świetna opcja dla par i małych rodzin szukających prostego, wygodnego noclegu blisko morza.", "Intimate units available during the summer season — a great option for couples and small families looking for a simple, comfortable stay close to the sea."),
    ("2 pokoje", "2 rooms"),
    ("Lokal dwupokojowy, dostępny w sezonie letnim", "A two-room unit, available during the summer season"),
    ("Dla par", "For couples"),
    ("Kameralny lokal dwuosobowy", "An intimate unit for two"),
    ("Design", "Design"),
    ("Stylowa, czarno-biała aranżacja z nastrojowym oświetleniem", "A stylish black-and-white interior with mood lighting"),
    ("Lokal czteroosobowy z osobną sypialnią", "A unit for four with a separate bedroom"),
    ("Apartament letni 1", "Summer Apartment 1"),
    ("Apartament letni 2", "Summer Apartment 2"),
    ("Apartament letni 3", "Summer Apartment 3"),
    ("Apartament letni 4", "Summer Apartment 4"),

    # ---- Mieszkania letnie block on index ----
    ("Sezon letni · ekonomiczny wypoczynek", "Summer season · budget-friendly stay"),
    ("Dodatkowe pokoje letnie z własnymi łazienkami — dobra opcja na prosty, ekonomiczny nocleg blisko morza.", "Extra summer rooms with private bathrooms — a good option for a simple, budget-friendly stay close to the sea."),
    ("Własna łazienka", "Private bathroom"),
    ("Mieszkania letnie – pokoje z łazienkami", "Summer rooms – rooms with private bathrooms"),
    ("Pokoje letnie z łazienkami", "Summer rooms with private bathrooms"),
    ("Dodatkowe pokoje letnie z własnymi łazienkami, dostępne w sezonie wakacyjnym — ekonomiczna opcja noclegu blisko morza. Kliknij zdjęcie, aby powiększyć.", "Extra summer rooms with private bathrooms, available during the holiday season — a budget-friendly stay close to the sea. Click a photo to enlarge."),
    ("Zapytaj o dostępność", "Ask about availability"),
    ("Mieszkania letnie to dodatkowe pokoje z własnymi łazienkami, dostępne w sezonie letnim — dobra opcja dla gości szukających prostego, ekonomicznego noclegu blisko morza. Zapytaj telefonicznie o aktualną dostępność i szczegóły.", "Summer rooms are extra rooms with private bathrooms, available during the summer season — a good option for guests looking for a simple, budget-friendly stay close to the sea. Call us to check current availability and details."),
    ("Zobacz także nasze apartamenty letnie", "See our summer apartments too"),
    ("Każdy pokój letni ma niezależną łazienkę — bez dzielenia z innymi gośćmi.", "Every summer room has its own bathroom — no sharing with other guests."),
    ("Ta sama lokalizacja", "Same location"),
    ("1500 m od plaży, w tym samym miejscu co pozostałe apartamenty Zatoki Cydrowej.", "1500 m from the beach, at the same site as the rest of the Zatoka Cydrowa apartments."),
    ("Ekonomiczna opcja", "Budget-friendly option"),
    ("Zobacz galerię →", "See gallery →"),

    # ---- Why us section ----
    ("Dlaczego Zatoka Cydrowa", "Why Zatoka Cydrowa"),
    ("Wygoda, cisza i bezpieczeństwo dla całej rodziny", "Comfort, quiet and safety for the whole family"),
    ("spokojna, zalesiona okolica Stegny", "a quiet, forested part of Stegna"),
    ("Blisko Bałtyku", "Close to the Baltic"),
    ("1500 m do piaszczystego wybrzeża", "1500 m to the sandy coastline"),
    ("Monitorowany parking", "Monitored parking"),
    ("duży, zamknięty i bezpieczny", "large, gated and secure"),
    ("Zwierzęta mile widziane", "Pets welcome"),
    ("nie musisz zostawiać pupila w domu", "no need to leave your pet at home"),

    # ---- Wellness section ----
    ("Regeneracja przez cały rok", "Recovery all year round"),
    ("Strefa wellness na miejscu", "On-site wellness zone"),
    ("Komora hiperbaryczna, sauna i solarium — dostępne także poza sezonem letnim.", "Hyperbaric chamber, sauna and solarium — available outside the summer season too."),
    ("Komora hiperbaryczna", "Hyperbaric chamber"),
    ("Wspomaga regenerację organizmu i szybszy powrót do formy po wysiłku.", "Supports the body's recovery and a faster return to form after exercise."),
    ("Wspiera regenerację i lepsze dotlenienie organizmu", "Supports recovery and better oxygenation of the body"),
    ("Polecana po intensywnym dniu na plaży lub treningu", "Recommended after an intense day at the beach or a workout"),
    ("Dostępna dla gości Zatoki Cydrowej przez cały rok", "Available to Zatoka Cydrowa guests all year round"),
    ("Umów sesję", "Book a session"),
    ("Relaks po dniu na plaży i wsparcie regeneracji mięśni.", "Relaxation after a day at the beach and support for muscle recovery."),
    ("Klasyczna sauna sucha dostępna na miejscu", "A classic dry sauna available on site"),
    ("Doskonała forma relaksu po aktywnym dniu", "A great way to relax after an active day"),
    ("Rezerwacja telefoniczna, bez dodatkowych opłat rezerwacyjnych", "Book by phone, no extra booking fees"),
    ("Dostępne na miejscu, niezależnie od pogody za oknem.", "Available on site, whatever the weather outside."),
    ("Dogodna lokalizacja na terenie obiektu", "Conveniently located on the property"),
    ("Dostępne poza sezonem letnim", "Available outside the summer season"),
    ("Idealne uzupełnienie dnia spędzonego nad morzem", "A perfect finish to a day spent by the sea"),

    # ---- Kids section ----
    ("Dla najmłodszych gości", "For our youngest guests"),
    ("Sala zabaw „Zatoczka Cydrowa” i bezpieczny ogród", "The “Zatoczka Cydrowa” playroom and a safe garden"),
    ("Plac zabaw w ogrodzie i kameralna sala zabaw na deszczowe dni — tak, żeby dzieci miały co robić niezależnie od pogody.", "A garden playground and a cosy indoor playroom for rainy days — so kids always have something to do, whatever the weather."),
    ("Plac zabaw w ogrodzie i kameralna sala zabaw na deszczowe dni — dzieci mają co robić niezależnie od pogody, a rodzice mogą odpocząć.", "A garden playground and a cosy indoor playroom for rainy days — kids always have something to do, whatever the weather, and parents can relax."),
    ("kameralna, bezpieczna przestrzeń na deszczowe dni", "a cosy, safe space for rainy days"),
    ("huśtawki i zjeżdżalnie na świeżym powietrzu", "swings and slides in the fresh air"),
    ("Kino letnie", "Summer cinema"),
    ("wieczorne seanse w sezonie dla całej rodziny", "evening screenings in season for the whole family"),
    ("Ogrodzony, monitorowany teren", "Fenced, monitored grounds"),
    ("spokój dla rodziców podczas zabawy dzieci", "peace of mind for parents while the kids play"),
    ("Rodzinna atmosfera", "Family atmosphere"),
    ("Co znajdziesz w strefie dla dzieci", "What you'll find in our kids' zone"),
    ("Sala zabaw „Zatoczka Cydrowa”", "The “Zatoczka Cydrowa” playroom"),
    ("Kameralna, bezpieczna przestrzeń na deszczowe dni.", "An intimate, safe space for rainy days."),
    ("Ogrodzony ogród i plac zabaw", "Fenced garden and playground"),
    ("Dzieci bezpiecznie bawią się na świeżym powietrzu, rodzice mogą odpocząć na tarasie.", "Kids play safely outdoors, while parents relax on the terrace."),
    ("Bezpieczna strefa malucha", "A safe zone for little ones"),
    ("Plac zabaw w ogrodzie", "Garden playground"),
    ("Zobacz strefę dla dzieci", "See the kids' zone"),

    # ---- Location section ----
    ("Stegna, Żuławy Wiślane", "Stegna, Żuławy Wiślane"),
    ("Zatoka Cydrowa — blisko wszystkiego, a jednak w leśnej ciszy", "Zatoka Cydrowa — close to everything, yet quiet in the forest"),
    ("Obiekt leży w spokojnej, zalesionej części Stegny — 1500 metrów od piaszczystej plaży Bałtyku, z łatwym dojazdem do okolicznych atrakcji Żuław i Mierzei Wiślanej.", "The property sits in a quiet, forested part of Stegna — 1500 metres from the sandy Baltic beach, with easy access to the nearby attractions of the Żuławy region and the Vistula Spit."),
    ("do plaży w Stegnie", "to the beach in Stegna"),
    ("do centrum miejscowości", "to the town centre"),
    ("do Krynicy Morskiej", "to Krynica Morska"),
    ("zjazd z trasy S7", "exit from route S7"),
    ("zjazd z trasy S7 (Nowy Dwór Gdański)", "exit from route S7 (Nowy Dwór Gdański)"),
    ("na miejscu, monitorowany", "on site, monitored"),
    ("Lokalizacja i dojazd", "Location & directions"),
    ("Stegna, ul. Grunwaldzka — cisza sosnowego lasu i bliskość plaży", "Stegna, Grunwaldzka St. — quiet pine forest, close to the beach"),
    ("Otwórz trasę w Google Maps", "Open route in Google Maps"),
    ("Mapa dojazdu — Zatoka Cydrowa, ul. Grunwaldzka 12, Stegna", "Directions map — Zatoka Cydrowa, Grunwaldzka 12, Stegna"),

    # ---- Reviews ----
    ("Zaufanie gości", "Guest trust"),
    ("Goście mówią najlepiej", "Our guests say it best"),
    ("Prawdziwe opinie naszych gości z Facebooka.", "Real reviews from our guests on Facebook."),
    ("„Pobyt w Zatoce Cydrowej był wspaniały. Obiekt jest super, położony w spokojnym miejscu, idealnym na odpoczynek. Gospodarze są fantastyczni — bardzo serdeczni i pomocni, dzięki czemu od razu można poczuć się jak u siebie. Ogromnym atutem jest relaks w jacuzzi, który był świetnym dopełnieniem wypoczynku. Zdecydowanie polecam to miejsce każdemu, kto szuka spokoju, komfortu i miłej atmosfery. Na pewno jeszcze tu wrócimy!”", "“Our stay at Zatoka Cydrowa was wonderful. The place is great, in a quiet spot perfect for relaxing. The hosts are fantastic — very warm and helpful, so you feel at home right away. A huge plus was relaxing in the jacuzzi, a great finishing touch to the holiday. I'd definitely recommend this place to anyone looking for peace, comfort and a lovely atmosphere. We'll definitely be back!”"),
    ("„Do tego opalenizna z solarium, gorący powiew z sauny — człowiek od razu zapomina, że nad Bałtykiem właśnie pada. Dzieci mają tutaj swój raj — bilard, kino i plac zabaw sprawiają, że każdy znajdzie coś dla siebie. A wszystko to w atmosferze, która jest naprawdę domowa, ciepła i pełna serdeczności. Ogromne podziękowania dla Klaudii i Łukasza — to prawdziwi ludzie o wielkich serduchach. Zatoka Cydrowa — zdecydowanie miejsce, do którego chce się wracać!”", "“A tan from the solarium, a hot blast from the sauna — you instantly forget it's raining by the Baltic. Kids have their own paradise here — a pool table, cinema and playground mean everyone finds something for themselves. And all of it in an atmosphere that's genuinely warm, homely and full of kindness. Huge thanks to Klaudia and Łukasz — truly big-hearted people. Zatoka Cydrowa is definitely a place you want to come back to!”"),
    ("„Jeśli szukacie idealnego miejsca na odpoczynek nad morzem, to Zatoka Cydrowa jest strzałem w dziesiątkę. Gwarancja relaksu na najwyższym poziomie. Pokoje lśnią czystością, są urządzone ze smakiem i bardzo przytulne. Właściciele i Gospodarze to niezwykle ciepli, pomocni i mega pozytywnie zakręceni ludzie, którzy dbają o każdy szczegół i sprawiają, że człowiek czuje się jak w domu. Rewelacyjne miejsce, do którego jeszcze nie raz wrócimy.”", "“If you're looking for the perfect place to relax by the sea, Zatoka Cydrowa is a bullseye. Top-level relaxation, guaranteed. The rooms are spotless, tastefully furnished and very cosy. The owners and hosts are incredibly warm, helpful and wonderfully upbeat people who care about every detail and make you feel right at home. A fantastic place we'll be returning to again and again.”"),
    ("Lokalny przewodnik Google", "Local Guide, Google"),
    ("Zobacz więcej opinii na Facebooku →", "See more reviews on Facebook →"),

    # ---- FAQ ----
    ("Najczęstsze pytania", "Frequently asked questions"),
    ("Pytania i odpowiedzi", "Questions & answers"),

    # ---- CTA ----
    ("Gotowi na wypoczynek nad Bałtykiem?", "Ready for a holiday by the Baltic?"),
    ("Sprawdźcie dostępność telefonicznie — odpowiemy na wszystkie pytania o apartamenty i termin przyjazdu.", "Check availability by phone — we'll answer every question about the apartments and your dates."),
    ("Facebook", "Facebook"),
    ("Zaplanujcie rodzinny wypoczynek nad Bałtykiem", "Plan your family holiday by the Baltic"),
    ("Zadzwońcie i zapytajcie o dostępny termin — chętnie doradzimy, który apartament sprawdzi się dla Waszej rodziny.", "Give us a call and ask about available dates — we'll gladly help you choose the apartment that suits your family best."),
    ("Zobacz dane kontaktowe", "See contact details"),

    # ---- Footer ----
    ("Apartamenty i domki w Stegnie, 1500 m od plaży Bałtyku, w otoczeniu sosnowego lasu.", "Apartments and cottages in Stegna, 1500 m from the Baltic beach, surrounded by pine forest."),
    ("Apartamenty i pokoje", "Apartments & rooms"),
    ("Strefa wellness i atrakcje", "Wellness zone & attractions"),
    ("Informacje", "Information"),

    # ---- Contact page ----
    ("Skontaktuj się z nami", "Get in touch"),
    ("Zadzwoń lub napisz na Messengerze — odpowiadamy zwykle w kilkanaście minut, codziennie w godzinach 8:00–20:00.", "Call us or message us on Messenger — we usually reply within minutes, every day from 8:00 AM to 8:00 PM."),
    ("Napisz lub zadzwoń", "Message or call us"),
    ("Najszybciej odpowiadamy na telefon i Messengera.", "We respond fastest to phone calls and Messenger."),
    ("Zadzwoń: 797 315 001", "Call: +48 797 315 001"),
    ("Napisz na Messengerze", "Message on Messenger"),
    ("facebook.com/ZatokaCydrowa", "facebook.com/ZatokaCydrowa"),
    ("Mierzeja Wiślana", "Vistula Spit"),
    ("1500 m do morza", "1500 m to the sea"),
    ("Zatoka Cydrowa mieści się przy ul. Grunwaldzkiej 12 w Stegnie — blisko piaszczystej plaży i leśnych ścieżek spacerowych.", "Zatoka Cydrowa is located at Grunwaldzka 12 in Stegna — close to the sandy beach and forest walking trails."),

    # ---- Privacy policy ----
    ("Administrator danych:", "Data controller:"),
    ("właściciel obiektu Zatoka Cydrowa, ul. Grunwaldzka 12, 82-103 Stegna, tel. 797 315 001, e-mail: kontakt@zatokacydrowa.pl.", "the owner of the Zatoka Cydrowa property, Grunwaldzka 12, 82-103 Stegna, Poland, phone +48 797 315 001, email: kontakt@zatokacydrowa.pl."),
    ("Jakie dane zbieramy", "What data we collect"),
    ("Serwis nie posiada formularza kontaktowego i sam nie zbiera ani nie przechowuje danych osobowych odwiedzających. Kontakt odbywa się bezpośrednio telefonicznie (połączenie lub SMS z Twojego urządzenia) albo przez Messenger na Facebooku — w obu przypadkach dane, które nam przekazujesz (np. imię, numer telefonu, treść wiadomości), trafiają do nas za pośrednictwem operatora telekomunikacyjnego lub platformy Meta, a nie przez naszą stronę.", "This site has no contact form and does not itself collect or store visitors' personal data. Contact happens directly by phone (a call or SMS from your own device) or via Messenger on Facebook — in both cases, the data you share with us (e.g. name, phone number, message content) reaches us through your telecom operator or the Meta platform, not through our website."),
    ("Cel przetwarzania danych", "Purpose of processing"),
    ("Dane przekazane nam telefonicznie lub przez Messenger przetwarzamy wyłącznie w celu odpowiedzi na zapytanie dotyczące oferty i rezerwacji noclegu (art. 6 ust. 1 lit. b i f RODO — działania przed zawarciem umowy oraz prawnie uzasadniony interes administratora).", "Data you share with us by phone or Messenger is processed solely to respond to enquiries about our offer and bookings (Art. 6(1)(b) and (f) GDPR — pre-contractual measures and the controller's legitimate interest)."),
    ("Okres przechowywania", "Retention period"),
    ("Dane przechowywane są przez okres niezbędny do obsługi zapytania i ewentualnej rezerwacji, nie dłużej niż 3 lata od ostatniego kontaktu, chyba że przepisy prawa (np. podatkowe) wymagają dłuższego okresu przechowywania.", "Data is kept for as long as necessary to handle the enquiry and any resulting booking, for no longer than 3 years from the last contact, unless the law (e.g. tax regulations) requires a longer retention period."),
    ("Odbiorcy danych", "Data recipients"),
    ("Wiadomości wysyłane przez Messenger są przekazywane za pośrednictwem platformy Meta (Facebook) — zasady przetwarzania danych w ramach tej usługi określa polityka prywatności Meta. Połączenia i SMS-y obsługuje Twój operator telekomunikacyjny.", "Messages sent via Messenger are carried through the Meta (Facebook) platform — data processing for that service is governed by Meta's own privacy policy. Calls and SMS messages are handled by your telecom operator."),
    ("Prawa użytkownika", "Your rights"),
    ("Masz prawo dostępu do swoich danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przenoszenia danych oraz wniesienia sprzeciwu wobec przetwarzania, a także prawo wniesienia skargi do Prezesa Urzędu Ochrony Danych Osobowych. W tym celu skontaktuj się z nami mailowo: kontakt@zatokacydrowa.pl.", "You have the right to access, rectify, erase and restrict the processing of your data, to data portability, to object to processing, and to lodge a complaint with the President of the Personal Data Protection Office (Poland). To exercise these rights, contact us by email: kontakt@zatokacydrowa.pl."),
    ("Pliki cookies", "Cookies"),
    ("Serwis może wykorzystywać niezbędne pliki cookies do prawidłowego działania strony. Nie wykorzystujemy plików cookies do profilowania reklamowego.", "This site may use essential cookies required for it to function correctly. We do not use cookies for advertising profiling."),

    # ---- Booking sidebar / shared booking blocks ----
    ("Rezerwacja telefoniczna", "Book by phone"),
    ("Klimatyzowany", "Air-conditioned"),
    ("Zobacz wszystkie zdjęcia", "See all photos"),
    ("powierzchnia", "floor area"),
    ("maks. gości", "max. guests"),
    ("niezależne łazienki", "independent bathrooms"),
    ("<span>łazienka</span>", "<span>bathroom</span>"),
    ("<span>łazienki</span>", "<span>bathrooms</span>"),
    ("klimatyzowany", "air-conditioned"),
    ("★ Całoroczny komfort · Mierzeja Wiślana", "★ Year-round comfort · Vistula Spit"),
    ("Taras z zejściem do ogrodu", "Terrace with access to the garden"),
    ("Główna sypialnia</span>", "Main bedroom</span>"),
    ("Komfort dla wymagających", "Comfort for discerning guests"),
    ("Kameralny komfort", "Cosy comfort"),
    ("Przestrzeń dla dużych grup", "Room for larger groups"),
    ("2 niezależne łazienki — zero kolejek", "2 independent bathrooms — no more queues"),
    ("Duży aneks kuchenny i jadalnia", "A large kitchenette and dining area"),
    ("W pełni wyposażona kuchnia oraz stół jadalny dla całej grupy — idealne miejsce na wspólne posiłki po dniu spędzonym na plaży.", "A fully equipped kitchen and a dining table for the whole group — the perfect spot for shared meals after a day at the beach."),
    ("W pełni wyposażony aneks kuchenny", "Fully equipped kitchenette"),
    ("Salon z rozkładaną sofą", "Living room with a sofa bed"),
    ("Dodatkowe miejsce do spania w salonie, telewizor oraz stół jadalny — wygodna przestrzeń wspólna dla całej grupy.", "An extra sleeping spot in the living room, a TV and a dining table — a comfortable shared space for the whole group."),
    ("Lodówka, płyta indukcyjna, czajnik, ekspres do kawy i pełny zestaw naczyń — wszystko, czego potrzeba do samodzielnego przygotowania posiłków.", "Fridge, induction hob, kettle, coffee machine and a full set of dishes — everything you need to cook for yourselves."),
    ("Osobna sypialnia", "Separate bedroom"),
    ("Oddzielna sypialnia z podwójnym łożem, zapewniająca prywatność niezależnie od salonu i strefy dziennej.", "A separate bedroom with a double bed, giving you privacy away from the living room and day area."),
    ("Funkcjonalny aneks kuchenny", "A functional kitchenette"),
    ("Rozkład pomieszczeń i stref spania", "Room layout and sleeping areas"),
    ("Zwierzęta domowe są u nas mile widziane!", "Pets are welcome with us!"),
    ("Nie musisz rozstawać się ze swoim psem lub kotem na czas wakacji.", "No need to leave your dog or cat behind during your holiday."),
    ("Pet friendly", "Pet friendly"),
    ("Rezerwacja bezpośrednia u właściciela", "Direct booking with the owner"),
    ("Zadzwoń lub napisz bezpośrednio — bez marż portali pośredniczących.", "Call or message us directly — no booking-platform commission."),
    ("Napisz na WhatsApp", "Message on WhatsApp"),
    ("Wyślij szybki SMS z zapytaniem", "Send a quick SMS enquiry"),
    ("Napisz przez Messenger / Facebook", "Message via Messenger / Facebook"),
    ("Odbieramy natychmiast lub oddzwaniamy w kilkanaście minut", "We answer right away or call you back within minutes"),
    ("Codziennie w godzinach 8:00–20:00.", "Every day, 8:00 AM–8:00 PM."),
    ("Dlaczego warto rezerwować bezpośrednio?", "Why book directly?"),
    ("Bezpłatne miejsce parkingowe na zamkniętym, monitorowanym terenie", "Free parking in a gated, monitored area"),
    ("Pakiet powitalny gratis: kawa i herbata w apartamencie", "Free welcome pack: coffee and tea in the apartment"),
    ("Preferencyjne warunki na strefę wellness (sauna, komora hiperbaryczna)", "Preferential rates for the wellness zone (sauna, hyperbaric chamber)"),
    ("Możliwość wystawienia faktury VAT", "VAT invoice available on request"),
    ("✓ Gwarancja najniższej ceny · 0% prowizji", "✓ Best price guarantee · 0% commission"),
    ("Odkryj nasze pokoje", "Discover our rooms"),
    ("Zobacz także inne apartamenty w Zatoce Cydrowej", "See other apartments at Zatoka Cydrowa"),
    ("Wszystkie apartamenty →", "All apartments →"),
    ("Zobacz także pozostałe apartamenty letnie", "See our other summer apartments"),
    ("Wszystkie apartamenty letnie →", "All summer apartments →"),
    ("Szczegóły →", "Details →"),
    ("8-osobowy", "For 8"),
    ("5-osobowy", "For 5"),
    ("7-osobowy", "For 7"),
    ("4-osobowy", "For 4"),
    ("Apartament 1 (8-osobowy)", "Apartment 1 (for 8)"),
    ("Apartament 2 (5-osobowy)", "Apartment 2 (for 5)"),
    ("Apartament 3 (7-osobowy)", "Apartment 3 (for 7)"),
    ("Apartament 4 (4-osobowy)", "Apartment 4 (for 4)"),
    ("Przestronny apartament z tarasem i 2 łazienkami.", "A spacious apartment with a terrace and 2 bathrooms."),
    ("Komfortowy apartament z w pełni wyposażonym aneksem kuchennym.", "A comfortable apartment with a fully equipped kitchenette."),
    ("Dobry wybór dla dużych rodzin lub zorganizowanych grup.", "A great choice for large families or organised groups."),
    ("Kameralny apartament z osobną sypialnią, aneksem i łazienką.", "An intimate apartment with a separate bedroom, kitchenette and bathroom."),
    ("3 pokoje · 65 m²", "3 rooms · 65 m²"),
    ("2 pokoje · 35 m²", "2 rooms · 35 m²"),
    ("2 pokoje · 65 m²", "2 rooms · 65 m²"),
    ("Dwa pokoje, jadalnia i aneks kuchenny dla rodziny.", "Two rooms, a dining area and a kitchenette for the family."),
    ("Przytulny lokal dwuosobowy z prywatną łazienką.", "A cosy unit for two with a private bathroom."),
    ("Dla pary", "For couples"),
    ("Osobna sypialnia, pełne wyposażenie dla rodziny 2+2.", "Separate bedroom, full facilities for a family of 4."),
    ("2 sypialnie", "2 bedrooms"),

    # ---- Related-apartments room card labels ----
    ("Pomieszczenie", "Room"),
    ("osoby", "guests"),
    ("osoba", "guest"),
    ("osób", "guests"),
    ("jadalnia", "dining area"),

    # ---- Room / feature copy — Apartment 1 ----
    ("Całoroczny apartament w Stegnie dla 8 osób. Dobry wybór dla dwóch zaprzyjaźnionych rodzin lub grupy przyjaciół szukających wytchnienia pośród sosnowego lasu.", "A year-round apartment in Stegna for 8 guests. A great choice for two families travelling together, or a group of friends looking to unwind in a pine forest."),
    ("Apartament 1 – przestronny apartament 65 m² z tarasem i 2 łazienkami", "Apartment 1 – a spacious 65 m² apartment with a terrace and 2 bathrooms"),
    ("Przestrzeń, prywatność i wysoki standard w sercu leśnej Stegny", "Space, privacy and a high standard in the heart of forested Stegna"),
    ("Apartament 1 to jeden z najbardziej reprezentacyjnych lokali w kompleksie Zatoka Cydrowa — zaprojektowany z myślą o komforcie nawet 8 osób. To dobra przestrzeń dla dwóch zaprzyjaźnionych rodzin z dziećmi lub większej grupy bliskich, którzy chcą spędzić wspólny urlop nad Bałtykiem, zachowując przy tym pełną niezależność.", "Apartment 1 is one of the flagship units at Zatoka Cydrowa — designed with the comfort of up to 8 guests in mind. It's a great space for two families with children travelling together, or a larger group of friends who want to share a holiday by the Baltic while keeping full independence."),
    ("Słoneczny taras i ogród na wyciągnięcie ręki", "A sunny terrace and garden right outside the door"),
    ("Z salonu i z głównej sypialni prowadzi wyjście na obszerny taras z meblami wypoczynkowymi. Z tarasu bezpośrednie zejście do ogrodu z dwiema zadaszonymi altanami grillowymi i placem zabaw.", "Both the living room and the main bedroom open onto a large terrace with lounge furniture. From the terrace there's direct access to the garden, with two covered barbecue gazebos and a playground."),
    ("Dwie w pełni wyposażone, oddzielne łazienki z kabinami prysznicowymi i suszarkami. Przy 8-osobowym pobycie eliminuje to poranne i wieczorne kolejki.", "Two fully equipped, separate bathrooms with shower cubicles and hair dryers. With 8 guests staying together, this removes the morning and evening queues."),
    ("Główna sypialnia małżeńska", "Main double bedroom"),
    ("Duże łoże 2-osobowe, szafki nocne, szafa w zabudowie, bezpośrednie wyjście na taras.", "A large double bed, bedside tables, a built-in wardrobe, and direct access to the terrace."),
    ("Druga sypialnia twin", "Second, twin bedroom"),
    ("2 łóżka 1-osobowe z możliwością złączenia w podwójne. Biurko z krzesłem, okno na sosny.", "2 single beds that can be joined into a double. Desk with a chair, window overlooking the pines."),
    ("Salon z aneksem i tarasem", "Living room with kitchenette and terrace"),
    ("2 rozkładane sofy 2-osobowe, stół jadalny dla 8 osób, telewizor, aneks kuchenny.", "2 double sofa beds, a dining table for 8, a TV, and a kitchenette."),
    ("1× łoże 2-osobowe", "1× double bed"),
    ("2× łóżko 1-osobowe", "2× single bed"),
    ("2× rozkładana sofa 2-os.", "2× double sofa bed"),
    ("65 m²", "65 m²"),
    ("do 8 osób", "up to 8 guests"),
    ("3", "3"),
    ("pokoje (salon + 2 sypialnie)", "rooms (living room + 2 bedrooms)"),
    ("3 + 2", "3 + 2"),
    ("łóżka podwójne / pojedyncze", "double / single beds"),
    ("1. piętro", "1st floor"),
    ("z tarasem", "with a terrace"),

    # ---- Apartment 2 ----
    ("Całoroczny apartament w Stegnie dla 5 osób. Dobry wybór dla rodziny lub grupy przyjaciół szukających przytulnego, w pełni wyposażonego lokum blisko morza.", "A year-round apartment in Stegna for 5 guests. A great choice for a family or a group of friends looking for a cosy, fully equipped place close to the sea."),
    ("Apartament 2 – kameralny apartament 35 m² na piętrze", "Apartment 2 – an intimate 35 m² apartment on the upper floor"),
    ("Przytulna przestrzeń dla rodziny w sercu leśnej Stegny", "A cosy space for the family in the heart of forested Stegna"),
    ("Apartament 2 to kompaktowy, funkcjonalnie zaprojektowany lokal w kompleksie Zatoka Cydrowa — idealny dla 5-osobowej rodziny lub grupy przyjaciół. Osobna sypialnia i przestronny salon z aneksem kuchennym zapewniają wygodę bez rezygnacji z prywatności.", "Apartment 2 is a compact, thoughtfully designed unit at Zatoka Cydrowa — ideal for a family of 5 or a group of friends. A separate bedroom and a spacious living room with a kitchenette provide comfort without giving up privacy."),
    ("Salon z rozkładaną sofą", "Living room with a sofa bed"),
    ("Dodatkowe miejsce do spania w salonie, telewizor oraz stół jadalny — wygodna przestrzeń wspólna dla całej grupy.", "An extra sleeping spot in the living room, a TV and a dining table — a comfortable shared space for the whole group."),
    ("Sypialnia", "Bedroom"),
    ("Łoże 2-osobowe, szafa w zabudowie, okno na sosnowy las.", "A double bed, built-in wardrobe, window overlooking the pine forest."),
    ("Salon z aneksem kuchennym", "Living room with kitchenette"),
    ("Rozkładana sofa 3-osobowa, stół jadalny, telewizor, w pełni wyposażony aneks kuchenny.", "A three-seat sofa bed, dining table, TV, and a fully equipped kitchenette."),
    ("1× rozkładana sofa 3-os.", "1× three-seat sofa bed"),
    ("35 m²", "35 m²"),
    ("do 5 osób", "up to 5 guests"),
    ("2", "2"),
    ("pokoje (salon + sypialnia)", "rooms (living room + bedroom)"),
    ("1", "1"),
    ("1 + 1", "1 + 1"),
    ("łóżko podwójne / sofa rozkładana", "double bed / sofa bed"),
    ("2. piętro", "2nd floor"),

    # ---- Apartment 3 ----
    ("Całoroczny apartament w Stegnie dla 7 osób. Dobry wybór dla dużej rodziny lub zorganizowanej grupy szukającej wytchnienia pośród sosnowego lasu.", "A year-round apartment in Stegna for 7 guests. A great choice for a large family or an organised group looking to unwind in a pine forest."),
    ("Apartament 3 – przestronny apartament 65 m² z 2 łazienkami", "Apartment 3 – a spacious 65 m² apartment with 2 bathrooms"),
    ("Komfort i niezależność dla licznej rodziny w sercu leśnej Stegny", "Comfort and independence for a large family in the heart of forested Stegna"),
    ("Apartament 3 to obszerny lokal w kompleksie Zatoka Cydrowa, zaprojektowany z myślą o komforcie 7 osób. To dobra przestrzeń dla dużej rodziny lub zorganizowanej grupy, którzy chcą spędzić wspólny urlop nad Bałtykiem, zachowując przy tym pełną niezależność.", "Apartment 3 is a spacious unit at Zatoka Cydrowa, designed for the comfort of 7 guests. It's a great space for a large family or an organised group who want to share a holiday by the Baltic while keeping full independence."),
    ("Dwie w pełni wyposażone, oddzielne łazienki z kabinami prysznicowymi i suszarkami. Przy 7-osobowym pobycie eliminuje to poranne i wieczorne kolejki.", "Two fully equipped, separate bathrooms with shower cubicles and hair dryers. With 7 guests staying together, this removes the morning and evening queues."),
    ("Sypialnia główna", "Main bedroom"),
    ("Duże łoże 2-osobowe, szafki nocne, szafa w zabudowie, okno na sosny.", "A large double bed, bedside tables, a built-in wardrobe, window overlooking the pines."),
    ("2 rozkładane sofy, stół jadalny, telewizor, w pełni wyposażony aneks kuchenny.", "2 sofa beds, a dining table, a TV, and a fully equipped kitchenette."),
    ("2× rozkładana sofa", "2× sofa bed"),
    ("do 7 osób", "up to 7 guests"),
    ("2 + 2", "2 + 2"),
    ("łóżka podwójne / sofy rozkładane", "double beds / sofa beds"),

    # ---- Apartment 4 ----
    ("Całoroczny apartament w Stegnie dla 4 osób. Dobry wybór dla pary lub małej rodziny szukającej spokojnego wypoczynku pośród sosnowego lasu.", "A year-round apartment in Stegna for 4 guests. A great choice for a couple or a small family looking for a peaceful stay in a pine forest."),
    ("Apartament 4 – kameralny apartament 35 m² na piętrze", "Apartment 4 – an intimate 35 m² apartment on the upper floor"),
    ("Spokojna przystań dla pary lub małej rodziny w sercu leśnej Stegny", "A peaceful retreat for a couple or a small family in the heart of forested Stegna"),
    ("Apartament 4 to najbardziej kameralny lokal w kompleksie Zatoka Cydrowa — zaprojektowany z myślą o komforcie 4 osób. To dobra przestrzeń dla pary lub małej rodziny, którzy chcą spędzić spokojny urlop nad Bałtykiem, zachowując przy tym pełną prywatność.", "Apartment 4 is the most intimate unit at Zatoka Cydrowa — designed for the comfort of 4 guests. It's a great space for a couple or a small family who want a peaceful holiday by the Baltic with complete privacy."),
    ("Rozkładana sofa 2-osobowa, stół jadalny, telewizor, w pełni wyposażony aneks kuchenny.", "A double sofa bed, dining table, TV, and a fully equipped kitchenette."),
    ("1× rozkładana sofa 2-os.", "1× double sofa bed"),
    ("do 4 osób", "up to 4 guests"),

    # ---- Summer apartment 1 ----
    ("Kameralny apartament sezonowy w Stegnie: dwa pokoje, jadalnia i w pełni wyposażony aneks kuchenny — dobry wybór dla rodziny szukającej wygodnego noclegu blisko morza.", "An intimate seasonal apartment in Stegna: two rooms, a dining area and a fully equipped kitchenette — a great choice for a family looking for a comfortable stay close to the sea."),
    ("Apartament letni 1 – dwupokojowy lokal na wakacyjny wypoczynek", "Summer Apartment 1 – a two-room unit for a holiday break"),
    ("Jadalnia + aneks kuchenny", "Dining area + kitchenette"),
    ("Prosty, wygodny wypoczynek", "Simple, comfortable stay"),
    ("Kameralny lokal na letni urlop w sercu leśnej Stegny", "An intimate unit for a summer holiday in the heart of forested Stegna"),
    ("Apartament letni 1 to dwupokojowy lokal dostępny w sezonie letnim — dobra opcja dla rodziny szukającej prostego, wygodnego noclegu blisko morza. Jadalnia z aneksem kuchennym pozwala samodzielnie przygotować posiłki, a osobna sypialnia zapewnia spokojny wypoczynek.", "Summer Apartment 1 is a two-room unit available during the summer season — a good option for a family looking for a simple, comfortable stay close to the sea. The dining area with kitchenette lets you cook for yourselves, while the separate bedroom offers a peaceful night's sleep."),
    ("Jadalnia z aneksem kuchennym", "Dining area with kitchenette"),
    ("Miejsce do wspólnych posiłków oraz podstawowe wyposażenie kuchenne do samodzielnego gotowania.", "A place for shared meals, with basic kitchen equipment for cooking for yourselves."),
    ("Wydzielona strefa nocna, niezależna od jadalni i przestrzeni dziennej.", "A separate sleeping area, independent from the dining area and living space."),
    ("Osobna sypialnia z łożem 2-osobowym i szafą, niezależna od jadalni.", "A separate bedroom with a double bed and a wardrobe, independent from the dining area."),
    ("Stół jadalny i w pełni wyposażony aneks kuchenny do samodzielnego przygotowania posiłków.", "A dining table and a fully equipped kitchenette for cooking for yourselves."),
    ("Aneks kuchenny", "Kitchenette"),
    ("pokoje (jadalnia + sypialnia)", "rooms (dining area + bedroom)"),
    ("Sezon letni", "Summer season"),
    ("dostępność czerwiec–wrzesień", "available June–September"),
    ("w pełni wyposażony", "fully equipped"),

    # ---- Summer apartment 2 ----
    ("Kameralny apartament sezonowy w Stegnie z przytulnym łożem małżeńskim i prywatną łazienką — spokojny wypoczynek we dwoje blisko morza.", "An intimate seasonal apartment in Stegna with a cosy double bed and a private bathroom — a peaceful getaway for two, close to the sea."),
    ("Apartament letni 2 – przytulny lokal dla pary", "Summer Apartment 2 – a cosy unit for couples"),
    ("Prywatna łazienka", "Private bathroom"),
    ("Spokój we dwoje", "Peace for two"),
    ("Kameralna przystań dla pary w sercu leśnej Stegny", "An intimate retreat for a couple in the heart of forested Stegna"),
    ("Apartament letni 2 to najbardziej kameralny z naszych lokali sezonowych — przytulne łoże małżeńskie i prywatna łazienka tworzą spokojną przestrzeń do wypoczynku we dwoje, z dala od zgiełku.", "Summer Apartment 2 is the most intimate of our seasonal units — a cosy double bed and a private bathroom create a peaceful space for two, away from the noise."),
    ("Przytulne łoże małżeńskie", "A cosy double bed"),
    ("Komfortowa sypialnia zaprojektowana z myślą o spokojnym wypoczynku pary.", "A comfortable bedroom designed for a couple's peaceful rest."),
    ("Własna, w pełni wyposażona łazienka do wyłącznej dyspozycji gości.", "Your own fully equipped bathroom, for the exclusive use of guests."),
    ("Sypialnia z prywatną łazienką", "Bedroom with a private bathroom"),
    ("Przytulne łoże małżeńskie, szafa i bezpośrednie wejście do prywatnej łazienki.", "A cosy double bed, a wardrobe, and direct access to the private bathroom."),
    ("prywatna łazienka", "private bathroom"),
    ("Dla pary", "For couples"),

    # ---- Summer apartment 3 ----
    ("Apartament sezonowy w Stegnie utrzymany w kontrastowej, czarno-białej stylistyce z nastrojowym oświetleniem — dwie sypialnie, aneks kuchenny i łazienka.", "A seasonal apartment in Stegna with a contrasting black-and-white style and mood lighting — two bedrooms, a kitchenette and a bathroom."),
    ("Apartament letni 3 – stylowa, czarno-biała aranżacja", "Summer Apartment 3 – a stylish black-and-white interior"),
    ("Design-owy akcent w ofercie letniej", "A design-forward option in our summer offer"),
    ("Kontrastowa, czarno-biała aranżacja z nastrojowym światłem", "A contrasting black-and-white interior with mood lighting"),
    ("Apartament letni 3 wyróżnia się na tle pozostałych lokali sezonowych stylową, czarno-białą kolorystyką wnętrz. Dwie sypialnie, aneks kuchenny i łazienka tworzą kameralną, dobrze wyposażoną przestrzeń na letni wypoczynek.", "Summer Apartment 3 stands out among our seasonal units with its stylish black-and-white interior. Two bedrooms, a kitchenette and a bathroom form an intimate, well-equipped space for a summer stay."),
    ("Stylowe, czarno-białe wnętrze", "A stylish black-and-white interior"),
    ("Kontrastowa aranżacja z nastrojowym oświetleniem — wyróżniający się charakter wśród naszych lokali letnich.", "A contrasting design with mood lighting — a distinctive character among our summer units."),
    ("Dwie sypialnie", "Two bedrooms"),
    ("Dodatkowa przestrzeń nocna, dobra opcja dla dwóch par lub rodziny z dziećmi.", "Extra sleeping space, a good option for two couples or a family with children."),
    ("Czarno-biała aranżacja z nastrojowym oświetleniem, łoże 2-osobowe.", "A black-and-white interior with mood lighting, a double bed."),
    ("Druga sypialnia", "Second bedroom"),
    ("Dodatkowa przestrzeń nocna w tej samej stylistyce — dobra opcja dla dwóch par lub rodziny z dziećmi.", "Extra sleeping space in the same style — a good option for two couples or a family with children."),
    ("W pełni wyposażony aneks kuchenny w tej samej stylistyce, miejsce do przygotowania posiłków.", "A fully equipped kitchenette in the same style, a place to prepare meals."),
    ("sypialnie", "bedrooms"),

    # ---- Summer apartment 4 ----
    ("Apartament sezonowy w Stegnie z osobną sypialnią i pełnym wyposażeniem — dobry wybór dla rodziny z dziećmi na letni wypoczynek blisko morza.", "A seasonal apartment in Stegna with a separate bedroom and full facilities — a great choice for a family with children on a summer break close to the sea."),
    ("Apartament letni 4 – pełne wyposażenie dla rodziny 2+2", "Summer Apartment 4 – full facilities for a family of 4"),
    ("Osobna sypialnia", "Separate bedroom"),
    ("Dla rodziny 2+2", "For a family of 4"),
    ("Wygodny lokal sezonowy dla małej rodziny", "A comfortable seasonal unit for a small family"),
    ("Apartament letni 4 to dobrze wyposażony lokal sezonowy z osobną sypialnią — myślany z myślą o rodzinach 2+2 szukających wygodnego noclegu na letni wyjazd nad Bałtyk.", "Summer Apartment 4 is a well-equipped seasonal unit with a separate bedroom — designed for families of 4 looking for a comfortable stay on a summer trip to the Baltic."),
    ("Wydzielona strefa nocna, niezależna od przestrzeni dziennej.", "A separate sleeping area, independent from the living space."),
    ("Dobrze wyposażony dla rodzin", "Well equipped for families"),
    ("Pełne wyposażenie potrzebne na letni pobyt z dziećmi.", "Everything you need for a summer stay with children."),
    ("Wydzielona strefa nocna z łożem 2-osobowym, niezależna od przestrzeni dziennej.", "A separate sleeping area with a double bed, independent from the living space."),
    ("Przestrzeń dzienna", "Living space"),
    ("Salon z rozkładaną sofą — dobre rozwiązanie na nocleg dla dzieci przy rodzinie 2+2.", "A living room with a sofa bed — a good sleeping solution for children in a family of 4."),
    ("osobna sypialnia", "separate bedroom"),

    # ---- Alt text (apartment galleries) ----
    ("Apartament 1 — Zatoka Cydrowa", "Apartment 1 — Zatoka Cydrowa"),
    ("Apartament 2 — Zatoka Cydrowa", "Apartment 2 — Zatoka Cydrowa"),
    ("Apartament 3 — Zatoka Cydrowa", "Apartment 3 — Zatoka Cydrowa"),
    ("Apartament 4 — Zatoka Cydrowa", "Apartment 4 — Zatoka Cydrowa"),
    ("Salon i jadalnia — Apartament 1, Zatoka Cydrowa", "Living room & dining area — Apartment 1, Zatoka Cydrowa"),
    ("Salon &amp; jadalnia", "Living room &amp; dining area"),
    ("Główna sypialnia — Apartament 1", "Main bedroom — Apartment 1"),
    ("Druga sypialnia — Apartament 1", "Second bedroom — Apartment 1"),
    ("Taras — Apartament 1", "Terrace — Apartment 1"),
    ("Taras", "Terrace"),
    ("Salon z aneksem — Apartament 2, Zatoka Cydrowa", "Living room with kitchenette — Apartment 2, Zatoka Cydrowa"),
    ("Salon &amp; aneks kuchenny", "Living room &amp; kitchenette"),
    ("Sypialnia — Apartament 2", "Bedroom — Apartment 2"),
    ("<span>Łazienka</span>", "<span>Bathroom</span>"),
    ("<span>łazienka</span>", "<span>bathroom</span>"),
    ("Łazienka — Apartament 2", "Bathroom — Apartment 2"),
    ("Balkon — Apartament 2", "Balcony — Apartment 2"),
    ("Balkon", "Balcony"),
    ("Salon i jadalnia — Apartament 3, Zatoka Cydrowa", "Living room & dining area — Apartment 3, Zatoka Cydrowa"),
    ("Salon — Apartament 3", "Living room — Apartment 3"),
    ("Salon", "Living room"),
    ("Taras — Apartament 3", "Terrace — Apartment 3"),
    ("Łazienka — Apartament 3", "Bathroom — Apartment 3"),
    ("Salon z aneksem — Apartament 4, Zatoka Cydrowa", "Living room with kitchenette — Apartment 4, Zatoka Cydrowa"),
    ("Sypialnia — Apartament 4", "Bedroom — Apartment 4"),
    ("Łazienka — Apartament 4", "Bathroom — Apartment 4"),
    ("Balkon — Apartament 4", "Balcony — Apartment 4"),
    ("Jadalnia i aneks kuchenny — Apartament letni 1, Zatoka Cydrowa", "Dining area & kitchenette — Summer Apartment 1, Zatoka Cydrowa"),
    ("Jadalnia &amp; aneks kuchenny", "Dining area &amp; kitchenette"),
    ("Sypialnia — Apartament letni 1", "Bedroom — Summer Apartment 1"),
    ("Przestrzeń dzienna — Apartament letni 1", "Living space — Summer Apartment 1"),
    ("Przestrzeń dzienna", "Living space"),
    ("Sypialnia — Apartament letni 2, Zatoka Cydrowa", "Bedroom — Summer Apartment 2, Zatoka Cydrowa"),
    ("Aneks kuchenny — Apartament letni 2", "Kitchenette — Summer Apartment 2"),
    ("Aneks kuchenny", "Kitchenette"),
    ("Sypialnia — Apartament letni 3, Zatoka Cydrowa", "Bedroom — Summer Apartment 3, Zatoka Cydrowa"),
    ("Druga sypialnia — Apartament letni 3", "Second bedroom — Summer Apartment 3"),
    ("Aneks kuchenny — Apartament letni 3", "Kitchenette — Summer Apartment 3"),
    ("Aneks kuchenny i jadalnia — Apartament letni 4, Zatoka Cydrowa", "Kitchenette & dining area — Summer Apartment 4, Zatoka Cydrowa"),
    ("Aneks kuchenny &amp; jadalnia", "Kitchenette &amp; dining area"),
    ("Sypialnia — Apartament letni 4", "Bedroom — Summer Apartment 4"),
    ("Łazienka — Apartament letni 4", "Bathroom — Summer Apartment 4"),
    ("Mieszkania letnie — Zatoka Cydrowa", "Summer rooms — Zatoka Cydrowa"),
    ("Apartament letni 1 — Zatoka Cydrowa", "Summer Apartment 1 — Zatoka Cydrowa"),
    ("Apartament letni 3 — Zatoka Cydrowa", "Summer Apartment 3 — Zatoka Cydrowa"),
    ("Apartament letni 4 — Zatoka Cydrowa", "Summer Apartment 4 — Zatoka Cydrowa"),
    ("Sala zabaw Zatoczka Cydrowa — wnętrze", "Zatoczka Cydrowa playroom — interior"),
    ("Sala zabaw Zatoczka Cydrowa — zabawki", "Zatoczka Cydrowa playroom — toys"),
    ("Sala zabaw Zatoczka Cydrowa — kącik dla dzieci", "Zatoczka Cydrowa playroom — kids' corner"),
    ("Plac zabaw w ogrodzie Zatoki Cydrowej", "Playground in the Zatoka Cydrowa garden"),
    ("Dekoracje w ogrodzie Zatoki Cydrowej", "Garden decorations at Zatoka Cydrowa"),
    ("Kino letnie w ogrodzie Zatoki Cydrowej", "Summer cinema in the Zatoka Cydrowa garden"),
    ("Dla dzieci — ", "For kids — "),

    # ---- Lightbox / gallery counters (dynamic, handled by JS but static fallback text) ----
    ("Zamknij galerię", "Close gallery"),
    ("Poprzednie zdjęcie", "Previous photo"),
    ("Następne zdjęcie", "Next photo"),
    ("Zdjęcie 1 / 6", "Photo 1 / 6"),
    ("Zdjęcie 1 / 5", "Photo 1 / 5"),
    ("Zdjęcie 1 / 7", "Photo 1 / 7"),
    ("Zdjęcie 1 / 4", "Photo 1 / 4"),
    ("Zdjęcie 1 / 3", "Photo 1 / 3"),
    ("Zdjęcie 1 / 2", "Photo 1 / 2"),
    ("Zdjęcie 1 / 18", "Photo 1 / 18"),
]
DICT.sort(key=lambda p: -len(p[0]))

# mieszkania-letnie.html gallery alt texts "Mieszkania letnie — zdjęcie N"
for i in range(1, 19):
    DICT.insert(0, (f"Mieszkania letnie — zdjęcie {i}", f"Summer rooms — photo {i}"))
DICT.sort(key=lambda p: -len(p[0]))


GALLERY_PATH_RE = re.compile(r'(?:\.\./)*gallery/[\w\-./]+\.(?:webp|jpg|jpeg|png)')


def protect_gallery_paths(html: str):
    """Image filenames (e.g. Sypialnia-czarno-bialy.webp) can contain words
    that are also dictionary entries (Sypialnia -> Bedroom). Stash every
    gallery/* path behind a placeholder before translating so the
    dictionary can't rewrite a real file path."""
    mapping = {}

    def repl(m):
        key = f"\x00GALLERY{len(mapping)}\x00"
        mapping[key] = m.group(0)
        return key

    return GALLERY_PATH_RE.sub(repl, html), mapping


def restore_gallery_paths(html: str, mapping: dict) -> str:
    for key, value in mapping.items():
        html = html.replace(key, value)
    return html


def translate(text: str) -> str:
    text, mapping = protect_gallery_paths(text)
    for pl, en in DICT:
        if pl in text:
            text = text.replace(pl, en)
    return restore_gallery_paths(text, mapping)


def rel_depth(path: str) -> int:
    return path.count("/")


def add_asset_prefix(html: str) -> str:
    """From an /en/... file, shared assets (css/js/icons/gallery) live one
    directory level further up than they did from the original PL file.
    Uses placeholders so a "../x" match can't be re-matched by the plain "x" pass."""
    PH = "\x00EN_UP\x00"
    # First: mark already-relative ("../") references so the later plain-prefix
    # substitutions can't double-apply to them.
    html = html.replace('href="../css/style.css"', f'href="{PH}css/style.css"')
    html = html.replace('href="../icons.svg', f'href="{PH}icons.svg')
    html = html.replace('src="../gallery/', f'src="{PH}gallery/')
    html = html.replace('"../gallery/', f'"{PH}gallery/')
    html = html.replace('src="../js/main.js"', f'src="{PH}js/main.js"')
    # Then: add one level to the still-plain (top-level-page) references.
    html = re.sub(r'href="css/style\.css"', 'href="../css/style.css"', html)
    html = re.sub(r'href="icons\.svg', 'href="../icons.svg', html)
    html = re.sub(r'src="gallery/', 'src="../gallery/', html)
    html = re.sub(r'"gallery/', '"../gallery/', html)
    html = re.sub(r'src="js/main\.js"', 'src="../js/main.js"', html)
    # Finally: resolve placeholders to the doubled-up path.
    html = html.replace(PH, "../../")
    return html


def fix_urls(html: str, rel_path: str) -> str:
    """og:url -> /en/<rel_path>. Only touches content=... (meta og:url), never
    href=..., so it can't collide with the hreflang <link> tags, which must
    keep pointing at both languages' canonical URLs in every file."""
    html = html.replace(
        f'content="https://zatokacydrowa.pl/{rel_path}"',
        f'content="https://zatokacydrowa.pl/en/{rel_path}"',
    )
    if rel_path == "index.html":
        html = html.replace(
            'content="https://zatokacydrowa.pl/"', 'content="https://zatokacydrowa.pl/en/"'
        )
    return html


def fix_jsonld_breadcrumbs(html: str) -> str:
    # Any breadcrumb / containedInPlace URL pointing at the PL site should point at /en/ instead,
    # except the bare homepage url used as the business URL (kept as canonical PL business record).
    def repl(m):
        url = m.group(1)
        if url == "https://zatokacydrowa.pl/":
            return m.group(0)  # containedInPlace business URL: keep pointing at canonical PL homepage
        if url.startswith("https://zatokacydrowa.pl/"):
            return f'"item": "https://zatokacydrowa.pl/en/{url[len("https://zatokacydrowa.pl/"):]}"'
        return m.group(0)
    html = re.sub(r'"item":\s*"(https://zatokacydrowa\.pl/[^"]*)"', repl, html)
    return html


def build_switcher_and_hreflang(rel_path: str):
    en_rel = "en/" + rel_path
    canonical_rel = "" if rel_path == "index.html" else rel_path
    en_canonical_rel = "en/" if rel_path == "index.html" else en_rel
    pl_url = f"https://zatokacydrowa.pl/{canonical_rel}"
    en_url = f"https://zatokacydrowa.pl/{en_canonical_rel}"
    depth = rel_depth(rel_path)
    to_en = ("../" * depth) + "en/" + rel_path if depth else "en/" + rel_path
    depth_en = rel_depth(en_rel)
    to_pl = ("../" * depth_en) + rel_path
    return pl_url, en_url, to_en, to_pl


def main():
    for rel in PAGES:
        src_path = os.path.join(ROOT, rel)
        with open(src_path, encoding="utf-8") as f:
            pl_html = f.read()

        pl_url, en_url, to_en, to_pl = build_switcher_and_hreflang(rel)
        x_default = pl_url if rel != "index.html" else "https://zatokacydrowa.pl/"

        # --- 1. Add hreflang + EN switch link to the ORIGINAL PL file (idempotent) ---
        if 'hreflang="en"' not in pl_html:
            hreflang_block = (
                f'<link rel="alternate" hreflang="pl" href="{pl_url}">\n'
                f'<link rel="alternate" hreflang="en" href="{en_url}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{x_default}">\n'
            )
            pl_html = pl_html.replace(
                f'<link rel="canonical" href="{pl_url}">\n',
                f'<link rel="canonical" href="{pl_url}">\n{hreflang_block}',
                1,
            )
            pl_html = pl_html.replace(
                '<button class="nav-toggle"',
                f'<a class="lang-switch" href="{to_en}" aria-label="Switch to English">EN</a>\n      <button class="nav-toggle"',
                1,
            )
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(pl_html)

        # --- 2. Build the EN file from the (now hreflang-tagged) PL source ---
        en_html = pl_html
        en_html = en_html.replace('lang="pl"', 'lang="en"', 1)
        en_html = en_html.replace(
            f'<link rel="canonical" href="{pl_url}">',
            f'<link rel="canonical" href="{en_url}">',
            1,
        )
        en_html = fix_urls(en_html, rel)
        en_html = fix_jsonld_breadcrumbs(en_html)
        en_html = add_asset_prefix(en_html)
        # language switch link now must point back to PL
        en_html = en_html.replace(
            f'<a class="lang-switch" href="{to_en}" aria-label="Switch to English">EN</a>',
            f'<a class="lang-switch" href="{to_pl}" aria-label="Przełącz na polski">PL</a>',
        )
        en_html = translate(en_html)

        out_path = os.path.join(ROOT, "en", rel)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(en_html)
        print("wrote", os.path.relpath(out_path, ROOT))


if __name__ == "__main__":
    main()
