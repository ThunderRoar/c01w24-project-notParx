import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import decodeToken from '../../token_handling/tokenHandling.js';
import Header from '../shared/header/header';
import './Prescriber.scss'

const Prescriber = () => {

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
      navigate('/Patient')
    } else if (decodedToken.user_type === 'Admin - Coordinator' || decodedToken.user_type === 'Admin - Assistant'){
      navigate('/Admin')
    }
  });

  return (
    <div className="prescriber-component">
      <Header tabs={[]} />
    </div>
  );
};

export default Prescriber;
