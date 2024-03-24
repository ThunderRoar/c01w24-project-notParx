import './App.scss';
import Header from './components/shared/header/header';
import { RouterProvider, createBrowserRouter, Navigate } from 'react-router-dom';
import React from 'react';
import AppRouter from './components/router/AppRouter';


function App() {
  return (
    <div className="App background">
      <RouterProvider router={AppRouter()}/>
    </div>
  );
}

export default App;
