from flask import Flask,render_template,flash, request, url_for
from google.cloud import automl
from google.api_core.client_options import ClientOptions
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/estellev_mbialeu/hello/french-text-difficulty-350020-42d146608f7d.json"

# TODO(developer): set the following variables
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.HTML')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        # getting input with name = targetfrase in HTML form
        text = request.form.get("targetfrase")
        project_id = "french-text-difficulty-350020"
        model_id = "TCN228192643228631040"
        content = text
        print(content)

        options = ClientOptions(api_endpoint='eu-automl.googleapis.com')
        prediction_client = automl.PredictionServiceClient.from_service_account_json("french-text-difficulty-350020-42d146608f7d.json", client_options=options)


        # Get the full path of the model.
        model_full_id = automl.AutoMlClient.model_path(project_id,'eu',model_id)

        text_snippet = automl.TextSnippet(content=content,mime_type='text/')
        payload = automl.ExamplePayload(text_snippet=text_snippet)

        response = prediction_client.predict(name=model_full_id, payload=payload)
       
       #return response.payload
        for annotation_payload in response.payload:
            print(u"Predicted class name: {}".format(annotation_payload.display_name))
            print(
                u"Predicted class score: {}".format(annotation_payload.classification.score)
            )
        return render_template("result.HTML", data=response.payload, result=text)
    if request.method == 'GET':
        return "<h3> nothing to show </h3>"

if __name__ == '__main__':
    app.run()
