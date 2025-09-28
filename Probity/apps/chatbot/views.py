from django.shortcuts import render
import requests, json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def list_available_models(api_key):
    """Función para listar modelos disponibles - solo para debugging"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            models = response.json().get('models', [])
            available_models = [model.get('name', '') for model in models]
            print("Modelos disponibles:", available_models)
            return available_models
        else:
            print(f"Error al listar modelos: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al consultar modelos: {e}")
        return []

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            user_message = body.get("message", "")
            
            # Validar que el mensaje no esté vacío
            if not user_message.strip():
                return JsonResponse({"reply": "Por favor, envía un mensaje válido."}, status=400)
            
            # System prompt mejorado
            system_prompt = """
            Eres un asistente experto en probabilidad, estadística y minería de datos.
            Responde de manera clara, concisa y educativa. Si te hacen preguntas sobre distribución binomial,
            explica conceptos de forma práctica con ejemplos cuando sea apropiado.
            """
            
            # Mensaje completo combinando contexto y pregunta del usuario
            full_message = f"{system_prompt}\n\nPregunta del usuario: {user_message}"
            
            # Verificar que la API key existe
            if not hasattr(settings, 'GEMINI_API_KEY') or not settings.GEMINI_API_KEY:
                return JsonResponse({"reply": "Error: API key no configurada."}, status=500)
            
            # Para debugging: listar modelos disponibles (quitar después de solucionar)
            available_models = list_available_models(settings.GEMINI_API_KEY)
            
            # Usar uno de los modelos disponibles más estables
            # Opciones recomendadas basadas en tus modelos disponibles:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            
            payload = {
                "contents": [
                    {
                        "parts": [{"text": full_message}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2048,
                    "topK": 1,
                    "topP": 1
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            # Debug: imprimir la respuesta completa para diagnóstico
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            response.raise_for_status()  # Lanza excepción si hay error HTTP
            
            data = response.json()
            
            # Mejor manejo de la respuesta
            candidates = data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    reply = parts[0].get("text", "No se pudo obtener respuesta.")
                else:
                    reply = "Respuesta vacía del modelo."
            else:
                reply = "No se recibieron candidatos de respuesta."
            
            return JsonResponse({"reply": reply})
            
        except json.JSONDecodeError:
            return JsonResponse({"reply": "Error: Formato JSON inválido"}, status=400)
        except requests.exceptions.HTTPError as e:
            # Manejo específico de errores HTTP
            error_detail = ""
            try:
                error_response = e.response.json()
                error_detail = error_response.get("error", {}).get("message", str(e))
            except:
                error_detail = str(e)
            
            return JsonResponse({
                "reply": f"Error de API: {error_detail}"
            }, status=500)
        except requests.RequestException as e:
            return JsonResponse({"reply": f"Error de conexión: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"reply": f"Error inesperado: {str(e)}"}, status=500)
    
    return JsonResponse({"reply": "Método no permitido"}, status=405)
