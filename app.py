from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML file for the calculator

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get form inputs
    storage_size_tb = float(request.form['storage_size'])  # TB
    data_egress_tb = float(request.form['data_egress'])  # TB/month
    usage_duration = int(request.form['usage_duration'])  # 1 for month, 12 for year

    # Convert TB to GB for calculations
    storage_size_gb = storage_size_tb * 1024
    data_egress_gb = data_egress_tb * 1024

    # Pricing details (per GB)
    spark_storage_cost = 0.013 * storage_size_gb * usage_duration
    spark_egress_cost = 0  # Spark has no egress fee

    aws_storage_cost = 0.023 * storage_size_gb * usage_duration
    aws_egress_cost = 0.09 * data_egress_gb * usage_duration

    gcp_storage_cost = 0.02 * storage_size_gb * usage_duration
    gcp_egress_cost = 0.12 * data_egress_gb * usage_duration

    azure_storage_cost = 0.0184 * storage_size_gb * usage_duration
    azure_egress_cost = 0.087 * data_egress_gb * usage_duration

    mediashuttle_storage_cost = 0.10 * storage_size_gb * usage_duration
    mediashuttle_egress_cost = 0.05 * data_egress_gb * usage_duration
    mediashuttle_total_cost = mediashuttle_storage_cost + mediashuttle_egress_cost

    # Google Drive pricing logic
    googledrive_cost = None  # Default as None (for when over 30TB)
    if storage_size_tb <= 0.2:
        googledrive_cost = 2.99 * usage_duration
    elif 0.2 < storage_size_tb <= 2:
        googledrive_cost = 9.99 * usage_duration
    elif 2 < storage_size_tb <= 5:
        googledrive_cost = 24.99 * usage_duration
    elif 5 < storage_size_tb <= 10:
        googledrive_cost = 49.99 * usage_duration
    elif 10 < storage_size_tb <= 20:
        googledrive_cost = 99.99 * usage_duration
    elif 20 < storage_size_tb <= 30:
        googledrive_cost = 149.99 * usage_duration

    # Dropbox pricing logic
    dropbox_cost = None  # Default as None (for when over 3TB)
    if storage_size_tb <= 2:
        dropbox_cost = 11.99 * usage_duration
    elif 2 < storage_size_tb <= 3:
        dropbox_cost = 19.99 * usage_duration

    # Total costs
    spark_total_cost = spark_storage_cost + spark_egress_cost
    aws_total_cost = aws_storage_cost + aws_egress_cost
    gcp_total_cost = gcp_storage_cost + gcp_egress_cost
    azure_total_cost = azure_storage_cost + azure_egress_cost

    return jsonify({
        'spark_cost': spark_total_cost,
        'aws_cost': aws_total_cost,
        'gcp_cost': gcp_total_cost,
        'azure_cost': azure_total_cost,
        'mediashuttle_cost': mediashuttle_total_cost,
        'googledrive_cost': googledrive_cost,
        'dropbox_cost': dropbox_cost
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
