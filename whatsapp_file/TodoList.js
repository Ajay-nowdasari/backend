// TodoList.js
import React, { useEffect, useState } from 'react';
import { fetchTodos, deleteTodo } from './api';

const TodoList = ({ onEdit }) => {
    const [todos, setTodos] = useState([]);

    useEffect(() => {
        fetchTodos().then(data => setTodos(data));
    }, []);

    const handleDelete = (id) => {
        deleteTodo(id).then(() => {
            setTodos(todos.filter(todo => todo.id !== id));
        });
    };

    return (
        <ul>
            {todos.map(todo => (
                <li key={todo.id}>
                    <span>{todo.title}</span>
                    <button onClick={() => onEdit(todo)}>Edit</button>
                    <button onClick={() => handleDelete(todo.id)}>Delete</button>
                </li>
            ))}
        </ul>
    );
};

export default TodoList;