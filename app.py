from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Hardcoded machine cost options for the dropdowns
machine_options = {
    "g5.4xlarge/16 Core/64GB RAM/NVIDIA A10 24 GB VRAM" : 3.49,
    "g5.8xlarge/32 Core/128GB RAM/NVIDIA A10 24 GB VRAM" : 7.99,
    "r7i.24xlarge/96 Core/768GB RAM/CPU Only" : 13.27,
    "r7i.48xlarge/192 Core/1536GB RAM/CPU Only": 26.54,
    "g6e.24xlarge/96 Core/768GB RAM/4x NVIDIA L40 48GB VRAM": 21.13,
    "g6.48xlarge/192 Core/768GB RAM/8x NVIDIA L4 24GB VRAM": 26.97,
    "g5.48xlarge/192 Core/768GB RAM/8x NVIDIA A10 24GB VRAM": 29.31,
    "g6e.48xlarge/192 Core/1536GB RAM/8x NVIDIA L40 48GB VRAM": 42.27,
}

@app.route('/')
def index():
    default_coding_instance = "g5.8xlarge/32 Core/128GB RAM/NVIDIA A10 24 GB VRAM"
    default_compile_instance = "g5.48xlarge/192 Core/768GB RAM/8x NVIDIA A10 24GB VRAM"
    return render_template('index.html', machines=machine_options, default_coding_instance=default_coding_instance, default_compile_instance=default_compile_instance)
    #return render_template('index.html', machines=machine_options)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Form inputs
    num_devs = int(request.form['num_devs'])
    on_prem_cost_per_dev = float(request.form['on_prem_cost_per_dev'])
    annual_maint_costs = float(request.form['annual_maint_costs'])
    coding_percentage = float(request.form['coding_percentage']) / 100
    compile_percentage = float(request.form['compile_percentage']) / 100
    hours_per_day = float(request.form['hours_per_day'])
    days_per_year = int(request.form['days_per_year'])
    
    # Selected machine costs from the dropdowns
    coding_machine = request.form['coding_machine']
    compile_machine = request.form['compile_machine']
    
    # Fetch machine costs from the hardcoded dictionary
    coding_machine_cost = machine_options[coding_machine]
    compile_machine_cost = machine_options[compile_machine]
    
    # Cloud cost calculations
    coding_hours = hours_per_day * coding_percentage
    compile_hours = hours_per_day * compile_percentage
    cloud_cost_per_dev = (coding_machine_cost * coding_hours * days_per_year) + (compile_machine_cost * compile_hours * days_per_year)
    total_cloud_cost = cloud_cost_per_dev * num_devs
    
    # On-prem cost calculations
    total_on_prem_cost = (on_prem_cost_per_dev * num_devs) + annual_maint_costs
    
    # Return JSON response for AJAX to update results
    return jsonify({
        'cloud_cost': total_cloud_cost,
        'on_prem_cost': total_on_prem_cost
    })

if __name__ == '__main__':
    app.run(debug=True)
