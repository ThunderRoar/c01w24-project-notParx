import React from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';
import { adminTabs } from '../shared/tabs-data';
import './login.scss';
import LoginBox from './LoginBox.jsx';
import LoginHeader from './LoginHeader.jsx';

const Login = () => {

  const tabs = adminTabs

  return (
    <div className="login-component">
      <LoginHeader/>
      <LoginBox/>
    </div>
  );
};

export default Login;