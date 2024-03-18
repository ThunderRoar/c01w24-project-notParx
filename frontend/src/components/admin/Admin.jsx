import React from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';
import Verification from './verification/Verification';
import Profiles from './profiles/Profiles';
import { adminTabs } from '../shared/tabs-data';
import './Admin.scss';
import Login from '../login/login';
import Patient from '../patient/Patient';
import Header from '../shared/header/header';

const Admin = () => {

  const tabs = adminTabs;

  return (
    <div className="admin-component">
      <Header tabs={tabs} />
      <Outlet />
    </div>
  );
};

export default Admin;