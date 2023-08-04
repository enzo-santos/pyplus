# pyplus

Um pacote de utilidades para uso interno.

- [pyplus](#pyplus)
  * [Instalação](#instalação)
  * [Uso](#uso)
    + [Leitura de recursos](#leitura-de-recursos)
      - [CSV](#csv)
      - [XLS](#xls)
      - [XLSX](#xlsx)
    + [Escrita de recursos](#escrita-de-recursos)
      - [CSV](#csv-1)
      - [URL](#url)

## Instalação

Execute o seguinte comando no seu terminal:

```shell
python -m pip install git+https://github.com/enzo-santos/pyplus.git
```

Em seguida, use-o no seu código de acordo com a documentação abaixo.


## Uso

Este pacote é dividido em módulos, detalhados abaixo.


### Leitura de recursos

Este módulo contém operações de leitura.

Para acessar essas funções auxiliares, utilize a seguinte importação:

```python
import pyplus.io.i
```

Todas as funções desse módulo contém os seguintes parâmetros:

- `header: bool = False`: se verdadeiro, ignora a primeira linha do arquivo


#### CSV

Para ler arquivos CSV, utilize a função `csv`:

```python
import pyplus.io.i

for linha in pyplus.io.i.csv('caminho/para/arquivo.csv'):
    print(linha)
```

O arquivo é aberto com a codificação UTF-8 e automaticamente fechado após a execução da iteração.

Contém os seguintes parâmetros adicionais:

- `delimiter: str = ';'`: define o delimitador do arquivo de texto


#### XLS

Para ler arquivos XLS, utilize a função `xls`:

```python
import pyplus.io.i

for linha in pyplus.io.i.xls('caminho/para/arquivo.xls'):
    print(linha)
```


#### XLSX

Para ler arquivos XLSX, utilize a função `xlsx`:

```python
import pyplus.io.i

for linha in pyplus.io.i.xlsx('caminho/para/arquivo.xlsx'):
    print(linha)
```


### Escrita de recursos

Este módulo contém operações de escrita.

Para acessar essas funções auxiliares, utilize a seguinte importação:

```python
import pyplus.io.o
```


#### CSV

Para criar um arquivo CSV, utilize `csv`:

```python
with pyplus.io.o.csv('caminho/para/arquivo.csv') as writer:
    writer.writerow(['a', 'b', 'c'])
```

A variável retornada por essa função é compatível com a retornada pela [função `writer` do
módulo `csv`](https://docs.python.org/3/library/csv.html#csv.writer) do Python. Isso significa
que você pode acessar os métodos `writerow` e `writerows` da mesma forma.

O parâmetro `header` define um cabeçalho a ser usado no arquivo. O código

```python
with pyplus.io.o.csv('caminho/para/arquivo.csv', header=('A', 'B', 'C')) as writer:
    pass
```

irá criar um arquivo vazio. Já o código

```python
with pyplus.io.o.csv('caminho/para/arquivo.csv', header=('A', 'B', 'C')) as writer:
    writer.writerow(['a', 'b', 'c'])
```

irá criar um arquivo CSV com o conteúdo

```csv
A;B;C
a;b;c
```

Note que o cabeçalho somente é adicionado na primeira chamada de `writerow` ou `writerows`.
Para forçar que o cabeçalho seja escrito, você pode chamar o método `writeheader`. O código

```python
with pyplus.io.o.csv('caminho/para/arquivo.csv', header=('A', 'B', 'C')) as writer:
    writer.writeheader()
```

irá criar um arquivo CSV com o conteúdo

```csv
A;B;C
```

Assim como seu homônimo de leitura, também é possível definir o delimitador do arquivo de texto
a ser escrito por meio do parâmetro `delimiter`.


#### URL

Para ler um arquivo *web* e armazenar sua resposta em um arquivo local, utilize `url`:

```python
REMOTE_FILE = 'https://file-examples.com/wp-content/storage/2017/10/file-sample_150kB.pdf'
LOCAL_FILE = 'caminho/para/arquivo.pdf'

pyplus.io.o.url(REMOTE_FILE, LOCAL_FILE, ftype='binary')
```

O parâmetro `ftype` define como o arquivo remoto deve ser salvado localmente:

- se o arquivo remoto for binário (PNG, MP4, PDF, XLSX), passe `'binary'`
- se o arquivo remoto estiver no formato JSON, passe `'json'`
- se o arquivo remoto for de texto (CSV, TXT, HTML, XML), passe `'text'`

A diferença entre `'json'` e `'text'` é que o primeiro é salvo com identação, facilitando a 
visualização.

O parâmetro `force` é falso por padrão. Isso significa que, caso já o arquivo local já exista,
não será enviada nenhuma requisição para baixar um novo arquivo remoto:

```python
pyplus.io.o.url(REMOTE_FILE, LOCAL_FILE, ftype='binary')   # Baixa o arquivo a primeira vez
pyplus.io.o.url(REMOTE_FILE, LOCAL_FILE, ftype='binary')   # Não baixa novamente
```

Caso seja verdadeiro, o arquivo será baixado novamente mesmo se já existe um arquivo local:

```python
pyplus.io.o.url(REMOTE_FILE, LOCAL_FILE, ftype='binary')               # Baixa o arquivo a primeira vez
pyplus.io.o.url(REMOTE_FILE, LOCAL_FILE, ftype='binary', force=True)   # Baixa o arquivo novamente
```

Note que este método também é compatível com APIs. O código

```python
pyplus.io.o.url('https://jsonplaceholder.typicode.com/todos/1', 'todos.json', ftype='json')
```

irá criar um arquivo JSON local.
