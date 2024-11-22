from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Hardcoded machine cost options for the dropdown
machine_options = {
    "Starter Kit | 4 Cores | 16GB RAM | NVIDIA T4 16 GB VRAM": 0.99,
    "Mid-tier | 8 Cores | 32GB RAM | NVIDIA T4 16 GB VRAM": 1.99,
    "High-end | 16 Cores | 64GB RAM | NVIDIA T4 16 GB VRAM": 2.99,
    "Top-tier | 32 Cores | 128GB RAM | NVIDIA T4 16 GB VRAM": 4.99,
    "Exceptional | 48 Cores| 192GB RAM | 4 x NVIDIA T4 16 GB VRAM": 9.99,
    "Insanity | 192 Cores | 768 GB RAM  | 8 x NVIDIA A10 25 GB VRAM": 39.99,
}

@app.route('/')
def index():
    # Set a default machine for the dropdown
    default_machine = "16 Cores | 64GB RAM   | NVIDIA A10 24 GB VRAM"
    return render_template('index.html', machine_options=machine_options, default_machine=default_machine)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Form inputs
    num_devs = int(request.form['num_devs'])
    on_prem_cost_per_dev = float(request.form['on_prem_cost_per_dev'])
    annual_maint_costs = float(request.form['annual_maint_costs'])
    hours_per_day = float(request.form['hours_per_day'])
    days_per_year = int(request.form['days_per_year'])

    # Check if the SmartCompute checkbox is checked
    use_smart_compute = request.form.get('use_smart_compute') == 'on'

    # Selected machine cost from the dropdown
    spark_prostation = request.form['spark_prostation']
    machine_cost_per_hour = machine_options[spark_prostation]

    # Apply SmartCompute discount if applicable
    if use_smart_compute:
        machine_cost_per_hour *= 0.35

    # Cloud cost calculations
    total_hours = hours_per_day * days_per_year
    cloud_cost_per_dev = machine_cost_per_hour * total_hours
    total_cloud_cost = cloud_cost_per_dev * num_devs

    # On-prem cost calculations
    total_on_prem_cost = (on_prem_cost_per_dev * num_devs) + annual_maint_costs

    return jsonify({
        'cloud_cost': total_cloud_cost,
        'on_prem_cost': total_on_prem_cost
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
