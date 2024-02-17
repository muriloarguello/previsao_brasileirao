"""
Este script tem o objetivo de acionar a análise de probabilidade dos jogos 
da próxima rodada do brasileirão série A.
"""

#importando bibliotecas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd
from datetime import date

class Jogos:

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
        
        self.driver.get("https://ge.globo.com/futebol/brasileirao-serie-a/")
        self.driver.maximize_window()
        self.driver.execute_script("window.scrollTo(0, 300);")
        sleep(3)
        Jogos._primeira_rodada(self)
        jogos_df = pd.DataFrame({'Datas':[], 'Time Mandante': [], 'Time Visitante': [], 'Rodada': []})
        while True:
            check1 = 0
            try:
                while True:
                    datas_lista, mandante_lista, visitante_lista, rodada = [], [], [], []
                    for partida in range(10):
                        data = self.driver.find_element(By.XPATH,f'/html/body/div[2]/main/div[2]/div/section[1]/section/ul/li[{partida+1}]/div/a/div/div[1]/span[2]').text
                        datas_lista.append(date(self.ano, int(data.split('/')[-1]), int(data.split('/')[0])))
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
                   
        self.tabela_partidas = jogos_df
        self.driver.quit()

def main(ano):

    jogos_objeto = Jogos(ano)
    jogos_objeto.tabela_partidas()
    jogos_df = jogos_objeto.tabela_partidas

    return jogos_df

if __name__ == "__main__":
    jogos_df = main(2023)
    print(jogos_df)