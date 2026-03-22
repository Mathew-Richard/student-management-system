from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "student_secret_key"

# This list acts as our temporary database
students = []

def calculate_data(s):
    # Convert inputs to numbers, ignoring empty boxes
    vals = [float(s[y]) for y in ['y1', 'y2', 'y3'] if s[y] and s[y].strip() != ""]
    
    if not vals:
        s['avg'] = 0
        s['result'] = "No Data"
        return s

    avg = sum(vals) / len(vals)
    s['avg'] = round(avg, 2)
    
    # Validation Logic: CGPA usually tops out at 10.0
    if avg > 10.0:
        s['result'] = "Invalid (Too High)"
    elif avg >= 5.0:
        s['result'] = "Pass"
    else:
        s['result'] = "Fail"
    
    return s

@app.route('/')
def index():
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        s_id = request.form['id']
        name = request.form['name']
        branch = request.form['branch']
        y1 = request.form['y1']
        y2 = request.form['y2']
        y3 = request.form['y3']

        # ID Validation: Must be 6 digits
        if len(s_id) != 6 or not s_id.isdigit():
            flash("Error: Student ID must be exactly 6 digits!")
            return redirect(url_for('add'))
        
        # CGPA Validation: Ensure they aren't typing "22" or "50"
        for val in [y1, y2, y3]:
            if val and float(val) > 10.0:
                flash("Error: Individual CGPA cannot be greater than 10.0!")
                return redirect(url_for('add'))

        if not any([y1, y2, y3]):
            flash("Error: Please enter at least one year's CGPA!")
            return redirect(url_for('add'))

        new_student = {'id': s_id, 'name': name, 'branch': branch, 'y1': y1, 'y2': y2, 'y3': y3}
        students.append(calculate_data(new_student))
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    result = None
    if request.method == 'POST':
        s_id = request.form['search_id']
        result = next((s for s in students if s['id'] == s_id), None)
    return render_template('search.html', result=result)

@app.route('/delete/<s_id>')
def delete(s_id):
    global students
    students = [s for s in students if s['id'] != s_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Running locally on port 5000
    app.run(debug=True)