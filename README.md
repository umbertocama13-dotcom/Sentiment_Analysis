# Sentiment Analysis
## Descrizione progetto
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

Ulteriori informazioni sulle scelte implementative e su come è stato costruito il programma sono presenti nel file **workflow_sviluppo.md**


**NOTA**: come modello di sentiment analysis è stato utilizzato il modello suggerito dalla consegna (indirizzo qui sotto)

https://github.com/Profession-AI/progetti-devops/raw/refs/heads/main/Deploy%20e%20monitoraggio%20di%20un%20modello%20di%20sentiment%20analysis%20per%20recensioni/sentimentanalysismodel.pkl.

Le performance del modello originale non erano qualitativamente positive, pertanto è stato addestrato un modello alternativo (TF-IDF + Logistic Regression su un sottoinsieme selezionato di recensioni Amazon, link seguente https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews?select=test.csv ), che performa meglio ed è stato lasciato come opzione di default. Il vecchio modello resta comunque disponibile per essere riattivato.

Per cambiare modello: sostituire il file nella cartella **app/model** mantenendo lo stesso nome, oppure aggiungere il nuovo file nella cartella e aggiornare la variabile **MODEL_PATH** nel file .env con **app/model/NOME_MODELLO.pkl**.



## Download e startup applicazione
- Assicurarsi di avere git scaricato e funzionante (link per download https://git-scm.com/install/ )
- Aprire il cmd
- Portarsi in una cartella dove si vuole depositare l'applicazione
                    `cd "C:\percorso_file"`
- Clonare la repository
                    `git clone https://github.com/umbertocama13-dotcom/Sentiment_Analysis`
- Entrare nella cartella del progetto 
                    `cd Sentiment_Analysis`
- Avviare un virtual environment (l'operazione richiede alcuni secondi)
                    `python -m venv venv` 
- Entrare nel venv
                    `venv\Scripts\activate`
- Eseguire il download delle dipendenze
                    `pip install -r requirements.txt`


- A fine esecuzione progetto è possibile uscire dalla venv con il comando
                    `deactivate`



## Visualizzazione metriche con Prometheus - grafana
Per visualizzare prometheus e grafana seguire il procedimento qui sotto:

- Aprire docker desktop  (link per download windows https://www.docker.com/products/docker-desktop/ )
- Se non ancora eseguito, tramite cmd recarsi nella cartella del progetto (sostituire C:\percorso_progetto con il percorso corretto fino a Sentiment_analysis)
                    `cd "C:\percorso_progetto"`
- Se non ancora eseguito, entrare in venv con il comando 
                    `venv\Scripts\activate`
- Entrare nella cartella docker 
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
- Eseguire il login su grafana con credenziali nome utente: `admin` password `admin`
- Su grafana andare nella sezione "dashboard" e selezionare la dashboard FastAPI Monitoring (è normale che venga segnato "No data" ovunque all'avviamento, aggiornare la dashboard dopo qualche minuto)
- Aprire una terza pagina del browser 
                    `http://localhost:8000/docs`
Da qui sarà possibile, tramite json, inserire una richiesta nell'endpoint
**NOTA**: potrebbe richiedere anche 3-4 minuti prima che FastAPI si avvii correttamente
- Selezionare POST /predict
- Selezionare Try it out
- Seguire le istruzioni di schema per inserire la richiesta, quindi premere "execute" per vedere il risultato
- Su Grafana adesso si devono vedere i dati nella dashboard
- Finito l'utilizzo dell'applicazione, per terminare, digitare su cmd:
                    `docker compose down`
- Quindi chiudere venv
                    `deactivate`


**NOTA**: L’integrazione tra Docker, Prometheus e Grafana ha dato risultati positivi durante i test, anche se le metriche `cpu usage` e `requests in progress` non hanno mai rilevato alcuna attività; nonostante ciò le metriche esposte dall’applicazione sono state verificate prima tramite l’endpoint /metrics in Postman e poi controllate nella sezione "edit" di Grafana, dove sono risultate coerenti con quanto esposto dal servizio. 
Le due metriche semplicemente mostrano lo stato attuale dell’applicazione e se durante il test il sistema non è stato caricato a sufficienza è naturale che queste metriche rimangano a 0; Il resto delle metriche ha risposto in modo **positivo e coerente** con quanto pensato 



## CI/CD con Jenkins
La seguente procedura di utilizzo di jenkins è stata ideata in quanto la macchina su cui si è eseguito il progetto è datata e non permetteva l'utilizzo di docker in macchina virtuale, così si è utilizzato lo stratagemma di containerizzare jenkins con docker, eseguire tutto in una cartella dedicata, quindi rimuovere tutte le tracce dell'utilizzo di jenkins dal PC.

- Aprire docker
- Aprire cmd e creare una cartella dedicata per contenere jenkins
                    `mkdir "C:\jenkins-custom"`
- Tramite esplora risorse entrare nella cartelle e incollare il file (si trova nel progetto) **script_dockerfile.txt** rinominandolo **dockerfile** (**SENZA** estensioni)                    
- Tramite cmd entrare nella cartella 
                    `cd "C:\jenkins-custom"`
- Costruire il container
                    `docker build -t jenkins-custom .`
- Eseguire il contenuto del container
                    `docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -v //var/run/docker.sock:/var/run/docker.sock jenkins-custom`
- Cercare la password di jenkins con il comando 
                    `docker logs jenkins`
la password si trova sotto la scritta **Please use the following password to proceed to installation:** 
ed ha una forma simile a **eaa2eb428afe48a6b0e7bf05ec469f0b**

- Da browser aprire la pagina
                    `http://localhost:8080`
quindi inserire la password amministratore precedentemente recuperata

- Cliccare su **installa componenti aggiuntivi consigliati** e attendere la fine del caricamento
- Completare la pagina *Crea primo utente amministratore* e ricordarsi nome utente e password
- Procedere premendo su *salva e continua*, quindi *Inizia ad utilizzare Jenkins*
- In alto a sinistra premere su "nuovo elemento", quindi emettere il nome della pipeline (esmepio *sentiment-analysis-pipeline*) e selezionare l'item **pipeline**. Premere ok per confermare
- Scorrere fino alla sezione *Definition* e selezionare **Pipeline script from SCM**
- Nella voce *SCM* selezionare **git**
- Inserire l'url di github **https://github.com/umbertocama13-dotcom/Sentiment_Analysis.git**
- Controllare che sotto la voce *Rami a costruire* / *ramo* sia scritto `*/master`, quindi cliccare su *save*
- Dopo il salvataggio, nel menù a sinistra, premere su **Compila ora** (il comando potrebbe richiedere tempo)
- In basso a sinistra compare l'esecusione della compilazione; dal menù a tendina premere su "Console output" per visualizzare l'output della compilazione (l'operazione richiederà circa 10-15 minuti)
- Al termine dell'operazione, se tutto è andato a buon fine, deve uscire la scritta 
                    *[Pipeline] End of Pipeline*
                    *Finished: SUCCESS*
- Per finire è possibile chiudere la pagina del browser e spostarsi su CMD per eliminare i residui di jenkins dal PC; eseguire in ordine:
                    `docker stop jenkins`               *ferma il conteiner*
                    `docker rm jenkins`                 *rimuove il container*
                    `docker volume rm jenkins_home`     *rimuove configurazione dati di jenkins*
                    `docker rmi jenkins-custom`         *rimuove immagine costruita*
                    `docker rmi jenkins/jenkins:lts`    *rimuove immagine scaricata*
                    `docker ps -a`                      *controllare che non sia rimasto jenkins*
- Da CMD spostarsi in una cartella diversa da quella provvisoria creata precedentemente ed eseguire:
                    `rmdir /s /q C:\jenkins-custom`

