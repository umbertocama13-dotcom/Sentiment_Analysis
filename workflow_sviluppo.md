# Deploy e monitoraggio di un modello di Sentiment Analysis per recensioni

## Passaggi per lo sviluppo del progetto

- Creare una cartella per il progetto e collegarla a github
- Verificare i requisiti minimi della consegna
- Dividere scripts e funzioni in modo da separare le logiche:
        - Service
        - Routes
        - Schemas
        - Tests
        - Monitoring
- Creare un venv in cui testare i componenti base del programma manualmente pezzo pezzo 
- Sviluppare in ordine:
        - Config del sistema di logging (utilizzato però solo nel main, le altre funzioni erano o troppo semplici, oppure già ben gestite da httpException)
        - Service e schema (logica cuore del progetto)
        - Esposizione della route con FastAPI
        - Creazione del main
        - Aggiunta del service per le metriche prometheus
        - Aggiunta della route delle metriche
        - Aggiornamento del main per includere le metriche
        - alert_rules.yml
        - prometheus.yml
        - dashboard.yml
        - datasource.yml
        - dashboard.json
        - Tests con pytest
        - File run.py
        - Dockerfile
        - Jenkinsfile
        - requirements.txt (si autopopola con il comando `pip freeze > requirements.txt`)
        - .dockerignore
        - .gitignore
        - README.md



## Scelte di sviluppo

### Logica di sviluppo
Si è tentato di dividere il più possibile il programma in sottocomponenti unitari, in modo da lasciare ogni funzione isolata e gestire tutto con le dipendenze (questa struttura mantiene logiche semplici da leggere e mantenere)

### Logica di funzionamento
- All'avvio dell'applicazione si apre con FastAPI un POST /predict
- Ad ogni richiesta il testo viene processato controllando se è in lingua inglese (se non lo è solleva un errore)
- Se è in lingua inglese viene predetta la sentiment "positive", "neutral" o "negative"
- In parallelo alla predizione vengono raccolte le metriche che sono poi esposte con un GET /metrics

### main.py
La logica del main è stata inglobata permettendo lo unittest su "startup_event" senza side effects; altrimenti il logger e il caricamento del modello verrebbero eseguiti al momento dell'importazione creando un fallimento del test. 
Alla fine viene istanziato l'entry point reale usato da uvicorn  **app = create_app()** 

### prometheus.yml
- scrape/evaluation interval a 15s (compromesso tra reattività e carico)
- rule_files punta alle alert rules per il controllo soglie
- scrape_configs punta a `app:8000/metrics`, dove "app" è il nome del servizio nel network Docker/Compose (non localhost)

### alert_rules.yml
- HighCPUUsage / HighMemoryUsage: warning se sopra 80% per più di 5m
- HighPredictionErrors: critical se >5 errori di predizione negli ultimi 5m (for: 0m, scatta subito)
- HighLatency: warning se il p95 della latenza supera 0.5s per più di 5m

### Grafana
Si è diviso il comportamento di grafana per riuscire ad automatizzare il caricamento senza dover passare per operazioni manuali; dashboard.yml e datasource.yml sono "istruzioni di configurazione automatica", mentre dashboard.json è il contenuto vero e proprio da visualizzare
**dashboard.json**
- 6 pannelli: gauge CPU/Memory (soglie verde <60%, giallo 60-80%, rosso >80%), timeseries Total Requests e Prediction Errors (rate 5m), stat Requests In Progress, timeseries Latency p95
- refresh 10s
**dashboard.yml**
- provisioning automatico: Grafana carica le dashboard da file (`/var/lib/grafana/dashboards`) invece che da import manuale via UI
**datasource.yml**
- provisioning automatico del datasource Prometheus, puntato su `http://prometheus:9090` (nome servizio nel network Docker)
- `isDefault: true` per non doverlo selezionare manualmente nei pannelli

### Docker
- Base image `python:3.11-slim` per ridurre dimensione
- requirements.txt copiato prima del codice per sfruttare cache Docker sulle dipendenze
- CMD con flag `-u` (unbuffered output): senza, i log restano nel buffer e non si vedono subito con `docker logs`, problema soprattutto per Jenkins/monitoring che leggono i log in tempo reale
- .dockerignore esclude venv, cache, test, log e file IDE/OS per ridurre il build context
**docker-compose**
Tiene insieme i 3 container (app, prometheus, grafana) come un unico sistema: li avvia con un solo comando, crea una rete condivisa dove si raggiungono per nome (es. `app:8000`, non `localhost`), e collega file di config esterni via volumi senza doverli inglobare nell'immagine
- 3 servizi: app, prometheus, grafana, collegati sullo stesso network di default
- app: build da Dockerfile, env da `.env`, volumi montati per hot-reload del codice senza rebuild
- prometheus: config e alert rules montate da file, `depends_on: app` per garantire ordine di avvio (non attesa readiness)
- grafana: provisioning e dashboard montati da file (vedi sezione Grafana)

### run.py
Entry point che avvia l'app con uvicorn (host/porta/config centralizzati in un unico file). 
Permette un comando di avvio semplice e uniforme (`python -u run.py`) invece di ripetere i 
parametri uvicorn in Dockerfile/Jenkinsfile/terminale ogni volta.

### Jenkinsfile
- 5 stage: Checkout (clone repo), Test (venv + pytest), Build Docker Image, Smoke Test, Deploy
- Smoke Test: avvia il container appena buildato e verifica con curl (/docs, /metrics, /predict) che ad alto livello il sistema funzioni e risponda prima di considerarlo deployabile; usa `--retry-connrefused` perché l'app impiega qualche secondo ad avviarsi; in ogni caso (successo o fallo) stampa i log e ferma il container di test
- `host.docker.internal` invece di `localhost`: necessario perché Jenkins gira in un container separato dall'app, quindi deve raggiungerla passando dall'host (setup specifico Docker Desktop/Mac)
- `export CXXFLAGS="-include cstdint"`: fix necessario per compilare una dipendenza C++ che altrimenti fallisce la build su questo ambiente
- Deploy: stop/rm del container precedente e riavvio con l'immagine appena testata
- Nessun rollback automatico in caso di fallimento del deploy: scelta accettabile per la scala del progetto, dato che lo Smoke Test blocca già in anticipo immagini rotte prima che arrivino al deploy vero. In un contesto di produzione reale andrebbe aggiunto (es. mantenendo il tag dell'immagine precedente e ripristinandolo in caso di fallimento del container in Deploy).
- Jenkins è containerizzato, per maggiori informazioni vedi README.md
**script_dockerfile.txt**
- Parte da `jenkins/jenkins:lts` e passa a `USER root` per poter installare pacchetti di sistema
- Installa Python3/venv/pip: necessari perché lo stage Test del Jenkinsfile crea un venv ed esegue pytest direttamente dentro il container Jenkins
- `build-essential`: richiesto per compilare dipendenze native (coerente con il fix `CXXFLAGS` nel Jenkinsfile)
- Installa il Docker CLI (solo il comando `docker`, non l'intero Docker Engine): il container Jenkins non ha bisogno di un proprio Docker Engine perché, tramite il socket montato (`-v //var/run/docker.sock:...`), comunica direttamente con l'Engine già in esecuzione sull'host. Serve quindi solo il client per inviare i comandi, non un secondo Engine duplicato dentro il container.

