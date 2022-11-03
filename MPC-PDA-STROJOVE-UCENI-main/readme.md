## Spuštění

- nainstalování potřebných balíčků `pip install numpy tensorflow scikit`
- nastavení požadovaného modelu v `server.py`
- spuštění serveru `python server.py`
- spuštění robocode

## Výsledky

Uvedena je úspěšnost střelby a počet výstřelů během 500 her.

| Protivník    | NN            | SVM           | KNN           |
| ------------ | ------------- | ------------- | ------------- |
| Sitting Duck | 99.9% (12507) | 98.7% (12566) | 99.6% (10795) |
| Walls        | 90.2% (5198)  | 23.2% (11027) | 37.2% (8369)  |
| Crazy        | 84.8% (11416) | 36.6% (21819) | 30.4% (26254) |
| Veloci Robot | 77.4% (2511)  | 40.0% (7012)  | 29.2% (17444) |
