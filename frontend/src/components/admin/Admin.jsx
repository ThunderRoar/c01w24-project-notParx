import React from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';
import Verification from './verification/Verification';
import Profiles from './profiles/Profiles';
import { adminTabs } from '../shared/tabs-data';
import './Admin.scss';
import Login from '../login/login';
import Patient from '../patient/Patient';

const Admin = () => {

  return (
    <div className="admin-component">
      <Outlet />
    </div>
  );
};

export default Admin;