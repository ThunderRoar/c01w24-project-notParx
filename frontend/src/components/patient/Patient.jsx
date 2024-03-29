import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import decodeToken from '../../token_handling/tokenHandling.js';
import { patientTabs } from '../shared/tabs-data';
import { Outlet } from 'react-router-dom';
import Header from '../shared/header/header';
import './Patient.scss';

const Patient = () => {
  const tabs = patientTabs;

  const navigate = useNavigate()
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/')
    }
    const decodedToken = decodeToken(token)
    if (!decodedToken) {
      navigate('/')
    } else if (decodedToken.user_type === 'Prescriber'){
      console.log('prescriber....')
      navigate('/prescriber')
    } else if (decodedToken.user_type === 'Admin - Coordinator' || decodedToken.user_type === 'Admin - Assistant') {
      navigate('/admin')
    }
  });

  return (
    <div className="patient-component">
      <Header tabs={tabs} />
      <Outlet />
    </div>
  );
};

export default Patient;