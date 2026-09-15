# Zatoka Cydrowa — redesign, etap 1

## Co jest gotowe

- `index.html` — strona główna: hero, apartamenty całoroczne (realne dane: liczba osób, m², pokoje), apartamenty letnie, sekcja "dlaczego warto", wellness (komora hiperbaryczna / sauna / solarium), sekcja dla dzieci, okolica + mapa, CTA, stopka, sticky przycisk telefonu na mobile.
- `apartamenty/apartament-1.html` — **rozbudowany wzorzec** podstrony apartamentu wg Twojej karty: galeria bento z lightboxem, parametry kluczowe, opis, 2 karty "komfort", banner pet-friendly, rozkład pomieszczeń, sticky panel rezerwacji (telefon/WhatsApp/SMS/Messenger/e-mail), widget lokalizacji, mapa, karty pozostałych apartamentów. **Bez zakładki "kompletne wyposażenie" i bez sekcji "w cenie pobytu"/"na miejscu"** — usunięte na Twoją prośbę, żeby skrócić stronę.
  - Uwaga: adres w Twoim wzorze karty to `ul. Morska`, ale na żywej stronie WordPress widnieje `ul. Grunwaldzka 12` — użyłem tego drugiego (zweryfikowanego). Daj znać, jeśli to pomyłka.
  - E-mail `kontakt@zatokacydrowa.pl` w przyciskach rezerwacji jest przepisany z Twojej karty — potwierdź, czy to aktualna skrzynka.
- `css/style.css` — kompletny system: kolory, typografia (Playfair Display + Plus Jakarta Sans), komponenty (karty, przyciski, sekcje) — zgodny z paletą i tokenami z projektu Stitch (DESIGN.md).
- `js/main.js` — mobilne menu, animacja pojawiania się sekcji, brak zależności (czysty JS, bez frameworków).

Treści (opisy, metraże, adres, telefon) pochodzą z Twojej obecnej strony WordPress — nie są wymyślone.

## Czego jeszcze brakuje (kolejny etap)

1. **`apartamenty/apartament-2.html`, `-3.html`, `-4.html`** — na bazie nowego, rozbudowanego wzorca `apartament-1.html`, dane już mam (5/7/4 osoby, 35/65/35 m², rozkład pomieszczeń trzeba dopytać — mam tylko ogólne specyfikacje z WordPressa, nie podział na sypialnie jak w karcie).
2. **`kontakt.html`** — z prawdziwym formularzem (wymaga PHP albo zewnętrznej usługi typu Formspree/Web3Forms, bo czysty HTML nie wysyła maili).
3. **`dla-dzieci.html`**, strony wellness (komora/sauna/solarium), **`okolica.html`** z opisem atrakcji Stegny.
4. **Podmiana zdjęć na lokalne.** Na razie strona odwołuje się bezpośrednio do zdjęć na Twoim obecnym Hostingerze (`zatokacydrowa.pl/wp-content/uploads/...`), więc **działa już teraz**, ale docelowo warto:
   - ściągnąć pliki do `assets/images/`,
   - przekonwertować do WebP/AVIF i dodać wersje mniejsze (mobile),
   - podmienić `src` na lokalne ścieżki.
   Mogę to zrobić automatycznie, jeśli dasz mi dostęp do menedżera plików Hostingera (obecnie nie mam autoryzacji do odczytu Twojego konta — do ustawienia w connectorze).
5. **Przekierowania 301.** Obecne adresy WordPressa (`/osmioosobowy/`, `/piecioosobowy/`, `/kontakt/` itd.) są prawdopodobnie zaindeksowane w Google. Nowa struktura używa innych adresów (`/apartamenty/apartament-1.html`). Przy wdrożeniu **koniecznie** trzeba dodać przekierowania 301 w `.htaccess`, inaczej stracisz pozycje w wyszukiwarce. Mogę to przygotować razem z resztą plików.

## Struktura

```
index.html
kontakt.html            (do zrobienia)
dla-dzieci.html          (do zrobienia)
apartamenty/
  apartament-1.html      ✅ gotowe
  apartament-2.html       (do zrobienia)
  apartament-3.html       (do zrobienia)
  apartament-4.html       (do zrobienia)
css/style.css
js/main.js
assets/images/            (docelowe lokalne zdjęcia)
```

## Jak wdrożyć już teraz (podgląd)

To są zwykłe pliki statyczne — wystarczy wgrać zawartość folderu do `public_html` na Hostingerze (np. przez File Manager albo FTP) obok istniejącego WordPressa w osobnym podfolderze testowym, np. `public_html/nowa-strona/`, żeby obejrzeć bez ryzyka dla działającej strony.
