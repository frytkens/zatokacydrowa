# Zatoka Cydrowa — redesign, etap 2

## Co jest gotowe

- `index.html` — strona główna: hero, apartamenty całoroczne (realne dane: liczba osób, m², pokoje), apartamenty letnie, sekcja "dlaczego warto", wellness (komora hiperbaryczna / sauna / solarium), sekcja dla dzieci, okolica + mapa, CTA, stopka, sticky przycisk telefonu na mobile.
- `apartamenty/apartament-1.html`, `-2.html`, `-3.html`, `-4.html` — **wszystkie 4 apartamenty całoroczne** wg wzorca z Twojej karty: galeria bento z lightboxem, parametry kluczowe, opis, karty "komfort", banner pet-friendly, rozkład pomieszczeń, sticky panel rezerwacji (telefon/WhatsApp/SMS/Messenger/e-mail), widget lokalizacji, mapa, karty pozostałych apartamentów.
  - Uwaga: adres w Twoim wzorze karty to `ul. Morska`, ale na żywej stronie WordPress widnieje `ul. Grunwaldzka 12` — użyłem tego drugiego (zweryfikowanego). Daj znać, jeśli to pomyłka.
  - E-mail `kontakt@zatokacydrowa.pl` w przyciskach rezerwacji jest przepisany z Twojej karty — **wciąż niezweryfikowany, proszę potwierdzić czy to aktualna skrzynka.**
  - Rozkład pomieszczeń w apartamentach 2/3/4 jest opisany ogólnie na podstawie dostępnych specyfikacji (liczba osób/pokoi/m²) — jeśli masz dokładniejszy podział na sypialnie (jak w oryginalnej karcie apartamentu 1), daj znać, uzupełnię.
- `kontakt.html` — formularz kontaktowy oparty o **Web3Forms** (darmowa usługa wysyłki maili z formularzy statycznych, bez PHP). **Wymaga Twojej konfiguracji**: załóż darmowe konto na [web3forms.com](https://web3forms.com), wygeneruj Access Key i wklej go w `kontakt.html` w miejscu `WSTAW_TUTAJ_SWOJ_ACCESS_KEY_Z_WEB3FORMS` (linia z `<input type="hidden" name="access_key"...>`). Do tego czasu formularz pokazuje komunikat z prośbą o kontakt telefoniczny/mailowy zamiast wysyłać.
- `dla-dzieci.html` — strona sali zabaw „Zatoczka Cydrowa" i placu zabaw, z galerią.
- `polityka-prywatnosci.html` — podstawowa polityka prywatności (RODO) pod formularz kontaktowy.
- `.htaccess` — przekierowania 301 ze starych adresów WordPress (`/osmioosobowy/`, `/piecioosobowy/`, `/siedmioosobowy/`, `/czteroosobowy/`, `/kontakt/`) na nową strukturę. **Nie wgrywać na `nowa.zatokacydrowa.pl`** — ten plik jest przeznaczony na katalog główny domeny, dopiero przy przełączeniu domeny produkcyjnej na nową wersję (patrz komentarz w pliku).
- `css/style.css` — kompletny system: kolory, typografia (Playfair Display + Plus Jakarta Sans), komponenty (karty, przyciski, sekcje, formularz kontaktowy) — zgodny z paletą i tokenami z projektu Stitch (DESIGN.md).
- `js/main.js` — mobilne menu, animacja pojawiania się sekcji, brak zależności (czysty JS, bez frameworków).
- **Zdjęcia są teraz self-hostowane lokalnie** w katalogu `gallery/` (przeniesionym z Twojego archiwum Google Drive) — wszystkie odwołania `<img src>` zostały podmienione z zablokowanych linków `zatokacydrowa.pl/wp-content/...` na lokalne ścieżki względne (`gallery/apartament-1/...` itd.). To usuwa problem z Hotlink Protection Hostingera opisany niżej.

Treści (opisy, metraże, adres, telefon) pochodzą z Twojej obecnej strony WordPress — nie są wymyślone.

## Zdiagnozowany i naprawiony bug: zdjęcia się nie ładowały

Zdjęcia na `nowa.zatokacydrowa.pl` nie ładowały się, ponieważ Hotlink Protection Hostingera blokował żądania z subdomeny do zdjęć hostowanych na głównej domenie (traktowane jako różne hosty). Rozwiązanie: self-hosting zdjęć lokalnie w `gallery/` — wdrożone we wszystkich stronach w tym etapie.

## Czego jeszcze brakuje (kolejny etap)

1. **Strony wellness** (osobne podstrony komora/sauna/solarium) i **`okolica.html`** z rozbudowanym opisem atrakcji Stegny — obecnie te tematy są tylko sekcjami na stronie głównej (`index.html#wellness`, `index.html#okolica`).
2. **Konfiguracja Web3Forms** — patrz wyżej, formularz kontaktowy nie wyśle maila bez wklejonego Access Key.
3. **Potwierdzenie adresu e-mail** `kontakt@zatokacydrowa.pl` używanego w CTA rezerwacji i formularzu.
4. **Weryfikacja jakości/kompletności galerii** po stronie hostingu — lokalnie w repo katalog `gallery/` zawiera zdjęcia z Twojego archiwum Google Drive; jeśli po wgraniu na Hostinger struktura podfolderów będzie inna, trzeba będzie dopasować ścieżki w kodzie.

## Struktura

```
index.html
kontakt.html                     ✅ gotowe (wymaga klucza Web3Forms)
dla-dzieci.html                  ✅ gotowe
polityka-prywatnosci.html        ✅ gotowe
.htaccess                        ✅ gotowe (przekierowania 301)
apartamenty/
  apartament-1.html              ✅ gotowe
  apartament-2.html              ✅ gotowe
  apartament-3.html              ✅ gotowe
  apartament-4.html              ✅ gotowe
css/style.css
js/main.js
gallery/                         zdjęcia self-hostowane (z archiwum Google Drive)
```

## Jak wdrożyć już teraz (podgląd)

To są zwykłe pliki statyczne — wystarczy wgrać zawartość folderu do `public_html` na Hostingerze (np. przez File Manager albo FTP) obok istniejącego WordPressa w osobnym podfolderze testowym, np. `public_html/nowa-strona/`, żeby obejrzeć bez ryzyka dla działającej strony. **Nie wgrywaj `.htaccess`** dopóki nie przełączasz domeny głównej na nową wersję — patrz komentarz w tym pliku.
