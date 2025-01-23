# SkillSwap
A social media application geared towards students in the Computer Science Major at UNC Charlotte.

# Motivation
This application was created for students to network with fellow classmates, figuring out which classes to take, gaining insight on interested concentrations, and overall have a common place for discussions revolving around computer science.

# Tech/Framework used
- Framework: Python - Flask
- Others: HTML, CSS, JavaScript (Frontend)

# Code Example
@app.post('/signing-in')
def signing_in():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash("Please enter the required fields")
        return redirect(url_for('sign_in'))
    user = database_methods.get_user_by_username(username)
    if user is None:
        flash("Invalid username or password")
        return redirect(url_for('sign_in'))
    if not bcrypt.check_password_hash(user['hashed_password'], password):
        flash("Invalid username or password")
        return redirect(url_for('sign_in'))
    session['user_id'] = user['user_id']
    return redirect(url_for('home_page'))
