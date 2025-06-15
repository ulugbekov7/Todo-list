from flask import Flask, redirect, request, render_template, url_for
from models import db, Task


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'


db.init_app(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form['task']

        if task:
            new_task = Task(
                title=task
            )
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('index'))
    
    tasks = Task.query.all()

    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.is_completed])
    remaining_tasks = total_tasks - completed_tasks

    return render_template('index.html',
                           tasks=tasks,
                           total_tasks=total_tasks,
                           completed_tasks=completed_tasks,
                           remaining_tasks=remaining_tasks
                           )


@app.route('/toggle/<int:id>')
def toggle_task(id:int):
    task = Task.query.get_or_404(id)
    task.is_completed = not task.is_completed
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete_task(id:int):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)