# 🐦 Flappy Bird in Python

Un clone del famoso gioco Flappy Bird realizzato in Python utilizzando PyGame. Progetto perfetto per chi ama i giochi e vuole programmare qualcosa in Python!

## 📋 Requisiti
- Python 3.x
- PyGame / pygame-ce (preferibile)

## 💻 Installazione

### Windows
1. Installa Python da [python.org](https://www.python.org/downloads/)
2. Apri il Prompt dei Comandi (cmd) come amministratore
3. Naviga nella cartella del gioco:
```cmd
cd percorso/alla/cartella/floppt-bird
```
4. Installa le librerie necessarie:
```cmd
pip install -r requirements.txt
```

### Mac/Linux
1. Apri il Terminale
2. Naviga nella cartella del gioco:
```bash
cd percorso/alla/cartella/floppt-bird
```
3. Installa le librerie necessarie:
```bash
python3 -m pip install -r requirements.txt
```

## 🎮 Come Giocare
1. Avvia il gioco:
   - Windows: `python main.py`
   - Mac/Linux: `python3 main.py`

2. Controlli:
   - SPAZIO: Salta
   - ESC: Pausa/Menu
   - Q: Esci dal gioco

## 🎵 Musica
- Individua la cartella `music`
- Inserisci i tuoi file musicali (.mp3, .wav, etc)
- Attiva/disattiva la musica dal menu di gioco

## 🛠️ Personalizzazione
Puoi modificare questi valori in `main.py`:
```python
BASE_SPEED = 3          # Velocità iniziale
SPEED_INCREASE = 0.4    # Aumento velocità per punto
MAX_SPEED = 12          # Velocità massima
GAP_HEIGHT = 180        # Spazio tra i tubi
```

## 📝 Licenza
Questo progetto è rilasciato sotto licenza [GNU GPL v3.0](LICENSE).

## 👥 Autore
Marco Carraro

## ❓ Problemi?
Se incontri problemi durante l'installazione:
1. Verifica di avere Python 3.x installato:
   - Windows: `python --version`
   - Mac/Linux: `python3 --version`
2. Aggiorna pip:
   - Windows: `python -m pip install --upgrade pip`
   - Mac/Linux: `python3 -m pip install --upgrade pip`
3. Prova a reinstallare le dipendenze
