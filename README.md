```
Sentiment_analisys/
├── app/
│   ├── __pycache__/
│   ├── Logs/
│   ├── model/
│   │   ├── __init__.py
│   │   └── sentiment_analysis_model.pkl
│   ├── routes/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   └── predict.py
│   ├── schemas/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── request.py
│   ├── services/
│   │   ├── __pycache__/
│   │   ├── services_model/
│   │   │   ├── __pycache__/
│   │   │   ├── __init__.py
│   │   │   └── model_fasttext.py
│   │   ├── __init__.py
│   │   ├── check_language.py
│   │   ├── metrics_service.py
│   │   └── sentiment_service.py
│   ├── __init__.py
│   ├── logging_config.py
│   └── main.py
├── docker/
│   └── docker-compose.yml
├── Logs/
│   └── Sentiment_analysis.log
├── monitoring/
│   ├── alerts/
│   │   └── alert_rules.yml
│   ├── grafana/
│   │   └── dashboard.json
│   └── prometheus.yml
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_integration.py
│   └── test_model.py
├── venv/
├── .env
├── .env.exemple
├── .gitignore
├── .dockerignore
├── Dockerfile
├── Jenkinsfile
├── README.md
├── requirements.txt
└── run.py
```

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