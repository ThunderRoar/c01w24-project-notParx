import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';import './login.scss';
import decodeToken from '../../token_handling/tokenHandling.js';
import LoginBox from './LoginBox.jsx';
import LoginHeader from './LoginHeader.jsx';

const Login = () => {

  // If user is already logged in, have them get directed to preferred page
  const navigate = useNavigate()
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = decodeToken(token)
      if (!decodedToken) {
      } else if (decodedToken.user_type === 'User'){
        navigate('/Patient')
      } else if (decodedToken.user_type === 'Prescriber'){
        navigate('/Prescriber')
      } else if (decodedToken.user_type === 'Admin - Coordinator' || decodedToken.user_type === 'Admin - Assistant') {
        navigate('/Admin')
      }
    }
  });

  return (
    <div className="login-component">
      <LoginHeader/>
      <LoginBox/>
    </div>
  );
};

export default Login;