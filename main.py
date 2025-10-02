#                               ------ ESTUDANTE *A* -------
from datetime import datetime

def validarData(dataStr, formato="%d-%m-%Y"):
    try:
        datetime.strptime(dataStr, formato)
        return True  
    except ValueError:
        return False  


contador_ids = 0

def adicionarEvento(listaEventos, nome, data, local, categoria):
    if not nome.strip() or not data.strip() or not local.strip() or not categoria.strip():
        print('\n❌ Falha ao adicionar: todos os campos devem ser preenchidos!')
        return False
    
    if not validarData(data):
        print('\n❌ Data inválida! Use o formato DD-MM-AAAA.')
        #print("Data inválida: por favor digite no formato DD-MM-AAAA.")
        return False
    
    #verificaçao de duplicatas
    for evento in listaEventos:
        if (evento['nome'].lower().strip() == nome.lower().strip() and \
        evento['data'].strip() == data.strip() and \
        evento ['categoria'].lower().strip() == categoria.lower().strip()):
             print('\n⚠️ Falha ao adicionar: evento já existe na lista.')
             return False
        
#     # Outra abordagem usando tuplas e sets (mais eficiente para listas grandes)
#     evento_chave = (nome.lower().strip(), data.strip(), categoria.lower().strip())
# +     chaves_existentes = set(
# +         (evento['nome'].lower().strip(), evento['data'].strip(), evento['categoria'].lower().strip())
# +         for evento in listaEventos
# +     )
# +     if evento_chave in chaves_existentes:
# +         print('Falha ao adicionar: evento já existe na lista.')
# +         return False
    
        
    #gerador de ID's 
    global contador_ids 
    contador_ids += 1
    novoID = f'{"EVT"}-{contador_ids}'

    novoEvento = {
        'id' : novoID,
        'nome' : nome.strip().lower(),
        'data' : data.strip(),
        'local' : local.strip().lower(),
        'categoria' : categoria.strip().lower(),
        'participado': False
    }

    listaEventos.append(novoEvento)
    print(f"\n🎉 Evento '{nome.title()}' adicionado com sucesso! ID: {novoID} ✅")
    return True

def listarEventos(listaEventos):
    if not listaEventos:
        print('\n 🔍 Lista de eventos vazia. Use a opção 1 para adicionar um evento.')
        return False
    
    print("\n🎉 EVENTOS CADASTRADOS!")
    
    #converte o valor booleano de 'participado' em texto
    for evento in listaEventos:
        if evento['participado']: #True
            statusParticipacao = 'Sim'
        else:
            statusParticipacao = 'Não'

        print("\n╔" + "═"*40 + "╗")
        print(f"║ 🆔 ID: \033[1;36m{evento['id']:<32}\033[0m║")
        print(f"║ 📌 Nome: \033[1;33m{evento['nome'].title():<30}\033[0m║")
        print(f"║ 🗓️  Data: \033[1;35m{evento['data']:<29}\033[0m║")
        print(f"║ 📍 Local: \033[1;34m{evento['local'].title():<29}\033[0m║")
        print(f"║ 🏷️  Categoria: \033[1;32m{evento['categoria'].title():<24}\033[0m║")
        print(f"║ {'✅ Participado' if evento['participado'] else '❌ Não Participado':<38}║")
        print("╚" + "═"*40 + "╝")



        # print("\033[1;30m" + "-~~•─• Detalhes do Evento •─•~~-" + "\033[0m")
        # print(f'ID: {evento["id"]}')
        # print(f'Nome: {evento["nome"].title()}')
        # print(f'Data: {evento["data"]}')
        # print(f'Local: {evento["local"].title()}')
        # print(f'Categoria: {evento["categoria"].title()}')
        # print(f'Participado: {statusParticipacao}')

    return True


def procurarEventoPorNome(listaEventos, nome):
    if not nome.strip():
         print('\n❌ Por favor, digite um nome para busca.')
         return False
    
    nomes_encontrados = [] #lista temporaria para guardar os eventos encontrados
    contador = 0 

    for evento in listaEventos:
        if nome.lower().strip() in evento['nome'].lower().strip():
            nomes_encontrados.append(evento)
            contador += 1

    if contador == 0:
        print(f'\n 🔍 Nenhum evento foi encontrado com o nome: {nome.strip()}')
    elif contador == 1:
        print(f'\n ✅ 1 evento encontrado com o nome: {nome.strip()}')
    else:
        print(f'\n ✅ {contador} eventos foram encontrados com o nome: {nome.strip()}')

    if nomes_encontrados:
        listarEventos(nomes_encontrados) #mostra detalhadamente o(s) evento(s)
     
    return bool(nomes_encontrados)

def deletarEvento(listaEventos, id):
    for evento in listaEventos:
        if id == evento['id']:
            print(f"\n⚠️ Tem certeza que deseja deletar este evento?\n")
            print(f"   🆔 {evento['id']} | 📌 Nome: {evento['nome'].title()} | 📅 Data: {evento['data']} | 📍Local: {evento['local'].title()}\n")
            escolha = input('Digite "Sim" para continuar, ou digite "Não" para cancelar a operação: ')
            print()

            if escolha.strip().lower() in ('s' , 'sim'):
                listaEventos.remove(evento)
                print('🗑️  Evento removido com sucesso!')
                return True 
            elif escolha.strip().lower() in ('nao','não' , 'n'):
                print('❌ A operação está sendo cancelada.')
                return False
            else:
                print('⚠️ Resposta inválida, digite: SIM (S/Sim) ou NÃO (N/Nao)')
                return False       
            
    print(f'\n 🔍 Evento com ID "{id}" não encontrado.')
    return False

    
