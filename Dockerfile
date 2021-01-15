FROM continuumio/anaconda3:4.4.0
COPY . /usr/app/
COPY lemmatizer /usr/local/share/nltk_data/
EXPOSE 8080
WORKDIR /usr/app/
RUN pip install -r requirements.txt
CMD python app.py
