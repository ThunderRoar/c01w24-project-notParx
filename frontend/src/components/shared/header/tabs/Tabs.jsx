import React from 'react';
import { NavLink } from 'react-router-dom';
import './Tabs.scss';

const Tab = ({ title, link, isActive, onClick }) => {

  return (
    <NavLink 
      to={link}  // Utilize the link prop
      className={`tab ${isActive ? 'active' : ''}`}
    >
      {title}
    </NavLink>
  );
};

export default Tab;