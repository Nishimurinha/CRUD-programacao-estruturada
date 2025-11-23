# Rastreamento Automático de Veículos com Python e OpenCV

## Integrantes do Grupo

- André Cavalcante Moreira
- Fábio Schwarz Nishimura
- Larissa da Silva Gervásio
- Maria Eduarda A. Verdi

---

## Descrição do Projeto

Este projeto implementa um sistema de detecção e rastreamento automático de veículos em um vídeo capturado por uma câmera fixa, utilizando Python e a biblioteca OpenCV. 
Os veículos são detectados por subtração de fundo (BackgroundSubtractorMOG2) aplicada a uma região de interesse (ROI) da pista, e o rastreamento múltiplo é realizado por um algoritmo de distância euclidiana (`EuclideanDistTracker`), que atribui um identificador numérico estável para cada veículo ao longo do tempo.

---

## Instruções de Instalação e Execução

### 1. Clonar o repositório

No terminal:

git clone https://github.com/Nishimurinha/CRUD-programacao-estruturada.git
cd CRUD-programacao-estruturada


### 2. (Opcional) Criar ambiente virtual

python -m venv venv
venv\Scripts\activate # Windows

ou: source venv/bin/activate # Linux / macOS

### 3. Instalar dependências

pip install opencv-python numpy


Esses pacotes fornecem as funções de visão computacional (OpenCV) e as operações numéricas (NumPy) usadas no projeto.

### 4. Estrutura de arquivos do projeto

- `rastreamento_objetos.py`  
  Script principal que:
  - lê o vídeo de entrada (`VideoCarros.mp4` ou similar),  
  - recorta a região de interesse (ROI) da pista,  
  - gera a máscara de movimento com `BackgroundSubtractorMOG2`,  
  - aplica limiarização (threshold) e operações morfológicas para limpar a máscara,  
  - encontra os contornos dos veículos na máscara,  
  - faz a fusão de caixas muito próximas,  
  - chama o `EuclideanDistTracker` para atualizar os IDs dos veículos,  
  - desenha as caixas e identificadores sobre o vídeo.

- `tracker.py`  
  Implementa a classe `EuclideanDistTracker`, responsável por:  
  - receber as bounding boxes detectadas em cada frame,  
  - calcular o centro de cada box,  
  - comparar a distância para os centros dos frames anteriores,  
  - decidir se é o mesmo veículo (mantém o ID) ou um novo veículo (cria um novo ID).

- Arquivo de vídeo (`VideoCarros.mp4`)  
  Vídeo utilizado como entrada para o rastreamento. O caminho do arquivo é configurado diretamente no código fonte do script principal.

### 5. Executar o projeto

Com o ambiente preparado e dentro da pasta do repositório:

python rastreamento_objetos.py


O programa abrirá duas janelas:

- **Frame**: mostra o vídeo original com as caixas verdes e IDs numéricos desenhados sobre cada veículo detectado.  
- **Mask**: mostra a máscara binária de movimento usada para a detecção (regiões brancas indicam áreas em movimento).

Pressione `q` ou `Esc` para encerrar a execução.

---

## Melhorias Implementadas

Em relação ao exemplo básico apresentado no vídeo de referência (Pysource), o projeto inclui as seguintes melhorias e adaptações: 

- **Fusão de bounding boxes próximas**  
  Implementação da função `merge_close_boxes`, que une caixas muito próximas ou sobrepostas, reduzindo o problema de um mesmo veículo aparecer fragmentado em várias boxes e recebendo vários IDs.

- **Parâmetros ajustáveis de detecção e rastreamento**  
  Exposição de constantes como `AREA_MINIMA`, `MERGE_MARGIN`, `history`, `varThreshold` e o valor de `threshold` binário, permitindo calibrar o sistema de acordo com o vídeo (distância da câmera, iluminação, presença de carros escuros ou claros). 

- **Filtros de ruído com operações morfológicas**  
  Uso de operações de abertura e fechamento (morphological opening/closing) na máscara de movimento para remover ruídos pequenos e preencher buracos na silhueta dos carros, gerando contornos mais estáveis e caixas mais consistentes.

- **Documentação detalhada do código**  
  Comentários linha a linha explicam o papel de cada biblioteca, variável, função e parâmetro, facilitando o entendimento do fluxo do projeto e atendendo ao requisito de código limpo e bem documentado indicado no enunciado do trabalho. 

---

## Link do Repositório

O código-fonte completo deste trabalho está disponível publicamente em:

https://github.com/Nishimurinha/CRUD-programacao-estruturada
