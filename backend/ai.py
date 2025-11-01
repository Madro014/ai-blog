import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

def generate_ai_content(prompt: str) -> str:
    """
    Genera un artículo de blog completo con título, cuerpo y SEO
    basado en el prompt del usuario.
    
    Args:
        prompt (str): Tema o idea para el artículo
        
    Returns:
        str: Artículo completo formateado con título, contenido y SEO
    """
    try:
        # Usar el modelo más reciente y eficiente
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Prompt mejorado para evitar caracteres de formato
        blog_prompt = f"""
        INSTRUCCIONES CRÍTICAS:
        - NO uses markdown, HTML, ni ningún formato especial
        - NO uses asteriscos **, guiones --, almohadillas #, ni backticks ```
        - NO incluyas código, solo texto plano
        - El título debe ser la PRIMERA línea, sin prefijos
        - Separa párrafos con doble salto de línea
        - Usa puntos y aparte para separar ideas

        Escribe un artículo de blog COMPLETO y profesional sobre: "{prompt}"

        ESTRUCTURA REQUERIDA:

        TÍTULO: 
        Crea un título atractivo y optimizado para SEO (máximo 60 caracteres)
        El título debe ser la primera línea del texto, sin formato.

        INTRODUCCIÓN:
        1-2 párrafos engaging que capturen la atención del lector.
        Presenta el tema y su relevancia actual.

        DESARROLLO PRINCIPAL:
        3-4 secciones sustanciales, cada una enfocada en un aspecto diferente.
        Cada sección debe tener un subtítulo claro seguido de contenido sustancial.
        Incluye ejemplos prácticos y aplicaciones reales.

        CONCLUSIÓN:
        Resumen de los puntos clave.
        Llamada a la acción inspiradora.
        Perspectivas futuras sobre el tema.

        OPTIMIZACIÓN SEO:
        Incluye palabras clave naturales relacionadas con el tema.
        Al final, añade una meta descripción clara y concisa.

        TONO Y ESTILO:
        Profesional pero accesible.
        Informativo y útil para el lector.
        Contenido original y bien estructurado.

        FORMATO FINAL:
        Solo texto plano, sin ningún tipo de marcado.
        Separación clara entre secciones con saltos de línea.
        Párrafos bien estructurados y fáciles de leer.
        """
        
        response = model.generate_content(blog_prompt)
        
        if response.text:
            # Limpieza adicional del texto generado
            cleaned_text = clean_generated_text(response.text)
            return cleaned_text
        else:
            return generate_fallback_content(prompt)
            
    except Exception as e:
        print(f"Error generating AI content: {e}")
        return generate_fallback_content(prompt)

def clean_generated_text(text: str) -> str:
    """
    Limpia el texto generado para eliminar caracteres de formato no deseados
    """
    # Eliminar patrones comunes de markdown y código
    replacements = {
        '**': '',
        '*': '',
        '#': '',
        '```': '',
        '`': '',
        '--': '-',
        '---': '',
        '### ': '',
        '## ': '',
        '# ': ''
    }
    
    cleaned = text
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
    
    # Limpiar títulos que empiecen con caracteres extraños
    lines = cleaned.split('\n')
    if lines and lines[0].startswith(('```', '**', '#', '*')):
        # Encontrar la primera línea que parezca un título real
        for i, line in enumerate(lines):
            if len(line.strip()) > 10 and not line.strip().startswith(('```', '**', '#', '*')):
                lines[0] = line.strip()
                break
    
    # Unir líneas y asegurar separación adecuada
    cleaned = '\n'.join(lines)
    
    # Asegurar que los párrafos estén separados por doble salto de línea
    paragraphs = cleaned.split('\n\n')
    cleaned_paragraphs = []
    
    for paragraph in paragraphs:
        # Limpiar cada párrafo individualmente
        clean_para = paragraph.strip()
        if clean_para and not clean_para.startswith(('```', '**', '#', '*')):
            cleaned_paragraphs.append(clean_para)
    
    return '\n\n'.join(cleaned_paragraphs)

def generate_fallback_content(prompt: str) -> str:
    """
    Genera contenido de respaldo en caso de error de la API
    """
    return f"""Guía Completa sobre {prompt}

Introducción

En el mundo actual, {prompt} se ha convertido en un tema de vital importancia que merece ser explorado en profundidad. Este artículo te proporcionará una visión completa y práctica para que puedas entender y aplicar los conceptos más relevantes.

Importancia de {prompt}

{prompt} representa una oportunidad única para transformar nuestra forma de abordar desafíos. Sus beneficios incluyen eficiencia mejorada en procesos cotidianos, nuevas perspectivas para resolver problemas complejos, ventaja competitiva en entornos profesionales y crecimiento personal mediante el desarrollo de habilidades.

Aplicaciones Prácticas

Implementación en la Vida Diaria
Incorporar {prompt} en tu rutina puede generar resultados significativos. Comienza con pequeños pasos y gradualmente expande su aplicación para maximizar los beneficios.

Uso en Contextos Profesionales
Las organizaciones que adoptan {prompt} suelen experimentar mejoras notables en productividad y innovación. La implementación estratégica puede marcar la diferencia en resultados empresariales.

Tendencias Futuras
El panorama de {prompt} continúa evolucionando, presentando nuevas oportunidades para aquellos que se mantienen actualizados. Estar al día con los desarrollos más recientes es crucial para el éxito continuo.

Mejores Prácticas Recomendadas

Investiga continuamente sobre nuevos desarrollos en el campo
Conecta con comunidades especializadas y profesionales
Experimenta con diferentes enfoques y metodologías
Mide resultados consistentemente para ajustar estrategias
Mantén una mentalidad abierta al aprendizaje continuo

Conclusión

{prompt} no es simplemente una tendencia pasajera, sino una herramienta poderosa para el crecimiento sostenible. Al dominar sus principios fundamentales, estarás mejor preparado para los desafíos del mañana y podrás aprovechar al máximo las oportunidades que presenta este fascinante campo.

Meta Descripción: Artículo completo sobre {prompt} que explora sus beneficios, aplicaciones prácticas y mejores estrategias de implementación para obtener resultados óptimos en diversos contextos.
"""