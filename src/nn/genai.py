from google import genai


class GenaAI():

    def __init__(self):
        self.client = genai.Client()


    def gen_text(self,prompt):

        response = self.client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        return response.text