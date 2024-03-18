import { Routes, Route } from 'react-router-dom';
import React from 'react';
import Login from '../login/login';
import Patient from '../patient/Patient';
import Prescriber from '../prescriber/Prescriber';
import Admin from '../admin/Admin';
import Verification from '../admin/verification/Verification';
import Profiles from '../admin/profiles/Profiles';


function Router() {

  return (
    <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/admin" element={<Admin />} />
            {/* <Route index element={<Verification />} />
            <Route path="/admin/verification" element={<Verification />} />
            <Route path="/admin/profiles" element={<Profiles />} /> */}
        <Route path="/patient" element={<Patient />} />
        <Route path="/prescriber" element={<Prescriber />} /> 
    </Routes>
  );
}

export default Router;