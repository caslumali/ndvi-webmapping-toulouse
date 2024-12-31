Curso mestrado em géomatique na França.
Tenho como projeto final da Unité d'Enseigment fazer um Webmapping complexo.

Estou usando apenas soluções OpenSource.

Armazenei minhas camadas em um Geoserver e estou gerando um serviço do lado cliente com : Node + Vue + Vite

As camadas de entrada são:
Emprise : contorno da área de estudo
Emprise inversee : máscara para esconder informações fora da área de estudo
BDForêt : Camada da BD Forêt para uma região do departamento do Haute-Garrone, as essences estão na coluna 'Nom'
Série Temporal do NDVI : Uma série temporal de 6 meses do NDVI para o ano de 2022
6 Rasters de NDVI : Exatamente os mesmo raster acima, mas as bandas separadas por visualizações.

Há diversas parametrizações que já foram implementadas e outras que eu preciso de ajuda sua para implementar, são elas:

1. O webmaping começa centralizado na cena. Isso já está feito e quero que você respeite a coordenada que centraliza ele. ✅ feito ❌

2. O usuário não poderia dar zoom out e sair da cena se limitando a emprise do raster ✅ feito

3. O mapa base deverá ser um fundo escuro ✅ feito

4. O usuário terá a opção de escolher entre : um fundo escuro, um fundo de satélite ESRI, e algumas das 6 bandas do NDVI. ✅ feito

5. A camada da emprise inversee e da emprise não seriam selecionadas e estariam como défault sempre, pois a ideia delas é centrar a atenção do usuário na área de estudo. ✅ feito

6. Cada bandas do raster de NDVI terão como simbologia um dêgrade verde, assim que você seleciona uma banda ele mostra a legenda específica dessa banda. ✅ feito

7. Preciso adicionar uma legenda ao lando do Controle de Couche. Essa legenda vai mudar quando um raster diferente for selecionado na barra delizante. A legenda não precisa ter título, quero apenas a simbologia ❌ Legenda a fazer

8. A camada BD Forêt também está adicionada. Falta adicionar a legenda dela. A legenda não precisa ter título, quero apenas a simbologia ❌ Legenda a fazer

1. O gráfico ira recuperar os valores do raster Multibanda. Esse raster multibanda deverá ter sido acionada, mas ele não é visível. Ele é carregado apenas para ser interrogado no mapa com um clique. 
1a. Quando o usuário clica em um pixel válido o gráfico vai recuperar os valores das 6 bandas e mostrar um gráfico em ordem cronológica (no eixo X os valores de cada um dos meses do raster multibanda, no eixo Y os valores do NDVI)
1b. Se possível o gráfico deverá ser bem atraente e responsivo onde:
1c: Vamos ter os 6 valores de NDVI ligados por uma linha 
1d: Se possível o gráfico será interativo, ou seja, ele mostrará um hover assim que o mouse passar no ponto de um valor 

2. Se o usuário clicar em uma área onde não tem pixel (NoData) o serviço avisará (em Francês, obviamente) que ele precisa clicar em um área com pixel válido.

3. Em cima do gráfico terá o nome da Essence. Esse nome ficará alinhado na parte superior esquerda do gráfico e deverá ter uma fonte pequena em negrito. O nome da essence será recuperada da camada vetorial (coluna 'Nom` da Camada da BD Forêt já adicionada')

4. O usuário pode fechar e abrir o gráfico quando quiser pressionando um X no canto direito superior do gráfico


Alguma regras imporantes:

Me dê o código sempre comentado sucintamente em Francês.
Mantenha a estrutura e divisão que já estamos utilizando, com estilo separado em um .css

Se você tiver uma sugestão de melhoria de organização eu aceito.

Vamos começar simples, agora vamos resolver a questão da legenda.

Na captura de tela que enviei em anexo está a visão do mapa quando carrega.

O Gráfico deverá ocupar o espaço do retângulo vermelho
A legenda da BD Foret e dos Raster NDVI deverá ficar no parte de Controle de Couches, onde estão os retângulos verdes.