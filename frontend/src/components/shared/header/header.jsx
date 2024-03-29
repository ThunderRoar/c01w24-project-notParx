import React, { useState, useEffect } from 'react';
import './header.scss';
import logoImg from '../../../resources/img/parx_logo.png';
import AccountIcon from '@mui/icons-material/AccountCircleOutlined';
import Tab from './tabs/Tabs';
import decodeToken from '../../../token_handling/tokenHandling.js';
import "@fontsource/ubuntu";
import "@fontsource/ubuntu/400.css";
import "@fontsource/ubuntu/400-italic.css";
import { useNavigate } from 'react-router-dom';

const Header = ({ tabs }) => {

    const [displayDropdown, setDisplayDropdown] = React.useState(false)
    const [name, setName] = React.useState('')
    const [email, setEmail] = React.useState('')

    const navigate = useNavigate()

    const activeTab = 'hi';

    const handleTabClick = (tabTitle) => {
        console.log('hi');
    };

    const handleLogout = () => {
        console.log('Logout clicked')
        localStorage.removeItem('token')
        navigate('/')
    }

    const handleIconClicked = () => {
        const token = localStorage.getItem('token');
        if (token) {
            const decodedToken = decodeToken(token)
            if (!decodedToken) {
            } else if (decodedToken.user_type === 'User' || decodedToken.user_type === 'Prescriber') {
                setName(decodedToken.firstName)
                setEmail(decodedToken.email)
            } else if (decodedToken.user_type === 'Admin - Coordinator' || decodedToken.user_type === 'Admin - Assistant') {
                setName(decodedToken.username)
            }
            setDisplayDropdown(!displayDropdown)
        }
    }

    const logoImgLink = logoImg;

    return (
        <div className='header'> 
            <div className='nav'>
                <img className='logo' src={logoImgLink} />
                {tabs.length > 0 && (
                    <div className='page-links'>
                        {tabs.map((tab) => (
                            <Tab 
                                key={tab.id}
                                title={tab.name}  
                                link={tab.link}
                                isActive={activeTab === tab.name} 
                                onClick={handleTabClick} 
                            />
                        ))}
                    </div>
                )}
            </div>
            <div className='dropdown'>
                <AccountIcon className='account-icon' onClick={handleIconClicked} />
                {displayDropdown && (
                    <div className='dropdown-info'>
                        <p>Hello, {name}</p>
                        <small>{email}</small>
                        <button className='logout-button' onClick={handleLogout}>
                            <span>Logout</span>
                        </button>
                    </div>
                )}
            </div>            
        </div>
    );
  };
  
  export default Header;