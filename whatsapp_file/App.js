// import logo from './logo.svg';
// import './App.css';
// // import Sample from './Sample';
// import UserForm from './components/UserForm'
// import Records from './components/Records';
// function App() {
//   return (
//     <>
//     {/* <Sample/> */}
//     <UserForm/>
//     <Records/>
//     </>
//   );
// }

// export default App;

// App.js
import React, { useState } from 'react';
import TodoList from './components/TodoList';
import TodoForm from './components/TodoForm';

const App = () => {
    const [editingTodo, setEditingTodo] = useState(null);

    const handleSave = () => {
        setEditingTodo(null);
    };

    return (
        <div>
            <h1>Todo List</h1>
            <TodoForm todoToEdit={editingTodo} onSave={handleSave} />
            <TodoList onEdit={setEditingTodo} />
        </div>
    );
};

export default App;

