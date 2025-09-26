from openai import OpenAI
from dotenv import load_dotenv
from rag import semantic_search_STRIDE
import aspose.pdf as ap
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
    sendo usada (aws, google cloud ou azure), separe cada um os itens do desenho e identifique qual é o tipo de
    solução e como ela interage entre todos os componentes do desenho
    
    Sua resposta de ser no seguinte formato:

    Modelo de cloud:
    Lista com os componentes:
    Interação entre os componentes:
    O que esse sistema faz:
    Vulnerabilidades e Solução para cara vulnerabilidade:    
    Gere um Relatório de Modelagem de Ameaças, baseado na metodologia STRIDE:

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
    
    command = """
            Você é um especialista em arquitetura de software, com base no levantamento da solução abaixo, você deve 
            gerar um diagrama marmeid com a descrição dos componente, como eles se relacionam e as correções dos pontos
            de vulnerabilidades, além disso, deve gerar um script terraform para a criação da solução           
     """   

    current_solution = analyze_image(image_path)

    prompt = command + current_solution
    
    response = client.chat.completions.create(
        model='gpt-5',
        messages=[{
            'role': 'user',
            'content': [
                {'type': 'text', 'text': prompt}
            ]
        }],        
    )
    
    improvement = response.choices[0].message.content

    print(improvement)
    generate_report(image_path, current_solution, improvement)

def generate_report (image_path, current_solution, improvement):
    complete_file_name = os.path.basename(image_path)
    file_name, _ = os.path.splitext(complete_file_name)

    document = ap.Document()   
    page = document.pages.add()    
    
    report = ap.text.TextFragment("Relatório de análise da solução: " + file_name )
    report.text_state.font_style = ap.text.FontStyles.BOLD
    report.position = ap.text.Position(200, 800)
    page.paragraphs.add(report)
    page.paragraphs.add(ap.text.TextFragment(""))  
    page.paragraphs.add(ap.text.TextFragment("")) 
    page.paragraphs.add(ap.text.TextFragment("")) 

    image_position = ap.Rectangle(500, 100, 150, 1200, True)
    page.add_image(image_path, image_position)

    current_solution_title = ap.text.TextFragment("Análise completa da solução atual")
    current_solution_title.text_state.font_style = ap.text.FontStyles.BOLD
    current_solution_title.position = ap.text.Position(90, 450)
    page.paragraphs.add(current_solution_title)
    page.paragraphs.add(ap.text.TextFragment("")) 
    page.paragraphs.add(ap.text.TextFragment(current_solution)) 
    page.paragraphs.add(ap.text.TextFragment(""))  
    page.paragraphs.add(ap.text.TextFragment("")) 

    improvement_title = ap.text.TextFragment("Sugestões de melhorias")
    improvement_title.text_state.font_style = ap.text.FontStyles.BOLD
    page.paragraphs.add(improvement_title)
    page.paragraphs.add(ap.text.TextFragment("")) 
    page.paragraphs.add(ap.text.TextFragment(improvement)) 
    page.paragraphs.add(ap.text.TextFragment(""))  
    page.paragraphs.add(ap.text.TextFragment(""))  
 
    pdf = "report/" + file_name + ".pdf"
    
    document.save(pdf)

    return pdf


solve_vulnerabilities("imagem\Cloud_aws.jpg")

# solve_vulnerabilities("imagem\Cloud_azure.jpg")

# generate_report("imagem\Arquitetura2.jpg", "teste", "melhoria")