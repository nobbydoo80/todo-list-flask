# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, url_for
from flask.ext.login import current_user

from . import main
from .forms import TodoForm, TodoListForm
from ..models import User, Todo, TodoList


@main.route('/')
def index():
    form = TodoForm()
    if form.validate_on_submit():
        return redirect(url_for('main.new_todolist'))
    return render_template('index.html', form=form)


@main.route('/todolists', methods=['GET', 'POST'])
def todolist_overview():
    # unregistered users don't have access to an overview
    if not current_user.is_authenticated():
        return redirect(url_for('main.index'))
    form = TodoListForm()
    if form.validate_on_submit():
        return redirect(url_for('main.add_todolist'))
    return render_template('overview.html', form=form)


@main.route('/todolist/<int:id>', methods=['GET', 'POST'])
def todolist(id):
    todolist = TodoList.query.filter_by(id=id).first_or_404()
    form = TodoForm()
    if form.validate_on_submit():
        Todo(form.todo.data, todolist.id).save()
        return redirect(url_for('main.todolist', id=id))
    return render_template('todolist.html', todolist=todolist, form=form)


@main.route('/todolist/new', methods=['POST'])
def new_todolist():
    form = TodoForm(todo=request.form.get('todo'))
    if form.validate():
        todolist = TodoList("", current_user.get_id()).save()
        Todo(form.todo.data, todolist.id).save()
        return redirect(url_for('main.todolist', id=todolist.id))
    return redirect(url_for('main.index'))


@main.route('/todolist/add', methods=['POST'])
def add_todolist():
    form = TodoListForm(todo=request.form.get('title'))
    if form.validate():
        todolist = TodoList(form.title.data, current_user.get_id()).save()
        return redirect(url_for('main.todolist', id=todolist.id))
    return redirect(url_for('main.index'))
