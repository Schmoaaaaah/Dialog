from flask import Flask, render_template, request, redirect, url_for
import openai
import json
import conf
import json

app = Flask(__name__)

openai.api_key = conf.openai_api_key

model_engine='gpt-3.5-turbo'
content_prompt = """Deine Aufgabe besteht darin, ein Language-to-Text-System zum automatischen Ausfüllen von einem Formular zu entwerfen. Das Formular ist ein Feedback-Formular zu einer Veranstaltung. Der User kann in jeder Sprache antworten. Bitte übertrage die Antworten in das Formular in Deutsch. Bitte duze den User.
Das System sollte in der Lage sein, Eingaben in natürlicher Sprache genau und effizient in die entsprechenden Felder eines Formulars umzuwandeln.
Das Formular besteht aus folgenden Grundinformationen zur Person: Vorname, Nachname, Firma, Mailadresse. Man darf auch anonym bleiben, aber ein Antwort wäre schön.
Des Weiteren sollen folgende Fragen beantwortet werden:
1) An welchem Tag hast Du teilgenommen?
Mögliche Antworten sind 12.05.2023, 16.05.2023 oder beide Tage. Das ist auch eine Pflichtangabe.
2) Wie zufrieden bist Du mit der Veranstaltung?
Die Antworten sollen geeignet eingruppiert werden in eine Klassifizierung 1 = schlecht bis 5 = sehr gut. Das ist auch eine Pflichtangabe.
3) Inwiefern war die Veranstaltung in Bezug auf deinen Job nützlich und hilfreich?
Die Antworten sollen geeignet eingruppiert werden in eine Klassifizierung 1 = schlecht bis 5 = sehr gut. Das ist auch eine Pflichtangabe.
4) Was ist das Wichtigste, das Du aus dieser Veranstaltung für dich mitnehmen?
Hier kann der User Freitext eingeben.
Das System sollte verschiedene Faktoren berücksichtigen, die die Genauigkeit des Konvertierungsprozesses beeinflussen können, wie etwa Homophone, Synonyme und kontextspezifische Bedeutungen. Es sollte auch Funktionen wie Fehlerkorrektur und Eingabeaufforderungen enthalten, um sicherzustellen, dass Benutzer etwaige Fehler oder Inkonsistenzen in ihren Eingaben korrigieren können.
Bitte geben Sie klare Anweisungen zur Verwendung des Systems, einschließlich der Texteingabe und der Navigation durch die verschiedenen Felder im Formular. Ihre Antwort sollte auch mögliche Einschränkungen oder Herausforderungen beschreiben, die mit dem Entwurf und der Implementierung dieses Systemtyps verbunden sind
Bitte überlegen Sie abschließend, wie Ihr System für verschiedene Arten von Formularen (z. B. Bewerbungen vs. medizinische Formulare) oder Benutzergruppen (z. B. Nicht-Muttersprachler) optimiert werden könnte."""
history = [{'role':'system','content':content_prompt}]

def context_chat(history,new_prompt_content):
    new_history = {'role':'user','content':new_prompt_content}
    history.append(new_history)
    completion = openai.ChatCompletion.create(
    model=model_engine,
    messages = history,
    temperature=0.5
    )
    assistant_answer = completion['choices'][0]['message']['content']
    print(assistant_answer)
    new_assistant_history = {'role':'assistant','content':assistant_answer}
    history.append(new_assistant_history)
    return history

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]

        result = context_chat(history,user_input)
        return redirect(url_for("index", result=history[-1]['content']))

    result = request.args.get("result")
    print(history)
    return render_template("index.html", result=history[-1]['content'])

@app.route("/json", methods=("GET", "POST"))
def json():
    result = context_chat(history,"give me the results in json. Reply just with the json")
    my_json = history[-1]['content']
    print(history)
    
    return json.loads(my_json)
