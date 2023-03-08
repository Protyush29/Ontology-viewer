import csv
import io
import requests
from flask import Flask, jsonify, make_response, request, url_for, redirect, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')
    
@app.route('/rdf_to_csv', methods=['POST'])
def rdf_to_csv():
    # Base parameters and form input
    ontology_name = request.form['Onto']
    api_url = "https://www.ebi.ac.uk/ols/api/ontologies/"+ontology_name+"/terms"

    # Make the API request and retrieve the JSON response
    response = requests.get(api_url, params={"size": 10000, "obo_format": True})
    response_json = response.json()

    # Write csv file
    csv_data = io.StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['IRI', 'label', 'obo_id'])
    for term in response_json['_embedded']['terms']:
        writer.writerow([term['iri'], term['label'], term['obo_id']])

    # Create a downloadable csv
    csv_output = csv_data.getvalue().encode('utf-8')
    response = make_response(csv_output)
    response.headers['Content-Disposition'] = 'attachment; filename=ontology.csv'
    response.headers['Content-Type'] = 'text/csv'
    
    js_code = '''
        <script>
        setTimeout(function() { window.close(); }, 1000);
        </script>
    '''
    
    response.data = response.data+js_code.encode('utf-8')

    return response
    

if __name__ == '_main_':
    app.run(debug=True)
