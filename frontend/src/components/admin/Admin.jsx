import React, { useEffect } from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';
import Verification from './verification/Verification';
import Profiles from './profiles/Profiles';
import { adminTabs } from '../shared/tabs-data';
import './Admin.scss';
import Header from '../shared/header/header';
import { useNavigate } from 'react-router-dom';
import decodeToken from '../../token_handling/tokenHandling.js';

const Admin = () => {

  const navigate = useNavigate()
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/')
    }
    const decodedToken = decodeToken(token)
    if (!decodedToken) {
      navigate('/')
    } else if (decodedToken.user_type === 'User'){
      navigate('/patient')
    } else if (decodedToken.user_type === 'Prescriber'){
      navigate('/prescriber')
    }
  });

  const tabs = adminTabs;

  return (
    <div className="admin-component">
      <Header tabs={tabs} />
      <Outlet />
    </div>
  );
};

export default Admin;