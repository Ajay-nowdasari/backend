// TodoForm.js
import React, { useState, useEffect } from 'react';
import { createTodo, updateTodo } from './api';

const TodoForm = ({ todoToEdit, onSave }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    useEffect(() => {
        if (todoToEdit) {
            setTitle(todoToEdit.title);
            setDescription(todoToEdit.description);
        }
    }, [todoToEdit]);

    const handleSubmit = (e) => {
        e.preventDefault();
        const todo = { title, description };
        if (todoToEdit) {
            updateTodo(todoToEdit.id, todo).then(() => {
                onSave();
            });
        } else {
            createTodo(todo).then(() => {
                onSave();
            });
        }
        setTitle('');
        setDescription('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Title"
                required
            />
            <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Description"
            />
            <button type="submit">{todoToEdit ? 'Update' : 'Add'} Todo</button>
        </form>
    );
};

export default TodoForm;
