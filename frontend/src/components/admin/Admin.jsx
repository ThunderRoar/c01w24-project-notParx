import React from 'react';
import { Outlet } from 'react-router-dom';
import { adminTabs } from '../shared/tabs-data';
import './Admin.scss';
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