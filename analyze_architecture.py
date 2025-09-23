from openai import OpenAI
from dotenv import load_dotenv
from rag import semantic_search_STRIDE
import base64
import os

load_dotenv()
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def encode_image(image_path):
    with open(image_path, 'rb' ) as img:
        return base64.b64encode(img.read()).decode('utf-8')
    
def analyze_image(image_path):    
    base_64_img = encode_image(image_path)

    command = """Você é um arquiteto de software, analise a imagem identificando qual é a cloud que está
    sendo usada (aws, google cloud ou azure), separa cada um os itens do desenho e identifique qual é o tipo de
    solução e como ela interage entre todos os componentes do desenho
    
    Sua resposta de ser no seguinte formato:

    Modelo de cloud:
    Lista com os componentes:
    Interação entre os componentes:
    O que esse sistema faz:
    Vulnerabilidades e Solução para cara vulnerabilidade:
    
    Gere um Relatório de Modelagem de Ameaças, baseado na metodologia STRIDE

    """

    prompt = command + semantic_search_STRIDE.search_knowledge_STRIDE_database(command)

    response = client.chat.completions.create(
        model='gpt-5',
        messages=[{
            'role': 'user',
            'content': [
                {'type': 'text', 'text': prompt},
                {'type': 'image_url', 'image_url': 
                {'url': f'data:image/jpg;base64,{base_64_img}'}}
            ]
        }],        
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content


def solve_vulnerabilities(image_path):
    
    # Você é um arquiteto de software senior e renomado no mercado de tecnologia. 
    #     Você precisa gerar diagrama em texto (Mermaid) e
    
    command = """Monte um prompt objetivo e curto para que o dall-e gere um 
        diagrama utilizando a mesma cloud da imagem origem aplicando as correções das vulnerabilidades           
     """   

    prompt = command + analyze_image(image_path)
    
    response = client.chat.completions.create(
        model='gpt-5',
        messages=[{
            'role': 'user',
            'content': [
                {'type': 'text', 'text': prompt}
            ]
        }],        
    )

    print(response.choices[0].message.content)
    # return response.choices[0].message.content

       
    # response = client.images.generate(
    # model="dall-e-3",
    # prompt=response.choices[0].message.content,
    # size="1024x1024",
    # n=1,
    # )

    # print(response.data[0].url)
    # return response.data[0].url



solve_vulnerabilities("imagem\Arquitetura2.jpg")