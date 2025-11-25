import requests
from datetime import datetime

#==============================================
#CONFIGURAÇÕES
#==============================================
API_KEY = "API_KEY_AQUI"  # Substitua pela sua chave da API
URL = "http://api.weatherapi.com/v1/forecast.json"

#==============================================
#PROGRAMA
#==============================================
def main():
    cidade = input("\nDigite o nome da cidade: ")
    pais = input("\nDigite o nome do país: ")

    local = f"{cidade},{pais}"

    # Pedido à API com previsão de 7 dias
    params = {
        "key": API_KEY,
        "q": local,
        "days": 7,
        "lang": "pt",
        "pollen": "yes"  # Adiciona dados de pólen
    }

    resposta = requests.get(URL, params=params)

    if resposta.status_code != 200:
        print("Erro ao obter dados da API.")
        return

    dados = resposta.json()

    print(f"\n Previsão para \033[38;5;214m\033[1m{dados['location']['name']}, {dados['location']['country']}\033[0m:\n")


    # Iterar pelos dias da previsão
    for dia in dados["forecast"]["forecastday"]:
        data = datetime.strptime(dia["date"], "%Y-%m-%d").strftime("%d/%m/%Y")
        temp_min = dia["day"]["mintemp_c"]
        temp_max = dia["day"]["maxtemp_c"]
        chuva = dia["day"]["daily_chance_of_rain"]
        vento = dia["day"]["maxwind_kph"]
        direcao_vento = dia["hour"][12]["wind_dir"]  # direção média ao meio-dia
        descricao = dia["day"]["condition"]["text"]
        nascer_sol = dia["astro"]["sunrise"]
        por_sol = dia["astro"]["sunset"]
        uvindex = dia["day"]["uv"]
        # Fase da Lua
        moon_phase_en = dia["astro"]["moon_phase"]
        fases_lua = {
        "New Moon": "Lua Nova",
        "Waxing Crescent": "Crescente Crescente",
        "First Quarter": "Quarto Crescente",
        "Waxing Gibbous": "Gibosa Crescente",
        "Full Moon": "Lua Cheia",
        "Waning Gibbous": "Gibosa Minguante",
        "Last Quarter": "Quarto Minguante",
        "Waning Crescent": "Crescente Minguante"
    }
        moon_phase_pt = fases_lua.get(moon_phase_en, moon_phase_en)
        # Pólen
        polen = dia["day"].get("pollen", {})

        # Print dados formatados
        print(f"\033[34m {data}\033[0m")
        print(f"    \033[33mTemp:\033[0m {temp_min:.1f}°C / {temp_max:.1f}°C")
        print(f"    \033[33mProb. precipitação:\033[0m {chuva}%")
        print(f"    \033[33mVento máx:\033[0m {vento:.1f} km/h ({direcao_vento})")
        print(f"    \033[33mDescrição:\033[0m {descricao}")
        print(f"    \033[33mNascer do sol:\033[0m {nascer_sol}")
        print(f"    \033[33mPor do sol:\033[0m {por_sol}")
        print(f"    \033[33mÍndice UV:\033[0m {uvindex}")
        print(f"    \033[33mFase da Lua:\033[0m {moon_phase_pt}")
        #print pólen
        print(f"    \033[33mPólen:\033[0m "
            f"\033[3mAveleira:\033[0m {polen.get("Hazel", "Não disponível")}, "
            f"\033[3mAmieiro:\033[0m {polen.get("Alder", "Não disponível")}, "
            f"\033[3mBétula:\033[0m {polen.get("Birch", "Não disponível")}, "
            f"\033[3mCarvalho:\033[0m {polen.get("Oak", "Não disponível")}, "
            f"\033[3mGramíneas:\033[0m {polen.get("Grass", "Não disponível")}, "
            f"\033[3mLosna:\033[0m {polen.get("Mugwort", "Não disponível")}, "
            f"\033[3mAmbrosia:\033[0m {polen.get("Ragweed", "Não disponível")}")
        print("-" * 40)

#==============================================
#EXECUÇÃO
#==============================================
if __name__ == "__main__":
    main()