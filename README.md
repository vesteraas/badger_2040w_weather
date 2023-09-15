# badger_2040w_weather

Bruk din Pimoroni Badger 2040W som værstasjon!

## Installasjon

Bruk Thonny eller lignende til å laste opp filene `main.py` og `display.py` til din Badger 2040W.  Om du ikke allerede
har gjort det, må du endre filen `WIFI_CONFIG.py` som allerede ligger på din Badger 2040W.  (Husk at `COUNTRY` også må
settes, ellers vil ikke programmet starte!)

Som standard vil programmet vise været for Oslo, og værdata vil hentes fire ganger i timen.  Du kan konfigurere både
posisjon og oppdateringsfrekvens med variablene `POSITION` og `UPDATES_PER_HOUR` i filen `main.py`.

## Feilsøking

Når du starter din Badger 2040W vil displayet blinke noen ganger, før værdata vises.  Hvis dette ikke skjer, så kan du
åpne filen `state/weather.py`, og se etter variabelen `last_error`.  Den vil fortelle hva som er feil.  Alternativet er
å kjøre programmet `main.py` direkte fra Thonny, og se etter feilmeldingen i konsollet.

Værdata hentes fra https://api.met.no