# =============== ESTUDANTE B: INTERFACE E RELATÓRIOS ===============

def displayMenu():
    print("\n" + "="*50)
    print("           🎉 GERENCIADOR DE EVENTOS 🎉")
    print("="*50)
    print("1. ➕ Adicionar novo evento")
    print("2. 📋 Listar todos os eventos")
    print("3. 🔍 Buscar evento por nome")
    print("4. 🏷️  Filtrar eventos por categoria")
    print("5. ✅ Marcar evento como participado")
    print("6. 📊 Gerar relatório resumido")
    print("7. 🗑️  Excluir evento por ID")
    print("0. ❌ Sair")
    print("="*50)

def getEscolhaDoUsuario():
    try:
        return int(input("➡️  Escolha uma opção: "))
    except ValueError:
        return -1

def filtrarEventosPorCategoria(listaEventos, categoria):
    encontrados = []
    categoria = categoria.strip().lower()

    # Exemplo abaixo usando list comprehension
    # encontrados = [evento for evento in listaEventos if categoria in evento["categoria"].lower()]
    
    for evento in listaEventos:
        if categoria in evento["categoria"].lower():
            encontrados.append(evento)
            
    if encontrados:
        print(f"\n🏷️  Eventos na categoria '{categoria}':")
        for evento in encontrados:
            # Usando get() para evitar erro se a chave não existir
            # status = "✅ Participado" if evento.get("participado", False) else "❌ Não participado"
            status = "✅ Participado" if evento["participado"] else "❌ Não participado"
            print(f"ID: {evento['id']} | Nome: {evento['nome']} | Data: {evento['data']} | "
                  f"Local: {evento['local']} | {status}")
    elif not encontrados:
        print(f"Nenhum evento encontrado na categoria '{categoria}'.")
        return False
    return encontrados

def marcarEventoAtendido(listaEventos, id):
    for evento in listaEventos:
        if evento["id"] == id.upper().strip():
            evento["participado"] = True
            print(f"✅ Evento '{evento['nome']}' (ID: {id}) marcado como participado!")
            return True
    print(f"❌ Evento com ID {id} não encontrado.")
    return False

def gerarRelatorio(listaEventos):
    total = len(listaEventos)
    if total == 0:
        print("📊 Nenhum evento cadastrado para gerar relatório.")
        return

    categorias = {}
    participados = 0

    for evento in listaEventos:
        cat = evento["categoria"]
        # Usando get() para inicializar ou incrementar
        # categorias[cat] = categorias.get(cat, 0) + 1
        if cat in categorias:
            categorias[cat] += 1
        else:
            categorias[cat] = 1
                
        # if evento.get("participado", False):
        #     participados += 1
        if evento["participado"]:
            participados += 1

    perc_participados = (participados / total) * 100 if total > 0 else 0

    print("\n" + "="*40)
    print("        📊 RELATÓRIO RESUMIDO")
    print("="*40)
    print(f"📌 Total de eventos: {total}")
    print(f"✅ Eventos participados: {participados} ({perc_participados:.1f}%)")
    print("\n📈 Eventos por categoria:")
    for cat, qtd in categorias.items():
        print(f"   • {cat}: {qtd}")
    print("="*40)

# =============== FUNÇÃO PRINCIPAL ===============

def main():
    eventos = []

    while True:
        displayMenu()
        escolha = getEscolhaDoUsuario()

        if escolha == 0:
            print("👋 Obrigado por usar o Gerenciador de Eventos! Até logo!")
            break

        elif escolha == 1:
            print("\n--- ➕ Adicionar Novo Evento ---")
            nome = input("Nome do evento: ").strip()
            data = input("Data (DD-MM-AAAA): ").strip()
            local = input("Local: ").strip()
            categoria = input("Categoria: ").strip()
            adicionarEvento(eventos, nome, data, local, categoria)

        elif escolha == 2:
            print("\n--- 📋 Lista de Todos os Eventos ---")
            listarEventos(eventos)

        elif escolha == 3:
            print("\n--- 🔍 Buscar Evento por Nome ---")
            nome_busca = input("Digite parte do nome: ")
            procurarEventoPorNome(eventos, nome_busca)

        elif escolha == 4:
            print("\n--- 🏷️  Filtrar por Categoria ---")
            cat_busca = input("Digite a categoria: ")
            filtrarEventosPorCategoria(eventos, cat_busca)

        elif escolha == 5:
            print("\n--- ✅ Marcar Evento como Participado ---")
            try:
                id_evento = input("ID do evento: ")
                marcarEventoAtendido(eventos, id_evento)
            except ValueError:
                print("❌ ID inválido. Digite um número inteiro.")

        elif escolha == 6:
            print("\n--- 📊 Gerar Relatório ---")
            gerarRelatorio(eventos)

        elif escolha == 7:
            print("\n--- 🗑️  Excluir Evento ---")
            try:
                id_evento = input("ID do evento: ")
                deletarEvento(eventos, id_evento)
            except ValueError:
                print("❌ ID inválido. Digite um número inteiro.")

        else:
            print("⚠️  Opção inválida. Tente novamente.")

        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()