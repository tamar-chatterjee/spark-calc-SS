from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file for the calculator

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get form inputs
    storage_size = float(request.form['storage_size'])  # GB
    data_egress = float(request.form['data_egress'])  # GB/month
    usage_duration = int(request.form['usage_duration'])  # months

    # Pricing details
    spark_storage_cost = 0.013 * storage_size * usage_duration
    spark_egress_cost = 0  # Spark has no egress fee

    aws_storage_cost = 0.023 * storage_size * usage_duration
    aws_egress_cost = 0.09 * data_egress * usage_duration

    gcp_storage_cost = 0.02 * storage_size * usage_duration
    gcp_egress_cost = 0.12 * data_egress * usage_duration

    azure_storage_cost = 0.0184 * storage_size * usage_duration
    azure_egress_cost = 0.087 * data_egress * usage_duration

    # Total costs
    spark_total_cost = spark_storage_cost + spark_egress_cost
    aws_total_cost = aws_storage_cost + aws_egress_cost
    gcp_total_cost = gcp_storage_cost + gcp_egress_cost
    azure_total_cost = azure_storage_cost + azure_egress_cost

    return jsonify({
        'spark_cost': spark_total_cost,
        'aws_cost': aws_total_cost,
        'gcp_cost': gcp_total_cost,
        'azure_cost': azure_total_cost
    })

if __name__ == '__main__':
    app.run(debug=True)
