import './App.scss';
import Header from './components/shared/header/header';
import { RouterProvider, createBrowserRouter, Navigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import { patientTabs, prescriberTabs, adminTabs } from './components/shared/tabs-data'
import Patient from './components/patient/Patient';
import Prescriber from './components/prescriber/Prescriber';
import Verification from './components/admin/verification/Verification';
import Profiles from './components/admin/profiles/Profiles';
import Admin from './components/admin/Admin';
import Login from './components/login/login';
import Router from './components/shared/Router';


function App() {

  const tabs = [];

  const router = createBrowserRouter([
    {
      path: "/",
      children: [
        {
          path: "login",
          element: <Login />,
        },
        {
          path: "admin",
          element: <Admin />,
          children: [
            { 
              index: true,
              element: <Navigate to="verification" replace /> 
            }, 
            {
              path: "verification",
              element: <Verification />,
            },
            {
              path: "profiles",
              element: <Profiles />,
            },
          ]
        },
        {
          path: "patient",
          element: <Patient />,
          children: [
            { 
              index: true,
              element: <Navigate to="my-prescriptions" replace /> 
            }, 
            {
              path: "my-prescriptions",
              element: <Verification />,
            },
            {
              path: "green-resources",
              element: <Profiles />,
            },
          ]
        },
        {
          path: "prescriber",
          element: <Prescriber />,
          children: [
            { 
              index: true,
              element: <Navigate to="my-prescriptions" replace /> 
            }, 
            {
              path: "my-prescriptions",
              element: <Verification />,
            },
            {
              path: "green-resources",
              element: <Profiles />,
            },
          ]
        },
      ],
    },
  ]);

  return (
    <div className="App background">
      <Header tabs={tabs} />
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
