# Programa Previsão do Brasileirão Série A

![Imagem de Futebol Ilustrativa](img/images.png)

## Introdução

Este projeto tem como objetivo mostrar todas as etapas do desenvolvimento de um programa que estima jogos para as rodadas do campeonato brasileiro da Série A.

Sendo assim, esse projeto será dividido nas seguintes etapas:

1. Levantamento de requisitos.
2. Desenvolvimento do diagrama de uso de caso.
3. Desenvolvimento do programa e códigos de teste.
4. Deploy do programa.

## Levantamento dos Requisitos

Exsitem diversas formas de ser feito o levantamento de requisitos, e uma delas é respondendo perguntas a fim de levantar e explorar mais informações. Sendo assim, os seguintes questionamentos foram levantados e respondidos.

1. Qual é o objetivo principal do programa?

   - Receber estimativas de placares das rodadas do campeonato brasileiro da série A.

2. Como as estimativas devem ser enviadas para o usuário?

   - Através de um e-mail.

3. Qual a frequência que as estimativas devem ser enviadas?

   - Um dia antes às 18 horas de cadas rodada.

4. Existe alguma taxa de acerto mínima?

   - Não inicialmente. Porém, é possível revisar esse ponto em uma segunda etapa desse projeto.

5. Deve ser utilizado dados dos anos anteriores?
   - Sim. Deve ser considerado até 5 anos antes.

## Diagrama do Usuário

Baseado nas respostas do levantamento de requisitos, é possível elaborar o seguinte diagrama do usuário.

![Diagrama do Usuário da UML](img/UML_Diagram.png)

### Detalhamento dos Cenários

Cenário Principal:

1. Sistema ativado um dia antes das rodadas às 18 horas.
2. Programa aquisita os dados atualizados das rodadas. << include >>
3. Realizar análise para aquisição da probabilidade dos jogos. << include >>
4. Enviar resultados para e-mail cadastrado. << include >>

Cenário Alternativo:

- Não acontecerá jogos na data estimada.
  - Não enviar e-mail com resultados.
- Não ser possível enviar o e-mail, pois o e-mail não é válido.
  - Enviar e-mail do gerenciador do sistema informando que não foi possível enviar as probabilidades para o e-mail determinado.

## Diagrama de Atividade

Os diagramas de atilidade são criados a fim de detalhar as etapas que serão criadas através dos códigos. Sendo assim, o seguinte diagrama é criado a partir dos cenários:

![Diagrama de Atividades](img/Diagrama_de_atividades.png)

## Aquisição das Datas das Rodadas

A primeira parte do código exige que as datas das partidas sejam aquisitadas. Sendo assim, é utilizado o seguinte código para poder fazer o web scraping do site do globo.com:

```python
#importando bibliotecas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd
from datetime import datetime
 
class Jogos:
    """
    Classe responsável pela criação das tabelas com os jogos do brasileirão,
    assim como as respectivas datas.
    """

    def __init__(self, ano):
        self.ano = ano
        opts = ChromeOptions()
        servico=Service(ChromeDriverManager().install())
        driver=webdriver.Chrome(service=servico, options=opts)
        self.driver = driver
    
    def _rodada_atual_func(self):
        """definir função para aquisitar a rodada atual"""
        try:
            self.rodada_atual = int(self.driver.find_element(By.XPATH,'/html/body/div[2]/main/div[2]/div/section[1]/section/nav/span[2]').text[:2])
        except:
            self.rodada_atual = int(self.driver.find_element(By.XPATH,'/html/body/div[2]/main/div[2]/div/section[1]/section/nav/span[2]').text[:1])

    def _primeira_rodada(self):
        """retornar para a primeira rodada"""
        while True:
            check1 = 0
            try:
                while True:
                    self.driver.find_element(By.XPATH,"/html/body/div[2]/main/div[2]/div/section[1]/section/nav/span[1]").click()
                    Jogos._rodada_atual_func(self)
                    if self.rodada_atual == 1:
                        break
                break
            except:
                if check1 == 10:
                    break
                else:
                    sleep(1)
                    check1 += 1

    def tabela_partidas(self):
        """criar tabela de jogos com datas, times mandantes e times visitantes"""
        #item 1
        self.driver.get("https://ge.globo.com/futebol/brasileirao-serie-a/")
        self.driver.maximize_window()
        self.driver.execute_script("window.scrollTo(0, 300);")
        sleep(3)
        
        #item 2
        Jogos._primeira_rodada(self)

        #item 3
        jogos_df = pd.DataFrame({'Datas':[], 'Time Mandante': [], 'Time Visitante': [], 'Rodada': []})
        while True:
            check1 = 0
            try:
                while True:
                    datas_lista, mandante_lista, visitante_lista, rodada = [], [], [], []
                    for partida in range(10):
                        data = self.driver.find_element(By.XPATH,f'/html/body/div[2]/main/div[2]/div/section[1]/section/ul/li[{partida+1}]/div/a/div/div[1]/span[2]').text
                        datas_lista.append(datetime(self.ano, int(data.split('/')[-1]), int(data.split('/')[0])))
                        mandante_lista.append(self.driver.find_element(By.XPATH,f"/html/body/div[2]/main/div[2]/div/section[1]/section/ul/li[{partida+1}]/div/a/div/div[2]/div[1]/span[1]").get_attribute('title'))
                        visitante_lista.append(self.driver.find_element(By.XPATH,f"/html/body/div[2]/main/div[2]/div/section[1]/section/ul/li[{partida+1}]/div/a/div/div[2]/div[3]/span[1]").get_attribute('title'))
                        rodada.append(int(self.rodada_atual))

                    df = pd.DataFrame({'Datas':datas_lista, 'Time Mandante': mandante_lista, 'Time Visitante': visitante_lista, 'Rodada': rodada})
                    jogos_df = pd.concat([jogos_df, df])
                    Jogos._rodada_atual_func(self)
                    if self.rodada_atual == 38:
                        break
                    else:
                        self.driver.find_element(By.XPATH,"/html/body/div[2]/main/div[2]/div/section[1]/section/nav/span[3]").click()
                break
            except:
                if check1 == 15:
                    break
                else:
                    sleep(1)
                    check1+=1
         
        #item 4                  
        self.tabela_partidas = jogos_df
        self.driver.quit()
```