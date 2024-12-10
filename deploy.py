import boto3
import pickle
from io import BytesIO
import pandas as pd
import numpy as np
import spacy
from tqdm import tqdm
import re
import json

from spellchecker import SpellChecker
from unidecode import unidecode
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet

spell = SpellChecker(language='pt')
nltk.download('stopwords')
nltk.download('omw-1.4')
dict_stemming = {}

def corrigir_ortografia(texto):
  palavras = texto.split()
  texto_corrigido = ''

  for i, palavra in enumerate(palavras):
    try:
      correcao = spell.correction(palavra)
    except:
      correcao = palavra

    if correcao == None:
      correcao = palavra
      
    if i == 0:
      texto_corrigido = correcao
    else:
      texto_corrigido = texto_corrigido + ' ' + correcao

  return texto_corrigido

def reconhecer_entidades_nomeadas(texto):
  nlp = spacy.load("pt_core_news_sm")
  entidades_nomeadas = []

  doc = nlp(texto)
  entidades = [(entidade.text, entidade.label_) for entidade in doc.ents]
  for entidade in entidades:
    texto = texto.replace(entidade[0], 'entidade_' + entidade[1])     

  return texto
 

def remover_stopwords(texto):
  stopwords_pt = set(stopwords.words('portuguese'))
  texto_sem_stopwords = ''

  texto = unidecode(texto)
  palavras = texto.split()
  for i, palavra in enumerate(palavras):
    if palavra.lower() not in stopwords_pt:
      if texto_sem_stopwords == '':
        texto_sem_stopwords = palavra.lower()
      else:
        texto_sem_stopwords = texto_sem_stopwords + ' ' + palavra.lower() 

  return texto_sem_stopwords

def realizar_stemming(texto):
  stemmer = SnowballStemmer("portuguese")
  palavras = texto.split()
  texto_stemmed = ''

  for i, palavra in enumerate(palavras):
    palavra_stemming = stemmer.stem(palavra)
    if i == 0:
      texto_stemmed = palavra_stemming
    else:
      texto_stemmed = texto_stemmed + ' ' + palavra_stemming 

    dict_stemming[palavra_stemming] = palavra

  return texto_stemmed

def manipulacao_sinonimos(texto, dicionario_de_sinonimos):
  palavras = nltk.word_tokenize(texto)
  novo_texto = []

  for palavra in palavras:
    if palavra in dicionario_de_sinonimos:
      sinonimos = dicionario_de_sinonimos[palavra]
      if sinonimos:
        novo_texto.append(sinonimos[0])
      else:
        novo_texto.append(palavra)
    else:
      novo_texto.append(palavra) 

  return ' '.join(novo_texto)

def bag_of_words(textos, palavras):
  word_counts = {word: [] for word in palavras}

  for texto in textos:
    counts = {word: 0 for word in palavras}
    text_words = texto.split()
    for word in text_words:
      if word in counts:
        counts[word] += 1
    for word in palavras:
      word_counts[word].append(counts[word])
  df = pd.DataFrame(word_counts)   

  return df

def lambda_handler(event, context):
  s3_bucket = 'fake-news-repository'
  s3_model = 'model.pkl'
  s3_lista_palavras = 'lista_palavras.txt'
  s3_dicionario_sinonimos = 'dicionario_de_sinonimos.txt'
 
  s3 = boto3.client('s3')

  response = s3.get_object(Bucket=s3_bucket, Key=s3_model)
  pickle_content = response['Body'].read()
  model = pickle.loads(pickle_content)
  
  response = s3.get_object(Bucket=s3_bucket, Key=s3_lista_palavras)
  file_content = response['Body'].read().decode('utf-8')
  lista_palavras_bagofwords = file_content.split()

  response = s3.get_object(Bucket=s3_bucket, Key=s3_dicionario_sinonimos)
  json_content = response['Body'].read().decode('utf-8')
  dicionario_de_sinonimos = json.loads(json_content)
 
  # Obtendo o texto a ser classificado
  texto = event['body']

  texto = re.sub(r'[^a-zA-Z0-9\s]', '', texto)
  texto_corrigido = corrigir_ortografia(texto)
  texto_entidate = reconhecer_entidades_nomeadas(texto_corrigido)
  texto_com_manipulacao_sinonimos = manipulacao_sinonimos(texto_entidate, dicionario_de_sinonimos)
  texto_stop = remover_stopwords(texto_com_manipulacao_sinonimos)
  texto_stemming = realizar_stemming(texto_stop)

  X_input = bag_of_words(texto_stemming, lista_palavras_bagofwords)

  # Carregando o modelo
  try:
    model = pickle.loads(pickle_content)
  except Exception as e:
    print(f"Erro ao carregar o modelo pickle: {e}")
    return {
      'statusCode': 500,
      'body': 'Erro interno do servidor'
    }
  
  # Executando o modelo
  try:
    prediction_result = model.predict(X_input)
  except Exception as e:
    print(f"Erro ao fazer a previsão: {e}")
    return {
      'statusCode': 500,
      'body': 'Erro interno do servidor'
    }
  
  # Retornando a resposta
  return {
    'statusCode': 200,
    'body': prediction_result
  }