
# Disparo-producao

## Descrição
Este script automatiza o disparo de frases para canais de atendimento (ex: WhatsApp, RH, etc) via webview, capturando as respostas do bot e salvando os resultados em arquivos XLSX na pasta `output`. O canal e o arquivo de entrada podem ser escolhidos dinamicamente.

## Como utilizar
1. **Pré-requisitos**
   - Python 3.8+
   - Instalar dependências:
     ```bash
     pip install -r requirements.txt
     ```


2. **Execução completa**
  - Para rodar tudo de uma vez (criar ambiente, instalar dependências e executar):
    1. Crie o ambiente virtual:
      ```powershell
      python -m venv .venv
      ```
    2. Ative o ambiente virtual:
      ```powershell
      .venv\Scripts\Activate
      ```
    3. Instale as dependências:
      ```powershell
      pip install -r requirements.txt
      ```
    4. Execute o script:
      ```powershell
      python disparo-webview.py
      ```

2. **Preparar arquivos**
  - Coloque o arquivo de entrada (.txt, .csv, .xlsx ou .xls) na pasta `input`. O arquivo pode ter qualquer nome.
  - Cada linha/registro deve conter uma frase para ser testada.

3. **Executar o script**
  - Para escolher o canal interativamente e detectar o arquivo automaticamente:
    ```bash
    python disparo-webview.py
    ```
    O script irá listar os canais disponíveis e pedir para digitar o nome do canal.

  - Para especificar o arquivo e canal:
    ```bash
    python disparo-webview.py meu_arquivo.txt --channels rh
    ```
    (Troque `meu_arquivo.txt` pelo nome do seu arquivo na pasta `input` e `rh` pelo canal desejado)

4. **Saída**
  - O resultado será salvo em um arquivo XLSX na pasta `output`, com o nome `output_<nome_do_arquivo>_<canal>.xlsx`.

## Observações
- O script aceita múltiplos canais separados por vírgula (ex: `--channels rh,app_mvp`).
- O arquivo de entrada pode ser `.txt`, `.csv`, `.xlsx` ou `.xls`.
- Se não houver arquivo válido na pasta `input`, o script exibirá uma mensagem de erro.
- Não é gerado arquivo `.txt` de saída, apenas `.xlsx`.

## Exemplo de uso
```bash
python disparo-webview.py frases.xlsx --channels rh,app_mvp
```
