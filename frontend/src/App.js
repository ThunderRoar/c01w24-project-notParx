import './App.scss';
import Header from './components/shared/header/header';
import { RouterProvider, createBrowserRouter, Navigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import { patientTabs, prescriberTabs, adminTabs } from './components/shared/tabs-data'
import AppRouter from './components/router/AppRouter';


function App() {
  return (
    <div className="App background">
      <RouterProvider router={AppRouter()}/>
    </div>
  );
}

export default App;
