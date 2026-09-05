# Sentiment Analysis

Questo è un progetto pensato per eseguire una sentiment analysis su delle recensioni;
I passaggi eseguiti sono i seguenti:

- Carica un modello di Sentiment Analysis già pronto
- Espone un’API REST per ricevere una recensione e restituire il sentiment previsto
- Fornisce un endpoint per le metriche del servizio
- Integra metriche di risposta, errori di predizione e uso di CPU e memoria
- Viene deployata in modo automatico tramite Jenkins
- Si eseguono test automatici prima del deploy
- Avviabile su container
- Rende le metriche visibili in Grafana tramite Prometheus
- Il progetto è inoltre disponibile su github al link https://github.com/umbertocama13-dotcom/Sentiment_Analysis


## Visualizzazione metriche con Prometheus - grafana
Per visualizzare prometheus e grafana seguire il procedimento qui sotto:

- Aprire docker desktop  (link per download windows https://docs.docker.com/desktop/setup/install/windows-install/ )
- Aprire cmd e recarsi nella cartella del progetto (sostituire C:\percorso_progetto con il percorso corretto fino a Sentiment_analysis)
                    `cd "C:\percorso_progetto"`
- eseguire pip install requirements
- entrare in venv con il comando 
                    `venv\Scripts\activate`
- entrare nella cartella docker 
                    `cd docker`
- Far partire il container docker con il comando 
                    `docker compose up -d`
- Quando si ottiene 

    [+] up 4/4
    ✔ Network docker_default  Created                                                                                  
    ✔ Container prometheus    Started                                                                                  
    ✔ Container grafana       Started                                                                                  
    ✔ Container sentiment_app Started

    è possibile avviare il browser e inserire in due pagine separate gli indirizzi  
            `http://localhost:9090/`    e   `http://localhost:3000/`
- Eseguire il login a grafana con credenziali nome utente: `admin` password `admin`
- Su grafana andare nella sezione "dashboard" e selezionare la dashboard FastAPI Monitoring (è normale che venga segnato "No data" ovunque all'avviamento)











`ricordarsi di scrivere nelle istruzioni che in prometheus.yml va cambiata localhost:8000 manualemnte se si cambia il file.env`


## Integrazione docker, prometheus e grafana
L’integrazione tra Docker, Prometheus e Grafana ha dato risultati positivi durante i test, anche se le metriche `cpu usage` e `requests in progress` non hanno mai rilevato alcuna attività; nonostante ciò le metriche esposte dall’applicazione sono state verificate prima tramite l’endpoint /metrics in Postman e poi controllate nella sezsione "edit" di Grafana, dove sono risultate coerenti con quanto esposto dal servizio. Le due metriche semplicemente mostrano lo stato attuale dell’applicazione e se durante il test il sistema non è stato caricato a sufficienza è naturale che queste metriche rimangano a 0; Il resto delle metriche ha risposto in modo **positivo e coerente** con quanto pensato 






`Unit test`
Da fare da zero.
Devi creare e testare:

test_api.py
test_model.py
test_integration.py

`Docker`
Già fatto, ma probabilmente da aggiornare.
Se aggiungi i test, dovrai quasi sicuramente rifare l’immagine o la configurazione per includerli.

`Jenkins`
Tutto da fare.
Devi costruire la pipeline che faccia:

test
build
deploy


`Test finale end-to-end`
Da fare alla fine, quando tutto è integrato.
Serve per controllare che il progetto funzioni dall’inizio alla fine.

`README`
Da scrivere.
Deve spiegare in modo semplice:

come avviare il progetto
come eseguire i test
come usare Docker, Prometheus, Grafana e Jenkins

`Zip finale`
Da preparare alla fine, con tutto il materiale ordinato.