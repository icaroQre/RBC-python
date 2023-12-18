import json
import PySimpleGUI as sg


def parte_3(cur, id, objetivo, path):
    with open(path, 'r') as f:
        novo_caso = json.load(f)

    cur.execute(f"SELECT * FROM public.casos_casospt WHERE caso = '{id}'")
    # Armazena os valores do banco de dados em um dicionario com as keys = as colunas do banco de dados

    # Recuperar o resultado da consulta
    row = cur.fetchone()

    # Verificar se a consulta retornou algum resultado
    if row:
        # Obter os nomes das colunas da tabela
        column_names = [desc[0] for desc in cur.description]

        # Criar um dicionário com os valores e as colunas correspondentes
        antigo_caso = dict(zip(column_names, row))

    else:
        print(f"Nenhum registro encontrado com o ID {id}")

    toprow = ["Atributo", "Valor"]
    rows_novo_caso = []
    rows_antigo_caso = []

    for key in novo_caso:
        rows_novo_caso.append([key, novo_caso[key]])
        rows_antigo_caso.append([key, antigo_caso[key]])

    tabela_novo_caso = sg.Table(values=rows_novo_caso, headings=toprow,
                                auto_size_columns=True,
                                display_row_numbers=False,
                                justification='center', key='-TABLE-',
                                selected_row_colors='red on yellow',
                                enable_events=True,
                                expand_x=True,
                                expand_y=True,
                                enable_click_events=True)

    tabela_antigo_caso = sg.Table(values=rows_antigo_caso, headings=toprow,
                                  auto_size_columns=True,
                                  display_row_numbers=False,
                                  justification='center', key='-TABLE-',
                                  selected_row_colors='red on yellow',
                                  enable_events=True,
                                  expand_x=True,
                                  expand_y=True,
                                  enable_click_events=True)

    # Cria um layout onde vai aparecer o novo caso e o antigo caso pysimplegui

    col1 = [
        [sg.Text('Novo Caso', background_color='#B2CBB0', font=('Times New Roman', 13))],
        [tabela_novo_caso],
    ]
    col2 = [[sg.Text('Caso Similar:', background_color='#B2CBB0', font=('Times New Roman', 13)),
             sg.Text(f'ID: {id} Descricao: {antigo_caso["desc_doenca"]}')],
            [tabela_antigo_caso]]
    next_button = [
        [sg.Button('Cadastrar')],
    ]
    back_button = [
        [sg.Button('Voltar')],
    ]
    layout_pag3 = [
        [sg.Column(col1, background_color='#B2CBB0'), sg.Column(col2, background_color='#B2CBB0')],
        [sg.Column(back_button, element_justification='left', expand_x=True),
         sg.Column(next_button, element_justification='right', expand_x=True),
         [sg.Text('Selecione o Objetivo:', font=('Times New Roman', 13)), sg.Text()],
         [sg.Combo(objetivo, key='objetivo', size=(20, 10), readonly=True)], ]
    ]

    window = sg.Window('Teste', layout_pag3)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            window.close()
            break
        elif event == 'Voltar':
            window.close()
            return 0
        elif event == 'Cadastrar':
            # Armazena o novo_caso no banco de dados
            cur.execute(
                f"INSERT INTO public.casos_casospt(desc_doenca, area_damaged, canker_lesion, crop_hist, date, external_decay, fruit_spots, fruiting_bodies, fruit_pods, germination, hail, int_discolor, leaf_malf, leaf_mild, leaf_shread, leafspots_halo, leafspot_size, leafspot_marg, leaves, lodging, mold_growth, mycelium, plant_growth, plant_stand, precip, roots, sclerotia, seed, seed_discolor, seed_size, seed_tmt, severity, shriveling, stem, stem_cankers, temp)VALUES ('{values['objetivo']}', '{novo_caso['area_damaged']}', '{novo_caso['canker_lesion']}', '{novo_caso['crop_hist']}', '{novo_caso['date']}', '{novo_caso['external_decay']}', '{novo_caso['fruit_spots']}', '{novo_caso['fruiting_bodies']}', '{novo_caso['fruit_pods']}', '{novo_caso['germination']}', '{novo_caso['hail']}', '{novo_caso['int_discolor']}', '{novo_caso['leaf_malf']}', '{novo_caso['leaf_mild']}', '{novo_caso['leaf_shread']}', '{novo_caso['leafspots_halo']}', '{novo_caso['leafspot_size']}', '{novo_caso['leafspot_marg']}', '{novo_caso['leaves']}', '{novo_caso['lodging']}', '{novo_caso['mold_growth']}', '{novo_caso['mycelium']}', '{novo_caso['plant_growth']}', '{novo_caso['plant_stand']}', '{novo_caso['precip']}', '{novo_caso['roots']}', '{novo_caso['sclerotia']}', '{novo_caso['seed']}', '{novo_caso['seed_discolor']}', '{novo_caso['seed_size']}', '{novo_caso['seed_tmt']}', '{novo_caso['severity']}', '{novo_caso['shriveling']}', '{novo_caso['stem']}', '{novo_caso['stem_cankers']}', '{novo_caso['temp']}')")
            sg.popup('Caso cadastrado com sucesso!', title='Sucesso')
            window.close()
            return 1